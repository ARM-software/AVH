# Copyright (c) 2021-2025 Arm Limited. All rights reserved.

# Virtual Streaming Interface instance 4 Python script

##@addtogroup arm_vsi_py_video
#  @{
#
##@package arm_vsi4_video
#Documentation for VSI peripherals module.
#
#More details.

import logging
import vsi_video

logger = logging.getLogger(__name__)
vsi_video.logger = logger

## Set verbosity level
#verbosity = logging.DEBUG
#verbosity = logging.INFO
#verbosity = logging.WARNING
verbosity = logging.ERROR

# [debugging] Verbosity settings
level = { 10: "DEBUG",  20: "INFO",  30: "WARNING",  40: "ERROR" }
logging.basicConfig(format='Py: %(name)s : [%(levelname)s]\t%(message)s', level = verbosity)
logger.info("Verbosity level is set to " + level[verbosity])


# Video Server configuration
server_address = ('127.0.0.1', 6000)
server_authkey = 'vsi_video'


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

# Data buffer
Data = bytearray()

# Streaming Server Connection Status
Server_Connected = False



## Initialize
#  @return None
def init():
    global Server_Connected
    logger.info("init() called")

    Server_Connected = vsi_video.init(server_address, server_authkey)


## Read interrupt request (the VSI IRQ Status Register)
#  @return value value read (32-bit)
def rdIRQ():
    global IRQ_Status
    logger.info("rdIRQ() called")

    value = IRQ_Status
    logger.debug(f"Read IRQ_Status: 0x{value:08X}")

    return value


## Write interrupt request (the VSI IRQ Status Register)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrIRQ(value):
    global IRQ_Status
    logger.info(f"wrIRQ(value=0x{value:08X}) called")

    IRQ_Status = value
    logger.debug(f"wrIRQ: write IRQ_Status: 0x{value:08X}")

    return value


## Write Timer registers (the VSI Timer Registers)
#  @param index Timer register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrTimer(index, value):
    global Timer_Control, Timer_Interval
    logger.info(f"wrTimer(index={index}, value=0x{value:08X}) called")

    if   index == 0:
        Timer_Control = value
        logger.debug(f"wrTimer: write Timer_Control: 0x{value:08X}")
    elif index == 1:
        Timer_Interval = value
        logger.debug(f"wrTimer: write Timer_Interval: 0x{value:08X}")

    return value


## Timer event (called at Timer Overflow)
#  @return None
def timerEvent():
    logger.info("timerEvent() called")

    if Server_Connected:
        vsi_video.timerEvent()


## Write DMA registers (the VSI DMA Registers)
#  @param index DMA register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrDMA(index, value):
    global DMA_Control
    logger.info(f"wrDMA(index={index}, value=0x{value:08X}) called")

    if   index == 0:
        DMA_Control = value
        logger.debug(f"wrDMA: write DMA_Control: 0x{value:08X}")

    return value


## Read data from peripheral for DMA P2M transfer (VSI DMA)
#  @param size size of data to read (in bytes, multiple of 4)
#  @return data data read (bytearray)
def rdDataDMA(size):
    global Data
    logger.info(f"rdDataDMA(size={size}) called")

    if Server_Connected:
        Data = vsi_video.rdDataDMA(size)

    n = min(len(Data), size)
    data = bytearray(size)
    data[0:n] = Data[0:n]
    logger.debug(f"rdDataDMA: read data ({size} bytes)")

    return data


## Write data to peripheral for DMA M2P transfer (VSI DMA)
#  @param data data to write (bytearray)
#  @param size size of data to write (in bytes, multiple of 4)
#  @return None
def wrDataDMA(data, size):
    global Data
    logger.info(f"wrDataDMA(data={type(data).__name__}, size={size}) called")

    Data = data
    logger.debug(f"wrDataDMA: write data ({size} bytes)")

    if Server_Connected:
        vsi_video.wrDataDMA(data, size)

    return


## Read user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @return value value read (32-bit)
def rdRegs(index):
    global Regs
    logger.info(f"rdRegs(index={index}) called")

    if Server_Connected:
        Regs[index] = vsi_video.rdRegs(index)

    value = Regs[index]

    # Log the value read from the register
    logger.debug(f"rdRegs: read Regs[{index}]: 0x{value:08X}")

    return value


## Write user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrRegs(index, value):
    global Regs
    logger.info(f"wrRegs(index={index}, value=0x{value:08X}) called")

    if Server_Connected:
        value = vsi_video.wrRegs(index, value)

    Regs[index] = value

    # Log the value written to the register
    logger.debug(f"wrRegs: write Regs[{index}] = 0x{value:08X}")

    return value


## @}
