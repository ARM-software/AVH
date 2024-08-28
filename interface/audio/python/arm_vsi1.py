# Copyright (c) 2021-2024 Arm Limited. All rights reserved.

# Virtual Streaming Interface instance 1 Python script: Audio Output

##@addtogroup arm_vsi1_py_audio_out
#  @{
#
##@package arm_vsi1_audio_out
#Documentation for VSI Audio Output module.
#
#More details.

import logging
import wave

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

CONTROL     = 0  # Regs[0]
CHANNELS    = 0  # Regs[1]
SAMPLE_BITS = 0  # Regs[2]
SAMPLE_RATE = 0  # Regs[3]

# User CONTROL register definitions
CONTROL_ENABLE_Msk = 1<<0

# Data buffer
Data = bytearray()


## Open WAVE file (store object into global WAVE object)
#  @param name name of WAVE file to open
def openWAVE(name):
    global WAVE
    logger.info("Open WAVE file (write mode): {}".format(name))
    WAVE = wave.open(name, 'wb')
    WAVE.setnchannels(CHANNELS)
    WAVE.setsampwidth((SAMPLE_BITS + 7) // 8)
    WAVE.setframerate(SAMPLE_RATE)
    logger.info("  Number of channels: {}".format(CHANNELS))
    logger.info("  Sample bits: {}".format(SAMPLE_BITS))
    logger.info("  Sample rate: {}".format(SAMPLE_RATE))

## Write WAVE frames (global WAVE object)
#  @param frames frames to write
def writeWAVE(frames):
    global WAVE
    logger.info("Write WAVE frames")
    WAVE.writeframes(frames)

## Close WAVE file (global WAVE object)
def closeWAVE():
    global WAVE
    logger.info("Close WAVE file")
    WAVE.close()


## Store audio frames from global Data buffer
#  @param block_size size of block to store (in bytes)
def storeAudioFrames(block_size):
    global Data
    logger.info("Store audio frames from data buffer")
    writeWAVE(Data)


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
    global Data
    logger.info("Python function rdDataDMA() called")

    n = min(len(Data), size)
    data = bytearray(size)
    data[0:n] = Data[0:n]
    logger.debug("Read data ({} bytes)".format(size))

    return data


## Write data to peripheral for DMA M2P transfer (VSI DMA)
#  @param data data to write (bytearray)
#  @param size size of data to write (in bytes, multiple of 4)
def wrDataDMA(data, size):
    global Data
    logger.info("Python function wrDataDMA() called")

    Data = data
    logger.debug("Write data ({} bytes)".format(size))

    storeAudioFrames(size)

    return


## Write CONTROL register (user register)
#  @param value value to write (32-bit)
def wrCONTROL(value):
    global CONTROL
    if ((value ^ CONTROL) & CONTROL_ENABLE_Msk) != 0:
        if (value & CONTROL_ENABLE_Msk) != 0:
            logger.info("Enable Transmitter")
            openWAVE('test.wav')
        else:
            logger.info("Disable Transmitter")
            closeWAVE()
    CONTROL = value

## Write CHANNELS register (user register)
#  @param value value to write (32-bit)
def wrCHANNELS(value):
    global CHANNELS
    CHANNELS = value
    logger.info("Number of channels: {}".format(value))

## Write SAMPLE_BITS register (user register)
#  @param value value to write (32-bit)
def wrSAMPLE_BITS(value):
    global SAMPLE_BITS
    SAMPLE_BITS = value
    logger.info("Sample bits: {}".format(value))

## Write SAMPLE_RATE register (user register)
#  @param value value to write (32-bit)
def wrSAMPLE_RATE(value):
    global SAMPLE_RATE
    SAMPLE_RATE = value
    logger.info("Sample rate: {}".format(value))


## Read user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @return value value read (32-bit)
def rdRegs(index):
    global Regs
    logger.info("Python function rdRegs() called")

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

    if   index == 0:
        wrCONTROL(value)
    elif index == 1:
        wrCHANNELS(value)
    elif index == 2:
        wrSAMPLE_BITS(value)
    elif index == 3:
        wrSAMPLE_RATE(value)

    Regs[index] = value
    logger.debug("Write user register at index {}: {}".format(index, value))

    return value


## @}

