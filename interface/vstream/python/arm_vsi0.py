# Copyright (c) 2021-2025 Arm Limited. All rights reserved.

# Virtual Streaming Interface instance 0 Python script: Audio Input

##@addtogroup arm_vsi0_py_audio_in
#  @{
#
##@package arm_vsi0_audio_in
#Documentation for VSI Audio Input module.
#
#More details.

import logging
import wave
import os

logger = logging.getLogger(__name__)

## Set verbosity level
#verbosity = logging.DEBUG
#verbosity = logging.INFO
#verbosity = logging.WARNING
verbosity = logging.ERROR

# [debugging] Verbosity settings
level = { 10: "DEBUG",  20: "INFO",  30: "WARNING",  40: "ERROR" }
logging.basicConfig(format='Py: %(name)s : [%(levelname)s]\t%(message)s', level = verbosity)
logger.info("Verbosity level is set to " + level[verbosity])


# IRQ registers
IRQ_Status = 0

# Timer registers
Timer_Control  = 0
Timer_Interval = 0

# Timer Control register definitions
Timer_Control_Run_Msk      = 1<<0
Timer_Control_Periodic_Msk = 1<<1
Timer_Control_Trig_IRQ_Msk = 1<<2
Timer_Control_Trig_DMA_Msk = 1<<3

# DMA registers
DMA_Control = 0

# DMA Control register definitions
DMA_Control_Enable_Msk    = 1<<0
DMA_Control_Direction_Msk = 1<<1
DMA_Control_Direction_P2M = 0<<1
DMA_Control_Direction_M2P = 1<<1

# User registers
Regs = [0] * 64

STATUS      = 0  # Regs[0]
CONTROL     = 0  # Regs[1]
CHANNELS    = 0  # Regs[2]
SAMPLE_BITS = 0  # Regs[3]
SAMPLE_RATE = 0  # Regs[4]

# STATUS register definitions
STATUS_OPEN_Msk = 1<<0 # Stream Open
STATUS_DATA_Msk = 1<<1 # Data Available
STATUS_EOS_Msk  = 1<<2 # End of Stream

# User CONTROL register definitions
CONTROL_ENABLE_Msk = 1<<0 #Enable Streaming

# Data buffer
Data = bytearray()

# Global WAVE object
WAVE = None

## Open WAVE file (store object into global WAVE object)
#  @param name name of WAVE file to open
#  @return True if successfully opened, False otherwise
def openWAVE(name):
    global WAVE
    abs_path = os.path.abspath(name)
    logger.info("Open WAVE file: {}".format(abs_path))

    try:
        WAVE = wave.open(abs_path, 'rb')

        # Output WAVE file properties
        logger.info("  Number of channels: {}".format(WAVE.getnchannels()))
        logger.info("  Sample bits: {}".format(WAVE.getsampwidth() * 8))
        logger.info("  Sample rate: {}".format(WAVE.getframerate()))
        logger.info("  Number of frames: {}".format(WAVE.getnframes()))
        return True
    except FileNotFoundError:
        logger.error("WAVE file not found: {}".format(abs_path))
        WAVE = None
        return False
    except wave.Error as e:
        logger.error("Invalid WAVE file {}: {}".format(abs_path, str(e)))
        WAVE = None
        return False
    except Exception as e:
        logger.error("Error opening WAVE file {}: {}".format(abs_path, str(e)))
        WAVE = None
        return False

## Read WAVE frames (global WAVE object)
#  @param n number of frames to read
#  @return frames frames read
def readWAVE(n):
    global WAVE
    logger.info("Read WAVE frames")
    if WAVE is None:
        logger.error("No valid WAVE file is open")
        return b''
    try:
        frames = WAVE.readframes(n)
        frames_read = len(frames) // (WAVE.getnchannels() * WAVE.getsampwidth()) if frames else 0
        logger.debug("Requested {} frames, got {} frames ({} bytes)".format(n, frames_read, len(frames)))

        return frames
    except Exception as e:
        logger.error("Error reading WAVE frames: {}".format(str(e)))
        return b''

## Close WAVE file (global WAVE object)
def closeWAVE():
    global WAVE
    logger.info("Close WAVE file")
    if WAVE is not None:
        try:
            WAVE.close()

        except Exception as e:
            logger.error("Error closing WAVE file: {}".format(str(e)))
        finally:
            WAVE = None
    else:
        logger.warning("No WAVE file to close")


## Read a block of data into the global Data buffer
#  @param block_size size of block to read (in bytes)
def readDataBlock(block_size):
    global Data, STATUS
    logger.info("Read block of data into the data buffer")

    frame_size = CHANNELS * ((SAMPLE_BITS + 7) // 8)
    frames_max = block_size // frame_size
    Data = readWAVE(frames_max)

    # Check if we've reached the end of the file
    if len(Data) == 0:
        logger.warning("End of WAVE file reached - no more frames available")
        # Set EOS bit in STATUS register
        STATUS |= STATUS_EOS_Msk
        logger.debug("STATUS register updated: EOS bit set")


## Initialize
def init():
    logger.info("Python function init() called")


## Read interrupt request (the VSI IRQ Status Register)
#  @return value value read (32-bit)
def rdIRQ():
    global IRQ_Status
    logger.info("Python function rdIRQ() called")

    value = IRQ_Status
    logger.debug("Read interrupt request: {}".format(value))

    return value


## Write interrupt request (the VSI IRQ Status Register)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrIRQ(value):
    global IRQ_Status
    logger.info("Python function wrIRQ() called")

    IRQ_Status = value
    logger.debug("Write interrupt request: {}".format(value))

    return value


## Write Timer registers (the VSI Timer Registers)
#  @param index Timer register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrTimer(index, value):
    global Timer_Control, Timer_Interval
    logger.info("Python function wrTimer() called")

    if   index == 0:
        Timer_Control = value
        logger.debug("Write Timer_Control: {}".format(value))
    elif index == 1:
        Timer_Interval = value
        logger.debug("Write Timer_Interval: {}".format(value))

    return value


## Timer event (called at Timer Overflow)
def timerEvent():
    logger.info("Python function timerEvent() called")


## Write DMA registers (the VSI DMA Registers)
#  @param index DMA register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrDMA(index, value):
    global DMA_Control
    logger.info("Python function wrDMA() called")

    if   index == 0:
        DMA_Control = value
        logger.debug("Write DMA_Control: {}".format(value))

    return value


## Read data from peripheral for DMA P2M transfer (VSI DMA)
#  @param size size of data to read (in bytes, multiple of 4)
#  @return data data read (bytearray)
def rdDataDMA(size):
    global Data, STATUS
    logger.info("Python function rdDataDMA() called")

    readDataBlock(size)

    n = min(len(Data), size)
    data = bytearray(size)
    data[0:n] = Data[0:n]
    logger.debug("Read data ({} bytes)".format(size))
    # Set DATA bit after the blocks of data is read
    STATUS |= STATUS_DATA_Msk
    logger.debug("STATUS register updated: DATA bit set")

    return data


## Write data to peripheral for DMA M2P transfer (VSI DMA)
#  @param data data to write (bytearray)
#  @param size size of data to write (in bytes, multiple of 4)
def wrDataDMA(data, size):
    global Data
    logger.info("Python function wrDataDMA() called")

    Data = data
    logger.debug("Write data ({} bytes)".format(size))

    return


## Write CONTROL register (user register)
#  @param value value to write (32-bit)
def wrCONTROL(value):
    global CONTROL, STATUS
    if ((value ^ CONTROL) & CONTROL_ENABLE_Msk) != 0:
        if (value & CONTROL_ENABLE_Msk) != 0:
            logger.info("CONTROL register updated: ENABLE bit set")
            if openWAVE('test.wav'):
                # File opened successfully, stream is open
                STATUS |= STATUS_OPEN_Msk
                logger.debug("STATUS register updated: OPEN bit set")
        else:
            logger.info("CONTROL register updated: ENABLE bit cleared")
            closeWAVE()
            # Clear OPEN, DATA, EOS status bits when stream is closed
            STATUS &= ~(STATUS_OPEN_Msk | STATUS_DATA_Msk | STATUS_EOS_Msk)
            logger.debug("STATUS register updated: OPEN, DATA, EOS bits cleared")
    CONTROL = value

## Write CHANNELS register (user register)
#  @param value value to write (32-bit)
def wrCHANNELS(value):
    global CHANNELS
    CHANNELS = value
    logger.info("CHANNELS: {}".format(value))

## Write SAMPLE_BITS register (user register)
#  @param value value to write (32-bit)
def wrSAMPLE_BITS(value):
    global SAMPLE_BITS
    SAMPLE_BITS = value
    logger.info("SAMPLE_BITS: {}".format(value))

## Write SAMPLE_RATE register (user register)
#  @param value value to write (32-bit)
def wrSAMPLE_RATE(value):
    global SAMPLE_RATE
    SAMPLE_RATE = value
    logger.info("SAMPLE_RATE: {}".format(value))

## Read STATUS register (user register)
#  @return value value read (32-bit)
def rdSTATUS():
    global STATUS
    logger.info("STATUS: {}".format(STATUS))
    value = STATUS
    # Clear DATA bit on read of STATUS register
    STATUS &= ~STATUS_DATA_Msk
    logger.debug("STATUS register updated: DATA bit cleared")
    return value

## Read user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @return value value read (32-bit)
def rdRegs(index):
    global Regs
    logger.info("Python function rdRegs() called")

    if index == 0:
        value = rdSTATUS()
    else:
        value = Regs[index]

    logger.debug("Read user register at index {}: {}".format(index, value))

    return value


## Write user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrRegs(index, value):
    global Regs
    logger.info("Python function wrRegs() called")

    if   index == 1:
        wrCONTROL(value)
    elif index == 2:
        wrCHANNELS(value)
    elif index == 3:
        wrSAMPLE_BITS(value)
    elif index == 4:
        wrSAMPLE_RATE(value)

    Regs[index] = value
    logger.debug("Write user register at index {}: {}".format(index, value))

    return value


## @}

