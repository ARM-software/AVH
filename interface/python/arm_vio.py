# Copyright (c) 2021-2022 Arm Limited. All rights reserved.

# Virtual Streaming Interface instance 0 Python script

##@addtogroup arm_vio_py
#  @{
#
##@package arm_vio
#Documentation for VIO peripherals module.
#
#More details.

import logging

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


# VIO Signals
SignalOut = 0
SignalIn  = 0

# VIO Values
Values = [0] * 64


## Initialize
#  @return None
def init():
    logger.info("Python function init() called")


## Read Signal
#  @param mask bit mask of signals to read
#  @return signal signal value read
def rdSignal(mask):
    global SignalIn
    logger.info("Python function rdSignal() called")

    signal = SignalIn & mask
    logger.debug("Read signal: {}, mask: {}".format(signal, mask))

    return signal


## Write Signal
#  @param mask bit mask of signals to write
#  @param signal signal value to write
#  @return None
def wrSignal(mask, signal):
    global SignalOut
    logger.info("Python function wrSignal() called")

    SignalOut &= ~mask
    SignalOut |=  mask & signal
    logger.debug("Write signal: {}, mask: {}".format(signal, mask))

    return


## Read Value
#  @param index value index (zero based)
#  @return value value read (32-bit)
def rdValue(index):
    global Values
    logger.info("Python function rdValue() called")

    value = Values[index]
    logger.debug("Read value at index {}: {}".format(index, value))

    return value


## Write Value
#  @param index value index (zero based)
#  @param value value to write (32-bit)
#  @return None
def wrValue(index, value):
    global Values
    logger.info("Python function wrValue() called")

    Values[index] = value
    logger.debug("Write value at index {}: {}".format(index, value))

    return


## @}

