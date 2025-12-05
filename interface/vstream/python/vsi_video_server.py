# Copyright (c) 2023-2025 Arm Limited. All rights reserved.
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

# Python VSI Video Server module

try:
    import argparse
    import ipaddress
    import logging
    from multiprocessing.connection import Listener
    from pathlib import Path

    import cv2
    import numpy as np
except ImportError as err:
    print(f"VSI:Video:Server:ImportError: {err}")
except Exception as e:
    print(f"VSI:Video:Server:Exception: {type(e).__name__}")

logger = logging.getLogger(__name__)

## Set verbosity level
#verbosity = logging.DEBUG
#verbosity = logging.INFO
#verbosity = logging.WARNING
verbosity = logging.ERROR

# [debugging] Verbosity settings
level = { 10: "DEBUG",  20: "INFO",  30: "WARNING",  40: "ERROR" }
logging.basicConfig(format='VSI Video Server: [%(levelname)s]\t%(message)s', level = verbosity)
logger.info("Verbosity level is set to " + level[verbosity])

# Default Server configuration
default_address       = ('127.0.0.1', 6000)
default_authkey       = 'vsi_video'

# Supported file extensions
video_file_extensions = ('wmv', 'avi', 'mp4')
image_file_extensions = ('bmp', 'png', 'jpg')
video_fourcc          = {'wmv' : 'WMV1', 'avi' : 'MJPG', 'mp4' : 'mp4v'}

# Mode Input/Output
MODE_VIDEO_NONE       = 0
MODE_VIDEO_INPUT      = 1
MODE_VIDEO_OUTPUT     = 2

class VideoServer:
    """Implements a TCP server for video streaming and frame I/O.

    Supports both video and image files as input/output, and can interface with a camera device.
    Listens for commands from a client (such as setting mode, filename, configuring stream,
    enabling/disabling stream, reading/writing frames), and performs the requested video
    operations using OpenCV.
    """
    def __init__(self, address, authkey):
        """
        Initialize the VideoServer.

        Sets up command codes, color space constants, and initializes all state variables.
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
        self.FRAME_READ       = 7
        self.FRAME_WRITE      = 8
        self.CLOSE_SERVER     = 9
        # Color space
        self.GRAYSCALE8       = 0
        self.RGB888           = 1
        self.BGR565           = 2
        self.YUV420           = 3
        self.NV12             = 4
        self.NV21             = 5
        # Variables
        self.listener         = Listener(address, authkey=authkey.encode('utf-8'))
        self.device           = 0
        self.filename         = None
        self.mode             = None
        self.active           = False
        self.video            = True
        self.stream           = None
        self.frame_ratio      = 0
        self.frame_drop       = 0
        self.eos              = False
        # Stream configuration
        self.frame_width      = None
        self.frame_height     = None
        self.frame_color      = None
        self.frame_rate       = None


    def _setMode(self, mode):
        """
        Set the stream mode to input (camera/file) or output (display/file).

        Args:
            mode: The I/O mode (input or output).
        """
        mode_valid = False

        if mode == MODE_VIDEO_INPUT:
            self.mode = MODE_VIDEO_INPUT
            logger.info("_setMode: set stream mode to Input")
            mode_valid = True

        elif mode == MODE_VIDEO_OUTPUT:
            self.mode = MODE_VIDEO_OUTPUT
            logger.info("_setMode: set stream mode to Output")
            mode_valid = True

        else:
            self.mode = MODE_VIDEO_NONE
            logger.error("_setMode: invalid mode")

        return mode_valid

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
            self.device = self._scan_video_devices()
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
        if ext not in video_file_extensions + image_file_extensions:
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

        if self.mode == MODE_VIDEO_INPUT:
            # Check if the file exists
            if Path(file_path).exists():
                # File exists
                filename_valid = True
            else:
                logger.error(f"_setFilename: file does not exist: {file_path}")

        if self.mode == MODE_VIDEO_OUTPUT:
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

    def _configureStream(self, frame_width, frame_height, frame_rate, frame_color):
        """
        Configure the video stream parameters.

        Args:
            frame_width: The desired frame width in pixels.
            frame_height: The desired frame height in pixels.
            frame_rate: The desired frame rate in frames per second.
            frame_color: The desired frame color space (one of the defined constants).
        Returns:
            configuration_valid: True if the configuration is valid and set, False otherwise.
        """
        logger.debug(f"_configureStream: frame_width={frame_width}, frame_height={frame_height}, frame_rate={frame_rate}, frame_color={frame_color}")

        if (frame_width == 0 or frame_height == 0 or frame_rate == 0):
            logger.error(f"_configureStream: invalid argument (width={frame_width}, height={frame_height}, rate={frame_rate})")
            return False
        if frame_color not in (self.GRAYSCALE8, self.RGB888, self.BGR565, self.YUV420, self.NV12, self.NV21):
            logger.error(f"_configureStream: invalid argument (color={frame_color})")
            return False

        self.frame_width  = frame_width
        self.frame_height = frame_height
        self.frame_rate   = frame_rate
        self.frame_color  = frame_color

        logger.info(f"_configureStream: stream configured to {self.frame_width}x{self.frame_height}, fps={self.frame_rate}, color={self.frame_color}")

        return True

    def _scan_video_devices(self):
        """
        Scan and log available video input devices.
        Returns:
            Default device index for the current mode.
        """
        logger.info("=== Available Video Devices ===")

        available_devices = []

        # Test device indices 0-1 (covers built-in webcam + external camera)
        for device_index in range(2):
            try:
                cap = cv2.VideoCapture(device_index)
                if cap.isOpened():

                    # Get device properties
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = cap.get(cv2.CAP_PROP_FPS)

                    device_info = {
                        'index': device_index,
                        'width': width,
                        'height': height,
                        'fps': fps,
                    }
                    available_devices.append(device_info)

                    logger.info(f"Device {device_index}: {width}x{height} @ {fps:.1f}fps")

                cap.release()
            except Exception as e:
                logger.error(f"Error accessing device {device_index}: {e}")

        if not available_devices:
            logger.warning("No video devices found")
            return -1
        else:
            logger.info(f"Found {len(available_devices)} input device(s)")
            logger.info(f"Default Input Device: 0")

        return 0

    def _enableStream(self):
        """
        Enable the video stream for input (camera/file) or output (file/display).

        Initializes the OpenCV VideoCapture or VideoWriter as needed.
        Handles both new and existing files, and sets up frame dropping if input FPS > requested FPS.
        Returns:
            None
        """

        if self.mode != MODE_VIDEO_INPUT and self.mode != MODE_VIDEO_OUTPUT:
            logger.error("_enableStream: invalid mode")
            return

        if self.active:
            logger.info("_enableStream: stream already active")
            return

        self.eos = False
        self.frame_ratio = 0
        self.frame_drop  = 0

        if self.stream is not None:
            self.stream.release()
            self.stream = None

        if self.filename == None:
            self.video = True

        if self.video:
            if self.mode == MODE_VIDEO_INPUT:
                # Input mode: read from camera or video file
                if self.filename == None:
                    # No filename specified: use camera interface
                    logger.debug("_enableStream: use camera interface for input streaming")
                    self.stream = cv2.VideoCapture(self.device)

                    if not self.stream.isOpened():
                        logger.error("_enableStream: failed to open Camera interface")
                        return
                else:
                    # Filename specified: use video file
                    logger.debug("_enableStream: use file interface for input streaming")
                    self.stream = cv2.VideoCapture(self.filename)

                # Display stream properties
                logger.info(f"_enableStream: source stream properties: width={self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)}, height={self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)}, fps={self.stream.get(cv2.CAP_PROP_FPS)}")

                # Get the video stream FPS
                video_fps = self.stream.get(cv2.CAP_PROP_FPS)

                if video_fps > self.frame_rate:
                    self.frame_ratio = video_fps / self.frame_rate
                    logger.debug(f"_enableStream: source/target frame ratio={self.frame_ratio}")

            elif self.mode == MODE_VIDEO_OUTPUT:
                # Output mode: write to video file or display window
                if self.filename != None:
                    # Filename specified: output to file
                    logger.debug("_enableStream: output stream to a file")

                    extension = self.filename.suffix.lstrip('.').lower()
                    fourcc = cv2.VideoWriter_fourcc(*f'{video_fourcc[extension]}')

                    self.stream = cv2.VideoWriter(self.filename, fourcc, self.frame_rate, (self.frame_width, self.frame_height))
                else:
                    logger.debug("_enableStream: output stream to display window")

        self.active = True
        logger.info("_enableStream: stream enabled")

    def _disableStream(self):
        """
        Disable the video stream and release OpenCV resources.

        For input streams, saves the current frame index for resuming later.
        Returns:
            None
        """
        self.active = False
        if self.stream is not None:
            # Clean-up stream resources and invalidate object
            self.stream.release()
            self.stream = None

        logger.info("_disableStream: stream disabled")

    def __cropFrame(self, frame, target_aspect_ratio):
        """
        Crop the input frame to match the specified aspect ratio.

        Args:
            frame: The input frame (as NumPy array) to be cropped.
            aspect_ratio: The target aspect ratio (width/height).
        Returns:
            frame: The cropped frame.
        """
        logger.debug(f"__cropFrame: original_size=({frame.shape[1]}, {frame.shape[0]}), target_aspect_ratio={target_aspect_ratio}")

        # NumPY array shape is (height, width, channels)
        frame_h = frame.shape[0]
        frame_w = frame.shape[1]

        frame_aspect_ratio = frame_w / frame_h

        if frame_aspect_ratio > target_aspect_ratio:
            # Frame is wider than target -> crop left and right
            new_w = int(frame_h * target_aspect_ratio)
            left = (frame_w - new_w) // 2
            right = left + new_w
            cropped = frame[:, left:right]
        else:
            # Frame is taller than target -> crop top and bottom
            new_h = int(frame_w / target_aspect_ratio)
            top = (frame_h - new_h) // 2
            bottom = top + new_h
            cropped = frame[top:bottom, :]

        logger.debug(f"__cropFrame: cropped_size=({cropped.shape[1]}, {cropped.shape[0]})")

        return cropped

    def __resizeFrame(self, frame, target_width, target_height):
        """
        Resize the input frame to the target width and height.

        Args:
            frame: The input frame (as NumPy array) to be resized.
            target_width: The target width in pixels.
            target_height: The target height in pixels.
        Returns:
            frame: The resized frame.
        """
        logger.debug(f"__resizeFrame: original_size=({frame.shape[1]}, {frame.shape[0]}), target_size=({target_width}, {target_height})")

        try:
            frame = cv2.resize(frame, (target_width, target_height))
        except Exception as e:
            logger.error(f"Error in resizeFrame(): {e}")

        logger.debug(f"__resizeFrame: resized_size=({frame.shape[1]}, {frame.shape[0]})")

        return frame

    def __convertToBGR(self, frame):
        """
        Convert the input frame to BGR color space if needed.

        Args:
            frame: The input frame (as NumPy array) to be converted.
        Returns:
            frame: The converted frame in BGR color space.
        """
        if self.frame_color == self.RGB888:
            # Convert RGB to BGR
            logger.debug(f"__convertToBGR: converting frame from RGB to BGR")
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        elif self.frame_color == self.GRAYSCALE8:
            # Convert Grayscale to BGR
            logger.debug(f"__convertToBGR: converting frame from Grayscale to BGR")
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        elif self.frame_color == self.BGR565:
            # Convert BGR565 to BGR
            logger.debug(f"__convertToBGR: converting frame from BGR565 to BGR")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR5652BGR)
        elif self.frame_color == self.YUV420:
            # Convert YUV420 to BGR
            logger.debug(f"__convertToBGR: converting frame from YUV420 to BGR")
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_I420)
        elif self.frame_color == self.NV12:
            # Convert NV12 to BGR
            logger.debug(f"__convertToBGR: converting frame from NV12 to BGR")
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV12)
        elif self.frame_color == self.NV21:
            # Convert NV21 to BGR
            logger.debug(f"__convertToBGR: converting frame from NV21 to BGR")
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV21)

        return frame

    def __convertFromBGR(self, frame):
        """
        Convert the input BGR frame to the specified color space if needed.

        Args:
            frame: The input frame (as NumPy array in BGR color space) to be converted.
        Returns:
            frame: The converted frame in the specified color space.
        """
        if self.frame_color == self.RGB888:
            # Convert BGR to RGB
            logger.debug(f"__convertFromBGR: converting frame from BGR to RGB")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif self.frame_color == self.GRAYSCALE8:
            # Convert BGR to Grayscale
            logger.debug(f"__convertFromBGR: converting frame from BGR to Grayscale")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.frame_color == self.BGR565:
            # Convert BGR to BGR565
            logger.debug(f"__convertFromBGR: converting frame from BGR to BGR565")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)
        elif self.frame_color == self.YUV420:
            # Convert BGR to YUV420
            logger.debug(f"__convertFromBGR: converting frame from BGR to YUV420")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
        elif self.frame_color == self.NV12:
            # Convert BGR to NV12
            logger.debug(f"__convertFromBGR: converting frame from BGR to NV12")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_NV12)
        elif self.frame_color == self.NV21:
            # Convert BGR to NV21
            logger.debug(f"__convertFromBGR: converting frame from BGR to NV21")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_NV21)

        return frame

    # Read frame from source
    def _readFrame(self):
        """Read a single frame from the current video or image source.

        If the stream is not active or end-of-stream is reached, returns an empty bytearray.
        For video sources, handles frame dropping to match requested frame rate.
        For image sources, reads the image once and sets end-of-stream.
        Resizes and converts color space as needed.
        Returns:
            frame: The read frame as a bytearray, or empty if no frame is available.
        """
        frame = bytearray()

        # If the stream is not active, return empty frame
        if not self.active:
            logger.error("_readFrame: stream not active")
            return frame

        # If end-of-stream has been reached, return empty frame
        if self.eos:
            logger.debug("_readFrame: end of stream reached")
            return frame

        if self.video:
            # Video source, read frame from the video stream
            _, frame_in = self.stream.read() # Frame is numpy.ndarray, (height, width, channels), dtype=uint8

            if frame_in is not None:
                logger.debug(f"_readFrame: frame captured, size=({frame_in.shape[1]}, {frame_in.shape[0]})")

                # Handle frame dropping if input FPS > requested FPS
                if self.frame_ratio > 1:
                    # Accumulate fractional frames to drop
                    self.frame_drop += (self.frame_ratio - 1)

                    if self.frame_drop > 1:
                        logger.debug(f"_readFrame: frames to drop={self.frame_drop}")
                        drop = int(self.frame_drop // 1)

                        # Drop the required number of frames to match requested FPS
                        for i in range(drop):
                            _, _ = self.stream.read()
                        logger.debug(f"_readFrame: frames dropped={drop}")
                        self.frame_drop -= drop
                        logger.debug(f"_readFrame: frames left to drop={self.frame_drop}")
            else:
                # Frame not read, mark end-of-stream
                self.eos = True
                logger.debug("_readFrame: end of stream.")
        else:
            # For image sources, read the image once and set end-of-stream
            frame_in = cv2.imread(self.filename)
            self.eos  = True
            logger.debug("_readFrame: end of stream.")

        if frame_in is not None:
            target_width  = self.frame_width
            target_height = self.frame_height

            frame_in_width = frame_in.shape[1]
            frame_in_height = frame_in.shape[0]

            # Check the target frame size aspect ratio
            target_aspect_ratio = target_width / target_height
            frame_aspect_ratio = frame_in_width / frame_in_height

            if not np.isclose(frame_aspect_ratio, target_aspect_ratio, rtol=1e-3):
                logger.debug(f"_readFrame: frame aspect ratio {frame_aspect_ratio:.2f} does not match target {target_aspect_ratio:.2f}, cropping frame")
                frame_in = self.__cropFrame(frame_in, target_aspect_ratio)

                # Update frame size after cropping
                frame_in_width = frame_in.shape[1]
                frame_in_height = frame_in.shape[0]

            # Check the target frame size
            if (frame_in_width != target_width) or (frame_in_height != target_height):
                logger.debug(f"_readFrame: frame size ({frame_in_width}, {frame_in_height}) does not match target ({target_width}, {target_height}), resizing frame")
                frame_in = self.__resizeFrame(frame_in, target_width, target_height)

            # Convert frame color space to target color space
            frame_in = self.__convertFromBGR(frame_in)

            # Convert the frame to a bytearray for transmission
            frame = bytearray(frame_in.tobytes())

        return frame

    def _writeFrame(self, frame):
        """
        Write a frame to the output destination (file or display window).

        If filename is empty, displays the frame in a window.
        If filename is set and video mode, writes frame to video file.
        If filename is set and image mode, saves frame as image file.
        Args:
            frame: The input frame as a bytearray to be written.
        Returns:
            None
        """
        logger.debug(f"_writeFrame: frame size={len(frame)} bytes")

        # If the stream is not active, do nothing
        if not self.active:
            logger.error("_writeFrame: stream not active")
            return

        try:
            # Decode the frame from bytearray to a NumPy array
            decoded_frame = np.frombuffer(frame, dtype=np.uint8)

            # Reshape the decoded frame to match the target resolution
            decoded_frame = decoded_frame.reshape((self.frame_height, self.frame_width, 3))
            logger.debug(f"_writeFrame: decoded frame size=({decoded_frame.shape[1]}, {decoded_frame.shape[0]})")

            # Convert color space to BGR
            frame_out = self.__convertToBGR(decoded_frame)

            if self.filename == None:
                logger.debug("_writeFrame: display frame in window")
                # If no filename, display the frame in a window
                cv2.imshow(self.filename, frame_out)
                cv2.waitKey(10)
            else:
                if self.video:
                    logger.debug("_writeFrame: write frame to video file")
                    # Write frame to video file
                    self.stream.write(np.uint8(frame_out))
                else:
                    logger.debug("_writeFrame: write frame as image file")
                    # Write frame as image file
                    cv2.imwrite(self.filename, frame_out)

        except Exception as e:
            # Output exception debug information but continue
            logger.error(f"Exception in _writeFrame: {type(e).__name__}: {e}", exc_info=True)
            pass


    def run(self):
        """
        Main server loop.

        Waits for a client connection, then processes commands in a loop.
        Handles all supported commands: set filename, configure stream, enable/disable stream, read/write frames, close server.
        Sends responses or frame data as appropriate.
        """
        logger.info("Video server started")

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
                mode_valid = self._setMode(payload[0])
                conn.send(mode_valid)

            elif cmd == self.SET_DEVICE:
                device_valid = self._setDevice(payload[0])
                conn.send(device_valid)

            elif cmd == self.SET_FILENAME:
                filename_valid = self._setFilename(payload[0], payload[1])
                conn.send(filename_valid)

            elif cmd == self.STREAM_CONFIGURE:
                configuration_valid = self._configureStream(payload[0], payload[1], payload[2], payload[3])
                conn.send(configuration_valid)

            elif cmd == self.STREAM_ENABLE:
                self._enableStream()
                conn.send(self.active)

            elif cmd == self.STREAM_DISABLE:
                self._disableStream()
                conn.send(self.active)

            elif cmd == self.FRAME_READ:
                frame = self._readFrame()
                conn.send_bytes(frame)
                conn.send(self.eos)

            elif cmd == self.FRAME_WRITE:
                frame = conn.recv_bytes()
                self._writeFrame(frame)

            elif cmd == self.CLOSE_SERVER:
                self.stop()


    def stop(self):
        """
        Stop the video server.

        Releases all resources and closes any open windows.
        Returns:
            None
        """
        self._disableStream()
        if (self.mode == MODE_VIDEO_OUTPUT) and (self.filename == None):
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass
        self.listener.close()
        logger.info("Video server stopped")


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
    Parse command-line arguments for the video server (IP, port, authkey).
    Returns:
        args: The parsed command-line arguments.
    """
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=41)
    parser = argparse.ArgumentParser(formatter_class=formatter, description="VSI Video Server")

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
    Server = VideoServer((args.ip, args.port), args.authkey)
    try:
        Server.run()
    except KeyboardInterrupt:
        Server.stop()
