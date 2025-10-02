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

# Python VSI Video Client module
# This module provides a client interface for communicating with a VSI (Virtual Streaming Interface) video server.
# It allows configuration, streaming, and frame transfer operations for video data, typically used in hardware simulation or testing environments.

try:
    import time
    import atexit
    import logging
    import subprocess
    from multiprocessing.connection import Client, Connection
    from os import path, getcwd
    from os import name as os_name
except ImportError as err:
    print(f"VSI:Video:ImportError: {err}")
    raise
except Exception as e:
    print(f"VSI:Video:Exception: {type(e).__name__}")
    raise

logger = logging.getLogger(__name__)


class VideoClient:
    """
    Client for communicating with the VSI video server using Python's multiprocessing connection.
    Provides methods to configure the stream, send/receive frames, and control the server.
    """
    def __init__(self):
        # Server command codes
        self.SET_MODE         = 1
        self.SET_FILENAME     = 2
        self.STREAM_CONFIGURE = 3
        self.STREAM_ENABLE    = 4
        self.STREAM_DISABLE   = 5
        self.FRAME_READ       = 6
        self.FRAME_WRITE      = 7
        self.CLOSE_SERVER     = 8
        # Color space codes
        self.GRAYSCALE8       = 0
        self.RGB888           = 1
        self.BGR565           = 2
        self.YUV420           = 3
        self.NV12             = 4
        self.NV21             = 5
        # Connection object
        self.conn = None

    def connectToServer(self, address, authkey):
        """
        Attempt to connect to the VSI video server at the given address with the provided authkey.

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
        Set the mode of the video stream (input/output).
        Args:
            mode: 0 for input, 1 for output.
        Returns:
            True if the mode is valid, False otherwise.
        """
        self.conn.send([self.SET_MODE, mode])
        mode_valid = self.conn.recv()

        return mode_valid

    def setFilename(self, filename):
        """
        Set the filename for the video stream on the server.
        Args:
            filename: The name of the file to set on the server.
        Returns:
            True if the filename is valid, False otherwise.
        """
        self.conn.send([self.SET_FILENAME, getcwd(), filename])
        filename_valid = self.conn.recv()

        return filename_valid

    def configureStream(self, frame_width, frame_height, frame_rate, color_format):
        """
        Configure the video stream parameters on the server.
        Args:
            frame_width: Width of the video frame.
            frame_height: Height of the video frame.
            frame_rate: Frame rate in frames per second.
            color_format: Color format code.
        Returns:
            True if configuration is valid, False otherwise.
        """
        self.conn.send([self.STREAM_CONFIGURE, frame_width, frame_height, frame_rate, color_format])
        configuration_valid = self.conn.recv()

        return configuration_valid

    def enableStream(self):
        """
        Enable the video stream on the server in the specified mode (input/output).
        Returns:
            `True` if the stream is active, `False` otherwise.
        """
        self.conn.send([self.STREAM_ENABLE])
        stream_active = self.conn.recv()

        return stream_active

    def disableStream(self):
        """
        Disable the video stream on the server.
        Returns:
            True if the stream is no longer active, False otherwise.
        """
        self.conn.send([self.STREAM_DISABLE])
        stream_active = self.conn.recv()

        return stream_active

    def readFrame(self):
        """
        Request a video frame from the server.
        Returns:
            tuple: (data, eos) where data is a Bytearray of frame data and eos is a Boolean indicating end-of-stream.
        """
        self.conn.send([self.FRAME_READ])
        data = self.conn.recv_bytes()
        eos  = self.conn.recv()

        return data, eos

    def writeFrame(self, data):
        """
        Send a video frame to the server.
        Args:
            data: Bytearray of frame data to write.
        Returns:
            None
        """
        self.conn.send([self.FRAME_WRITE])
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
CONTROL                   = 0   # Regs[0]  // Control: enable, mode, continuous
STATUS                    = 0   # Regs[1]  // Status: active, eos, file_name, file_valid
FILENAME                  = ""  # Regs[2]  // Filename string array
FRAME_WIDTH               = 300 # Regs[3]  // Requested frame width
FRAME_HEIGHT              = 300 # Regs[4]  // Requested frame height
FRAME_RATE                = 0   # Regs[5]  // Frame rate
FRAME_COLOR               = 0   # Regs[6]  // Frame color space
FRAME_COUNT               = 0   # Regs[7]  // Frame count


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


# Global variables for video client and filename handling
Video                     = VideoClient()



def cleanup():
    """
    Close the VSI Video Server on exit.
    Returns:
        None
    """
    Video.closeServer()


def init(address, authkey):
    """
    Initialize connection to the VSI Video Server and start the server process if not already running.
    Args:
        address: Tuple (IP, port) for the server.
        authkey: Authorization key for server connection.
    Returns:
        None
    """

    base_dir = path.dirname(__file__)
    server_path = path.join(base_dir, 'vsi_video_server.py')

    logger.info("Start video server")
    if path.isfile(server_path):
        # Start Video Server as a subprocess
        if os_name == 'nt':
            py_cmd = 'python'
        else:
            py_cmd = 'python3.9'
        cmd = f"{py_cmd} {server_path} "\
              f"--ip {address[0]} "\
              f"--port {address[1]} "\
              f"--authkey {authkey}"
        subprocess.Popen(cmd, shell=True)

        # Connect to Video Server
        Video.connectToServer(address, authkey)
        if Video.conn == None:
            logger.error("Server not connected")
    else:
        logger.error(f"Server script not found: {server_path}")

    # Register clean-up function
    atexit.register(cleanup)

    if Video.conn == None:
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
        data: Bytearray of frame data.
    """
    global STATUS, FRAME_COUNT

    if (STATUS & STATUS_ACTIVE_Msk) != 0:

        data, eos = Video.readFrame()
        if eos:
            STATUS |= STATUS_EOS_Msk
            logger.debug("rdDataDMA: STATUS register updated: EOS bit set")

        if (STATUS & STATUS_EOS_Msk) == 0:
            # No End Of Stream, increment number of frames streamed
            FRAME_COUNT += 1
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
        data: Bytearray of frame data to write.
        size: Number of bytes to write (multiple of 4).
    """
    global STATUS, FRAME_COUNT

    if (STATUS & STATUS_ACTIVE_Msk) != 0:

        Video.writeFrame(data)

        # Set DATA bit after the block of data is written
        STATUS |= STATUS_DATA_Msk
        logger.debug("wrDataDMA: STATUS register updated: DATA bit set")

        # Increment number of frames streamed
        FRAME_COUNT += 1


def wrCONTROL(value):
    """
    Write to the CONTROL register (user register).

    Args:
        value: 32-bit value to write to CONTROL register.
    """
    global CONTROL, STATUS

    if ((value ^ CONTROL) & CONTROL_MODE_Msk) != 0:
        # MODE changed
        mode_valid = Video.setMode((value & CONTROL_MODE_Msk) >> CONTROL_MODE_Pos)
        if mode_valid:
            logger.info("wrCONTROL: CONTROL register updated: MODE changed")
        else:
            # Reset Mode
            Video.setMode(0)
            value &= ~CONTROL_MODE_Msk
            logger.error("wrCONTROL: CONTROL register updated: MODE cleared")

    if ((value ^ CONTROL) & CONTROL_ENABLE_Msk) != 0:
        # ENABLE bit changed
        if (value & CONTROL_ENABLE_Msk) != 0:
            logger.info("wrCONTROL: CONTROL register updated: ENABLE bit set")

            # Configure video stream
            configuration_valid = Video.configureStream(FRAME_WIDTH, FRAME_HEIGHT, FRAME_RATE, FRAME_COLOR)
            if configuration_valid:
                # Configuration is valid, enable video stream
                server_active = Video.enableStream()

                if server_active:
                    STATUS |=  STATUS_ACTIVE_Msk
                    STATUS &= ~STATUS_EOS_Msk
                else:
                    logger.error("wrCONTROL: enable video stream failed")
            else:
                logger.error("wrCONTROL: configure video stream failed")
        else:
            logger.info("wrCONTROL: CONTROL register updated: ENABLE bit cleared")
            Video.disableStream()

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
        logger.debug("STATUS register updated: FILE_NAME and FILE_VALID bits cleared")

        FILENAME = ""
        logger.debug("FILENAME register reset")

    logger.info(f"Append {char} to filename")
    FILENAME += f"{char}"

    if char == '\0':
        # Filename is null terminated
        logger.info(f"Filename: {FILENAME}")

        STATUS |= STATUS_FILE_NAME_Msk
        logger.debug("STATUS register updated: FILE_NAME bit set")

        if Video.setFilename(FILENAME) == True:
            STATUS |= STATUS_FILE_VALID_Msk
            logger.debug("STATUS register updated: FILE_VALID bit set")
        else:
            logger.error("Filename validation failed, file not found on server")


def rdRegs(index):
    """
    Read user registers (the VSI User Registers).

    Read the value of a user register by index.
    Args:
        index: User register index (zero based)
    Returns:
        value: Value read (32-bit)
    """
    value = 0

    if   index == 0:
        value = CONTROL
    elif index == 1:
        value = rdSTATUS()
    elif index == 2:
        value = rdFILENAME()
    elif index == 3:
        value = FRAME_WIDTH
    elif index == 4:
        value = FRAME_HEIGHT
    elif index == 5:
        value = FRAME_RATE
    elif index == 6:
        value = FRAME_COLOR
    elif index == 7:
        value = FRAME_COUNT

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
    global MODE, FRAME_WIDTH, FRAME_HEIGHT, FRAME_COLOR, FRAME_RATE

    if   index == 0:
        wrCONTROL(value)
    elif index == 1:
        value = STATUS
    elif index == 2:
        wrFILENAME(value)
    elif index == 3:
        FRAME_WIDTH = value
    elif index == 4:
        FRAME_HEIGHT = value
    elif index == 5:
        FRAME_RATE = value
    elif index == 6:
        FRAME_COLOR = value
    elif index == 7:
        value = FRAME_COUNT

    return value
