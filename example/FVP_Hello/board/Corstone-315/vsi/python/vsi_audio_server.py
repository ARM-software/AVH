# Copyright (c) 2025-2026 Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Python VSI Audio Server module

try:
    import argparse
    import ipaddress
    import logging
    import time
    import wave
    from multiprocessing.connection import Listener
    from pathlib import Path

    import pyaudio
    import numpy as np
except ImportError as err:
    raise SystemExit(f"VSI:Audio:Server:ImportError: {err}") from err
except Exception as e:
    raise SystemExit(f"VSI:Audio:Server:Exception: {type(e).__name__}: {e}") from e

logger = logging.getLogger(__name__)

## Set verbosity level
#verbosity = logging.DEBUG
#verbosity = logging.INFO
#verbosity = logging.WARNING
verbosity = logging.ERROR

# [debugging] Verbosity settings
level = { 10: "DEBUG",  20: "INFO",  30: "WARNING",  40: "ERROR" }
logging.basicConfig(format='VSI Audio Server: [%(levelname)s]\t%(message)s', level = verbosity)
logger.info("Verbosity level is set to " + level[verbosity])

# Default Server configuration
default_address       = ('127.0.0.1', 6001)
default_authkey       = 'vsi_audio'

# Supported file extensions
supported_files  = ['wav']

# Mode Input/Output
MODE_AUDIO_INPUT      = 0
MODE_AUDIO_OUTPUT     = 1

class AudioServer:
    """Implements a TCP server for audio streaming and sample I/O.

    Supports both audio files and microphone/speaker devices as input/output.
    Listens for commands from a client (such as setting mode, filename, configuring stream,
    enabling/disabling stream, reading/writing audio data), and performs the requested audio
    operations using PyAudio and wave modules.
    """
    def __init__(self, address, authkey):
        """
        Initialize the AudioServer.

        Sets up command codes, audio format constants, and initializes all state variables.
        Creates a Listener object for incoming client connections.
        Args:
            address: The (IP, port) tuple for the server to listen on.
            authkey: The authorization key for client connections.
        Returns:
            None
        """
        # Server commands
        self.SET_MODE         = 1
        self.SET_DEVICE       = 2
        self.SET_FILENAME     = 3
        self.STREAM_CONFIGURE = 4
        self.STREAM_ENABLE    = 5
        self.STREAM_DISABLE   = 6
        self.AUDIO_READ       = 7
        self.AUDIO_WRITE      = 8
        self.CLOSE_SERVER     = 9

        # Variables
        self.listener         = Listener(address, authkey=authkey.encode('utf-8'))
        self.device           = 0
        self.filename         = None
        self.mode             = MODE_AUDIO_INPUT
        self.active           = False
        self.eos              = False
        self.stream           = None
        self.wave_file        = None
        self.pyaudio_obj      = pyaudio.PyAudio()
        self.audio_buffer     = bytearray()
        self.chunk_size       = 1024

        # Stream configuration
        self.channels         = None
        self.sample_rate      = None
        self.sample_bits      = None

    def _setMode(self, mode):
        """
        Set the stream mode to input (microphone/file) or output (speakers/file).

        Args:
            mode: The I/O mode (input or output).
        Returns:
            Current mode value.
        """
        if mode == MODE_AUDIO_INPUT:
            self.mode = MODE_AUDIO_INPUT
            logger.info("_setMode: set stream mode to Input")

        elif mode == MODE_AUDIO_OUTPUT:
            self.mode = MODE_AUDIO_OUTPUT
            logger.info("_setMode: set stream mode to Output")

        else:
            logger.error(f"_setMode: invalid mode {mode}, keeping current mode")

        return self.mode

    def _setDevice(self, device):
        """
        Set the streaming device index for input/output.

        Sets the device index to the specified value, or
        scans for the default device if -1 (0xFFFFFFFF) is given.

        Args:
            device: The device index to set.
        Returns:
            Device index actually set.
        """
        logger.debug(f"_setDevice: device={device}")

        if (device == 4294967295):  # -1 as unsigned 32-bit
            # Set device index to point to default device for the selected mode
            self.device = self._scan_audio_devices()
        else:
            # Set device index to the specified value
            self.device = device

        logger.info(f"_setDevice: streaming device set to {self.device}")

        return self.device

    def _setFilename(self, base_dir, filename):
        """
        Set the filename for input or output file.

        Checks file extension to determine if file format is supported.
        For input: verifies file exists and is supported.
        For output: removes existing file if present.
        Args:
            base_dir: The base directory for the file.
            filename: The name of the file (with extension).
        Returns:
            filename_valid: True if the filename is valid and set, False otherwise.
        """
        logger.debug(f"_setFilename: base_dir={base_dir}, filename={filename}")

        filename_valid = False

        self.filename = None

        if filename == "":
            # Empty filename is valid (use microphone/speakers)
            return True

        work_dir   = Path(base_dir)
        file_name  = Path(filename)
        file_path  = Path("")

        # Check if file extension is supported
        ext = file_name.suffix.lstrip('.').lower()
        if ext not in supported_files:
            logger.error(f"_setFilename: unsupported file extension={ext}")
            return filename_valid

        # Check if filename is absolute path
        if file_name.is_absolute():
            # Absolute path provided
            file_path = file_name
            logger.debug(f"_setFilename: absolute path provided, file path={file_path}")
        else:
            # Relative path provided, create full path
            file_path = work_dir / file_name
            logger.debug(f"_setFilename: relative path provided, file path={file_path}")

        # Normalize the file path
        file_path = file_path.resolve()

        if self.mode == MODE_AUDIO_INPUT:
            # Check if the file exists
            if Path(file_path).exists():
                # File exists
                filename_valid = True
            else:
                logger.error(f"_setFilename: file does not exist: {file_path}")

        if self.mode == MODE_AUDIO_OUTPUT:
            # Check if the file exists
            if Path(file_path).exists():
                # Remove existing file
                Path(file_path).unlink(missing_ok=True)

            filename_valid = True

        if filename_valid:
            # Set server side filename
            self.filename = file_path
            logger.info(f"_setFilename: filename set to {self.filename}")

        return filename_valid

    def _configureStream(self, channels, sample_rate, sample_bits):
        """
        Configure the audio stream parameters.

        Args:
            channels: The number of audio channels (1=mono, 2=stereo).
            sample_rate: The sample rate in Hz (8000, 16000, 44100, 48000).
            sample_bits: The bit depth (8, 16, 24, 32).
        Returns:
            configuration_valid: True if the configuration is valid and set, False otherwise.
        """
        logger.debug(f"_configureStream: channels={channels}, sample_rate={sample_rate}, sample_bits={sample_bits}")

        if channels <= 0 or sample_rate <= 0 or sample_bits <= 0:
            logger.error(f"_configureStream: invalid argument (channels={channels}, sample_rate={sample_rate}, sample_bits={sample_bits})")
            return False

        if sample_bits not in [8, 16, 24, 32]:
            logger.error(f"_configureStream: unsupported sample_bits={sample_bits}")
            return False

        self.channels = channels
        self.sample_rate = sample_rate
        self.sample_bits = sample_bits

        logger.info(f"_configureStream: stream configured to {self.channels} channels, {self.sample_rate}Hz, {self.sample_bits} bits")

        return True

    def _get_pyaudio_format(self):
        """Get PyAudio format based on sample bits."""
        if self.sample_bits == 8:
            return pyaudio.paUInt8
        elif self.sample_bits == 16:
            return pyaudio.paInt16
        elif self.sample_bits == 24:
            return pyaudio.paInt24
        elif self.sample_bits == 32:
            return pyaudio.paInt32
        else:
            return pyaudio.paInt16  # default

    def _scan_audio_devices(self):
        """
        Scan and log available audio devices, separating input and output devices.
        Returns:
            Default device index for the current mode.
        """
        if self.pyaudio_obj is None:
            logger.error(" _scan_audio_devices: PyAudio object is not initialized")
            return 0

        logger.info("=== Available Audio Devices ===")
        device_count = self.pyaudio_obj.get_device_count()

        input_devices = []
        output_devices = []

        # Scan all devices
        for i in range(device_count):
            try:
                info = self.pyaudio_obj.get_device_info_by_index(i)
                host_api_info = self.pyaudio_obj.get_host_api_info_by_index(info['hostApi'])

                device_info = {
                    'index': i,
                    'name': info['name'],
                    'max_input_channels': info['maxInputChannels'],
                    'max_output_channels': info['maxOutputChannels'],
                    'default_sample_rate': info['defaultSampleRate'],
                    'host_api': host_api_info['name']
                }

                # Categorize devices
                if info['maxInputChannels'] > 0:
                    input_devices.append(device_info)
                if info['maxOutputChannels'] > 0:
                    output_devices.append(device_info)

            except Exception as e:
                logger.warning(f"Device {i}: Error reading device info - {e}")

        # Retrieve default devices
        try:
            default_input = self.pyaudio_obj.get_default_input_device_info()
            default_output = self.pyaudio_obj.get_default_output_device_info()
        except Exception as e:
            logger.warning(f"Error getting default devices: {e}")

        if self.mode == MODE_AUDIO_INPUT:
            # Log input devices
            logger.info("--- INPUT DEVICES ---")
            if input_devices:
                for device in input_devices:
                    logger.debug(f"Device {device['index']}: {device['name']}")
                    logger.debug(f"  - Input Channels: {device['max_input_channels']}")
                    logger.debug(f"  - Sample Rate: {device['default_sample_rate']}")
            else:
                logger.info("No input devices found")

            logger.info(f"Default Input Device: {default_input['index']} - {default_input['name']}")

            rval = default_input['index']

        if self.mode == MODE_AUDIO_OUTPUT:
            # Log output devices
            logger.debug("--- OUTPUT DEVICES ---")
            if output_devices:
                for device in output_devices:
                    logger.debug(f"Device {device['index']}: {device['name']}")
                    logger.debug(f"  - Output Channels: {device['max_output_channels']}")
                    logger.debug(f"  - Sample Rate: {device['default_sample_rate']}")
            else:
                logger.info("No output devices found")

            logger.info(f"Default Output Device: {default_output['index']} - {default_output['name']}")

            rval = default_output['index']

        return rval

    def _audio_callback_input(self, in_data, frame_count, time_info, status):
        """
        Callback for PyAudio input stream.
        """
        logger.debug(f"_audio_callback_input: received {len(in_data)} bytes")

        self.audio_buffer.extend(in_data)
        return (None, pyaudio.paContinue)

    def _audio_callback_output(self, in_data, frame_count, time_info, status):
        """
        Callback for PyAudio output stream.
        """
        logger.debug(f"_audio_callback_output: requested {frame_count} frames")

        bytes_needed = frame_count * self.channels * (self.sample_bits // 8)
        if len(self.audio_buffer) >= bytes_needed:
            data = bytes(self.audio_buffer[:bytes_needed])
            del self.audio_buffer[:bytes_needed]
        else:
            # Not enough data, return silence
            data = b'\x00' * bytes_needed
        return (data, pyaudio.paContinue)

    def _enableStream(self):
        """
        Enable the audio stream for input (microphone/file) or output (file/speakers).

        Initializes the PyAudio stream or wave file as needed.
        Returns:
            None
        """
        if self.active:
            logger.info("_enableStream: stream already active")
            return

        self.eos = False
        self.audio_buffer.clear()

        try:
            if self.filename == None:
                # Use microphone/speakers
                if self.pyaudio_obj is None:
                    logger.error("_enableStream: PyAudio object is not initialized")
                    return

                audio_format = self._get_pyaudio_format()

                if self.mode == MODE_AUDIO_INPUT:
                    logger.debug("_enableStream: use microphone for input streaming")
                    self.stream = self.pyaudio_obj.open(
                        format=audio_format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        input_device_index=self.device,
                        frames_per_buffer=self.chunk_size,
                        stream_callback=self._audio_callback_input
                    )
                    self.stream.start_stream()

                if self.mode == MODE_AUDIO_OUTPUT:
                    logger.debug("_enableStream: use speakers for output streaming")
                    self.stream = self.pyaudio_obj.open(
                        format=audio_format,
                        channels=self.channels,
                        rate=self.sample_rate,
                        output=True,
                        output_device_index=self.device,
                        frames_per_buffer=self.chunk_size,
                        stream_callback=self._audio_callback_output
                    )
                    self.stream.start_stream()

                logger.info(f"_enableStream: audio device stream properties: channels={self.channels}, rate={self.sample_rate}, bits={self.sample_bits}")

            else:
                # Set file name string for audio file
                file = str(self.filename.absolute())

                logger.debug(f"_enableStream: use audio file: {file}")

                if self.mode == MODE_AUDIO_INPUT:
                    self.wave_file = wave.open(file, 'rb')

                    # Verify file properties match configuration
                    file_channels = self.wave_file.getnchannels()
                    file_rate = self.wave_file.getframerate()
                    file_bits = self.wave_file.getsampwidth() * 8

                    if (file_channels != self.channels or file_rate != self.sample_rate or file_bits != self.sample_bits):
                        logger.warning(f"_enableStream: file properties ({file_channels}ch, {file_rate}Hz, {file_bits}bit) "
                                     f"don't match configured ({self.channels}ch, {self.sample_rate}Hz, {self.sample_bits}bit)")

                    logger.info(f"_enableStream: input file properties: channels={file_channels}, rate={file_rate}, bits={file_bits}")

                if self.mode == MODE_AUDIO_OUTPUT:
                    self.wave_file = wave.open(file, 'wb')
                    self.wave_file.setnchannels(self.channels)
                    self.wave_file.setsampwidth(self.sample_bits // 8)
                    self.wave_file.setframerate(self.sample_rate)

                    logger.info(f"_enableStream: output file properties: channels={self.channels}, rate={self.sample_rate}, bits={self.sample_bits}")

            self.active = True
            logger.info("_enableStream: stream enabled")

        except Exception as e:
            logger.error(f"_enableStream: failed to enable stream: {e}")
            self._disableStream()

    def _disableStream(self):
        """
        Disable the audio stream and release resources.

        Returns:
            None
        """
        self.active = False

        try:
            if self.stream is not None:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            if self.pyaudio_obj is not None:
                self.pyaudio_obj.terminate()
                self.pyaudio_obj = None

            if self.wave_file is not None:
                self.wave_file.close()
                self.wave_file = None

        except Exception as e:
            logger.error(f"_disableStream: error during cleanup: {e}")

        logger.info("_disableStream: stream disabled")

    def _readAudio(self, size):
        """
        Read audio data from the current source.

        Args:
            size: Number of bytes to read.
        Returns:
            audio_data: The read audio data as a bytearray, or empty if no data is available.
        """
        logger.debug(f"_readAudio: size={size} bytes")

        audio_data = bytearray()

        if not self.active:
            logger.error("_readAudio: stream not active")
            return audio_data

        if self.eos:
            logger.debug("_readAudio: end of stream")
            return audio_data

        try:
            if self.filename == None:
                # Read from microphone buffer
                while len(self.audio_buffer) < size:
                    # Wait for enough data
                    time.sleep(0.01)  # Wait 10ms

                # Now we have enough data
                audio_data = bytearray(self.audio_buffer[:size])
                del self.audio_buffer[:size]

                logger.debug(f"_readAudio: read {len(audio_data)} bytes from microphone buffer")

            else:
                # Read from wave file
                frames_to_read = size // (self.channels * (self.sample_bits // 8))
                frames_data = self.wave_file.readframes(frames_to_read)

                if len(frames_data) > 0:
                    audio_data = bytearray(frames_data)
                    logger.debug(f"_readAudio: read {len(audio_data)} bytes from file")
                else:
                    self.eos = True
                    logger.debug("_readAudio: end of file reached")

        except Exception as e:
            logger.error(f"_readAudio: error reading audio data: {e}")

        return audio_data

    def _writeAudio(self, data):
        """
        Write audio data to the output destination (file or speakers).

        Args:
            data: The input audio data as a bytearray to be written.
        Returns:
            None
        """
        logger.debug(f"_writeAudio: audio data size={len(data)} bytes")

        if not self.active:
            logger.error("_writeAudio: stream not active")
            return

        try:
            if self.filename == None:
                # Write to speakers buffer
                self.audio_buffer.extend(data)
                logger.debug("_writeAudio: added data to speaker buffer")

            else:
                # Write to wave file
                self.wave_file.writeframes(data)
                logger.debug("_writeAudio: wrote data to file")

        except Exception as e:
            logger.error(f"_writeAudio: error writing audio data: {e}")

    def run(self):
        """
        Main server loop.

        Waits for a client connection, then processes commands in a loop.
        Handles all supported commands: set filename, configure stream, enable/disable stream, read/write audio, close server.
        Sends responses or audio data as appropriate.
        """
        logger.info("Audio server started")

        try:
            conn = self.listener.accept()
            logger.info(f'Connection accepted {self.listener.address}')
        except Exception:
            logger.error("Connection not accepted")
            return

        while True:
            try:
                recv = conn.recv()
            except EOFError:
                return

            cmd     = recv[0]  # Command
            payload = recv[1:] # Payload

            if   cmd == self.SET_MODE:
                current_mode = self._setMode(payload[0])
                conn.send(current_mode)

            elif cmd == self.SET_DEVICE:
                device_valid = self._setDevice(payload[0])
                conn.send(device_valid)

            elif cmd == self.SET_FILENAME:
                filename_valid = self._setFilename(payload[0], payload[1])
                conn.send(filename_valid)

            elif cmd == self.STREAM_CONFIGURE:
                configuration_valid = self._configureStream(payload[0], payload[1], payload[2])
                conn.send(configuration_valid)

            elif cmd == self.STREAM_ENABLE:
                self._enableStream()
                conn.send(self.active)

            elif cmd == self.STREAM_DISABLE:
                self._disableStream()
                conn.send(self.active)

            elif cmd == self.AUDIO_READ:
                size = payload[0]
                audio_data = self._readAudio(size)
                conn.send_bytes(audio_data)
                conn.send(self.eos)

            elif cmd == self.AUDIO_WRITE:
                audio_data = conn.recv_bytes()
                self._writeAudio(audio_data)

            elif cmd == self.CLOSE_SERVER:
                self.stop()


    def stop(self):
        """
        Stop the audio server.

        Releases all resources.
        Returns:
            None
        """
        self._disableStream()
        self.listener.close()
        logger.info("Audio server stopped")


def ip(ip):
    """
    Validate that the input string is a valid IP address.
    Args:
        ip: The input IP address string to validate.
    Returns:
        ip: The validated IP address string. Raises an argparse.ArgumentTypeError if invalid.
    """
    try:
        _ = ipaddress.ip_address(ip)
        return ip
    except:
        raise argparse.ArgumentTypeError(f"Invalid IP address: {ip}!")

def parse_arguments():
    """
    Parse command-line arguments for the audio server (IP, port, authkey).
    Returns:
        args: The parsed command-line arguments.
    """
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=41)
    parser = argparse.ArgumentParser(formatter_class=formatter, description="VSI Audio Server")

    parser_optional = parser.add_argument_group("optional")
    parser_optional.add_argument("--ip", dest="ip",  metavar="<IP>",
                                        help=f"Server IP address (default: {default_address[0]})",
                                        type=ip, default=default_address[0])
    parser_optional.add_argument("--port", dest="port",  metavar="<TCP Port>",
                                        help=f"TCP port (default: {default_address[1]})",
                                        type=int, default=default_address[1])
    parser_optional.add_argument("--authkey", dest="authkey",  metavar="<Auth Key>",
                                        help=f"Authorization key (default: {default_authkey})",
                                        type=str, default=default_authkey)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    Server = AudioServer((args.ip, args.port), args.authkey)
    try:
        Server.run()
    except KeyboardInterrupt:
        Server.stop()
