# Copyright (c) 2025 Arm Limited. All rights reserved.
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

# Python VSI Audio Client module
# This module provides a client interface for communicating with a VSI (Virtual Streaming Interface) audio server.
# It allows configuration, streaming, and audio data transfer operations, typically used in hardware simulation or testing environments.

try:
    import time
    import atexit
    import logging
    import subprocess
    from multiprocessing.connection import Client, Connection
    from os import path, getcwd
    from os import name as os_name
except ImportError as err:
    print(f"VSI:Audio:ImportError: {err}")
    raise
except Exception as e:
    print(f"VSI:Audio:Exception: {type(e).__name__}")
    raise

logger = logging.getLogger(__name__)


class AudioClient:
    """
    Client for communicating with the VSI audio server using Python's multiprocessing connection.
    Provides methods to configure the stream, send/receive audio data, and control the server.
    """
    def __init__(self):
        # Server command codes
        self.SET_MODE         = 1
        self.SET_DEVICE       = 2
        self.SET_FILENAME     = 3
        self.STREAM_CONFIGURE = 4
        self.STREAM_ENABLE    = 5
        self.STREAM_DISABLE   = 6
        self.AUDIO_READ       = 7
        self.AUDIO_WRITE      = 8
        self.CLOSE_SERVER     = 9

        # Audio format codes
        self.PCM_S8           = 0
        self.PCM_S16LE        = 1
        self.PCM_S24LE        = 2
        self.PCM_S32LE        = 3
        self.PCM_F32LE        = 4

        # Connection object
        self.conn = None

    def connectToServer(self, address, authkey):
        """
        Attempt to connect to the VSI audio server at the given address with the provided authkey.

        Args:
            address: The (IP, port) tuple for the server to connect to.
            authkey: The authorization key for server connection.
        Returns:
            None
        """
        for _ in range(50):
            try:
                self.conn = Client(address, authkey=authkey.encode('utf-8'))
                if isinstance(self.conn, Connection):
                    break
                else:
                    self.conn = None
            except Exception:
                self.conn = None
            time.sleep(0.01)

    def setMode(self, mode):
        """
        Set the mode of the audio stream (input/output).
        Args:
            mode: 1 for input, 2 for output.
        Returns:
            True if the mode is valid, False otherwise.
        """
        self.conn.send([self.SET_MODE, mode])
        mode_valid = self.conn.recv()

        return mode_valid

    def setDevice(self, device):
        """
        Set the audio streaming device index (input/output).
        Args:
            device: The device index value to set on the server.
        Returns:
            Device index actually set.
        """
        self.conn.send([self.SET_DEVICE, device])
        device_index = self.conn.recv()

        return device_index

    def setFilename(self, filename):
        """
        Set the filename for the audio stream on the server.
        Args:
            filename: The name of the file to set on the server.
        Returns:
            True if the filename is valid, False otherwise.
        """
        self.conn.send([self.SET_FILENAME, getcwd(), filename])
        filename_valid = self.conn.recv()

        return filename_valid

    def configureStream(self, channels, sample_rate, sample_bits):
        """
        Configure the audio stream parameters on the server.
        Args:
            channels: Number of audio channels (1=mono, 2=stereo).
            sample_rate: Sample rate in Hz (e.g., 44100, 48000).
            sample_bits: Bit depth (8, 16, 24, 32).
        Returns:
            True if configuration is valid, False otherwise.
        """
        self.conn.send([self.STREAM_CONFIGURE, channels, sample_rate, sample_bits])
        configuration_valid = self.conn.recv()

        return configuration_valid

    def enableStream(self):
        """
        Enable the audio stream on the server in the specified mode (input/output).
        Returns:
            `True` if the stream is active, `False` otherwise.
        """
        self.conn.send([self.STREAM_ENABLE])
        stream_active = self.conn.recv()

        return stream_active

    def disableStream(self):
        """
        Disable the audio stream on the server.
        Returns:
            True if the stream is no longer active, False otherwise.
        """
        self.conn.send([self.STREAM_DISABLE])
        stream_active = self.conn.recv()

        return stream_active

    def readAudio(self, size):
        """
        Request audio data from the server.
        Args:
            size: Number of bytes to read.
        Returns:
            tuple: (data, eos) where data is a Bytearray of audio data and eos is a Boolean indicating end-of-stream.
        """
        self.conn.send([self.AUDIO_READ, size])
        data = self.conn.recv_bytes()
        eos  = self.conn.recv()

        return data, eos

    def writeAudio(self, data):
        """
        Send audio data to the server.
        Args:
            data: Bytearray of audio data to write.
        Returns:
            None
        """
        self.conn.send([self.AUDIO_WRITE])
        self.conn.send_bytes(data)

    def closeServer(self):
        """
        Close the connection to the server and request server shutdown.
        Returns:
            None
        """
        try:
            if isinstance(self.conn, Connection):
                self.conn.send([self.CLOSE_SERVER])
                self.conn.close()
        except Exception as e:
            logger.error(f'Exception occurred on cleanup: {e}')



# User register variables (simulate hardware registers for VSI peripheral)
CONTROL                   = 0     # Regs[0]  // Control: enable, mode, continuous
STATUS                    = 0     # Regs[1]  // Status: active, eos, file_name, file_valid
DEVICE                    = -1    # Regs[2]  // Streaming device
FILENAME                  = ""    # Regs[3]  // Filename string array
CHANNELS                  = 1     # Regs[4]  // Number of audio channels
SAMPLE_RATE               = 16000 # Regs[5]  // Sample rate
SAMPLE_BITS               = 16    # Regs[6]  // Bits per sample


# CONTROL register bit definitions
CONTROL_ENABLE_Pos        = 0
CONTROL_ENABLE_Msk        = 1<<CONTROL_ENABLE_Pos
CONTROL_MODE_Pos          = 1
CONTROL_MODE_Msk          = 3<<CONTROL_MODE_Pos
CONTROL_CONTINUOUS_Pos    = 3
CONTROL_CONTINUOUS_Msk    = 1<<CONTROL_CONTINUOUS_Pos

CONTROL_MODE_NONE         = 0
CONTROL_MODE_IN           = 1
CONTROL_MODE_OUT          = 2


# STATUS register bit definitions
STATUS_ACTIVE_Msk         = 1<<0    # Stream is active
STATUS_DATA_Msk           = 1<<1    # Data is available
STATUS_EOS_Msk            = 1<<2    # End of stream
STATUS_FILE_NAME_Msk      = 1<<3    # File name latched/received
STATUS_FILE_VALID_Msk     = 1<<4    # File is valid


# Global variables for audio client and filename handling
Audio                     = AudioClient()


def cleanup():
    """
    Close the VSI Audio Server on exit.
    Returns:
        None
    """
    Audio.closeServer()


def init(address, authkey):
    """
    Initialize connection to the VSI Audio Server and start the server process if not already running.
    Args:
        address: Tuple (IP, port) for the server.
        authkey: Authorization key for server connection.
    Returns:
        None
    """

    base_dir = path.dirname(__file__)
    server_path = path.join(base_dir, 'vsi_audio_server.py')

    logger.info("Start audio server")
    if path.isfile(server_path):
        # Start Audio Server as a subprocess
        if os_name == 'nt':
            py_cmd = 'python'
        else:
            py_cmd = 'python3.9'
        cmd = f"{py_cmd} {server_path} "\
              f"--ip {address[0]} "\
              f"--port {address[1]} "\
              f"--authkey {authkey}"
        subprocess.Popen(cmd, shell=True)

        # Connect to Audio Server
        Audio.connectToServer(address, authkey)
        if Audio.conn == None:
            logger.error("Server not connected")
    else:
        logger.error(f"Server script not found: {server_path}")

    # Register clean-up function
    atexit.register(cleanup)

    if Audio.conn == None:
        return False
    else:
        return True


def timerEvent():
    """
    Timer event callback (called when VSI Timer overflow occurs).

    If not in continuous mode, disables the stream.
    Returns:
        None
    """
    if (CONTROL & CONTROL_CONTINUOUS_Msk) == 0:
        wrCONTROL(CONTROL & ~CONTROL_ENABLE_Msk)


def rdDataDMA(size):
    """
    Read data from the server (simulate DMA peripheral-to-memory transfer).

    This method is called when VSI Timer overflow occurs.
    Args:
        size: Number of bytes to read (multiple of 4).
    Returns:
        data: Bytearray of audio data.
    """
    global STATUS

    if (STATUS & STATUS_ACTIVE_Msk) != 0:

        data, eos = Audio.readAudio(size)
        if eos:
            STATUS |= STATUS_EOS_Msk
            logger.debug("rdDataDMA: STATUS register updated: EOS bit set")
    else:
        data = bytearray()

    # Set DATA bit after the block of data is read
    STATUS |= STATUS_DATA_Msk
    logger.debug("rdDataDMA: STATUS register updated: DATA bit set")

    return data


def wrDataDMA(data, size):
    """
    Write data to the server (simulate DMA memory-to-peripheral transfer).

    Args:
        data: Bytearray of audio data to write.
        size: Number of bytes to write (multiple of 4).
    """
    global STATUS

    if (STATUS & STATUS_ACTIVE_Msk) != 0:

        Audio.writeAudio(data)

        # Set DATA bit after the block of data is written
        STATUS |= STATUS_DATA_Msk
        logger.debug("wrDataDMA: STATUS register updated: DATA bit set")


def wrCONTROL(value):
    """
    Write to the CONTROL register (user register).

    Args:
        value: 32-bit value to write to CONTROL register.
    """
    global CONTROL, STATUS

    if ((value ^ CONTROL) & CONTROL_MODE_Msk) != 0:
        # MODE changed
        mode_valid = Audio.setMode((value & CONTROL_MODE_Msk) >> CONTROL_MODE_Pos)
        if mode_valid:
            logger.info("wrCONTROL: CONTROL register updated: MODE changed")
        else:
            # Reset Mode
            Audio.setMode(0)
            value &= ~CONTROL_MODE_Msk
            logger.error("wrCONTROL: CONTROL register updated: MODE cleared")

    if ((value ^ CONTROL) & CONTROL_ENABLE_Msk) != 0:
        # ENABLE bit changed
        if (value & CONTROL_ENABLE_Msk) != 0:
            logger.info("wrCONTROL: CONTROL register updated: ENABLE bit set")

            # Configure stream
            configuration_valid = Audio.configureStream(CHANNELS, SAMPLE_RATE, SAMPLE_BITS)
            if configuration_valid:
                # Configuration is valid, enable stream
                server_active = Audio.enableStream()

                if server_active:
                    STATUS |=  STATUS_ACTIVE_Msk
                    STATUS &= ~STATUS_EOS_Msk
                else:
                    logger.error("wrCONTROL: enable stream failed")
            else:
                logger.error("wrCONTROL: configure stream failed")
        else:
            logger.info("wrCONTROL: CONTROL register updated: ENABLE bit cleared")
            Audio.disableStream()

            STATUS &= ~STATUS_ACTIVE_Msk
            logger.info("wrCONTROL: STATUS register updated: ACTIVE bit cleared")

    CONTROL = value


def rdSTATUS():
    """
    Read the STATUS register (user register).

    Returns:
        status: Current STATUS register value (32-bit)
    """
    global STATUS
    logger.info(f"rdSTATUS: read STATUS: 0x{STATUS:08X}")
    value = STATUS

    # Clear DATA bit on read of STATUS register
    STATUS &= ~STATUS_DATA_Msk
    logger.debug("rdSTATUS: STATUS register updated: DATA bit cleared")

    return value


def wrDEVICE(value):
    """
    Write DEVICE register (user register).
    Write is ignored if value to write equals to -1.

    Args:
        value: Device index to set.
    Returns:
        None
    """
    global DEVICE
    DEVICE = Audio.setDevice(value)
    logger.info(f"wrDEVICE: DEVICE register set to {DEVICE}")


def rdFILENAME():
    """
    Read FILENAME register (user register).

    Returns:
        filename_len: Length of the filename string
    """
    global FILENAME
    value = len(FILENAME)
    logger.info(f"rdFILENAME: read FILENAME length: {value}")
    return value


def wrFILENAME(value):
    """
    Write FILENAME register (user register).

    Append character represented by argument `value` to the filename string.
    Write 0 to set a null terminator.
    First character received after null terminator starts a new filename.
    Args:
        value: Character to append (as string or int)
    Returns:
        None
    """
    global FILENAME, STATUS

    char = chr(value)

    if STATUS & STATUS_FILE_NAME_Msk:
        # Clear file related flags and reset filename
        STATUS &= ~(STATUS_FILE_NAME_Msk | STATUS_FILE_VALID_Msk)
        logger.debug("wrFILENAME: STATUS register updated: FILE_NAME and FILE_VALID bits cleared")

        FILENAME = ""
        logger.info("wrFILENAME: FILENAME register reset")

    if char != '\0':
        # Got character to append
        logger.debug(f"wrFILENAME: append {char} to filename")
        FILENAME += f"{char}"
    else:
        # Got null terminator
        logger.info(f"wrFILENAME: filename: {FILENAME}")

        STATUS |= STATUS_FILE_NAME_Msk
        logger.debug("wrFILENAME: STATUS register updated: FILE_NAME bit set")

        if Audio.setFilename(FILENAME) == True:
            STATUS |= STATUS_FILE_VALID_Msk
            logger.debug("wrFILENAME: STATUS register updated: FILE_VALID bit set")
        else:
            logger.error("wrFILENAME: Filename validation failed, file not found on server")


def rdRegs(index):
    """
    Read user registers (the VSI User Registers).

    Read the value of a user register by index.
    Args:
        index: User register index (zero based)
    Returns:
        value: Value read (32-bit)
    """
    global CONTROL, DEVICE, CHANNELS, SAMPLE_RATE, SAMPLE_BITS
    value = 0

    if   index == 0:
        value = CONTROL
    elif index == 1:
        value = rdSTATUS()
    elif index == 2:
        value = DEVICE
    elif index == 3:
        value = rdFILENAME()
    elif index == 4:
        value = CHANNELS
    elif index == 5:
        value = SAMPLE_RATE
    elif index == 6:
        value = SAMPLE_BITS

    return value


def wrRegs(index, value):
    """
    Write user registers (the VSI User Registers).

    Write a value to a user register by index.
    Args:
        index: User register index (zero based)
        value: Value to write (32-bit)
    Returns:
        value: Value written (32-bit)
    """
    global STATUS, CHANNELS, SAMPLE_RATE, SAMPLE_BITS

    if   index == 0:
        wrCONTROL(value)
    elif index == 1:
        value = STATUS
    elif index == 2:
        wrDEVICE(value)
    elif index == 3:
        wrFILENAME(value)
    elif index == 4:
        CHANNELS = value
    elif index == 5:
        SAMPLE_RATE = value
    elif index == 6:
        SAMPLE_BITS = value

    return value
