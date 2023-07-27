# Copyright (c) 2022 Arm Limited. All rights reserved.
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

# Python VSI sensor module


import logging
from os import path
from struct import unpack


class RecordManager:
    def __init__(self):
        self.WINDOW_SIZE        = 10000 #ms
        self.SLIDE_INTERVAL     = 1000  #ms
        self.HEADER_SIZE        = 8     #B
        self.TIMESTAMP_SIZE     = 4     #B
        self.data_buff          = bytearray()
        self.timestamp          = []
        self.data_size          = []
        self.interval           = 0
        self.window             = 0
        self.cnt                = 0
        self.cnt_old            = 0
        self.elapsed_time       = 0
        self.timer_event_cnt    = 0
        self.initial_interval   = 0
        self.active_record_size = 0

    # Flush variables
    def flush(self):
        logging.info("Flush Record Data")
        self.data_buff          = bytearray()
        self.timestamp          = []
        self.data_size          = []
        self.interval           = 0
        self.window             = 0
        self.cnt                = 0
        self.cnt_old            = 0
        self.elapsed_time       = 0
        self.timer_event_cnt    = 0
        self.initial_interval   = 0
        self.active_record_size = 0

    # Read one Record from data file and save acquired data in corresponding buffers
    def __getRecord(self):
        logging.info("Get Record Data")
        data = readFile(self.HEADER_SIZE)
        if len(data) == self.HEADER_SIZE:
            self.timestamp.append(unpack("I", data[:self.TIMESTAMP_SIZE])[0])
            self.data_size.append(unpack("I", data[self.TIMESTAMP_SIZE:])[0])
            self.data_buff.extend(readFile(self.data_size[-1]))
            logging.debug(f"Record Data size: {len(self.data_buff)}")
        else:
            logging.info("No Record")

    # Extract requested number of bytes from data buffer
    # If end of file is reached, return requested number of zeroes
    def getData(self, size):
        logging.info("Get Data from Record")

        if len(self.data_buff) == 0:
            self.__getRecord()

        if len(self.data_buff) >= size:
            data = self.data_buff[:size]
            self.data_buff = self.data_buff[size:]
            logging.debug(f"Requested Data size: {size}")

            if self.active_record_size == 0:
                self.active_record_size = self.data_size[self.cnt]
                self.cnt += 1
            self.active_record_size -= size
        else:
            logging.info("No Data in Record")
            data = bytearray(size)

        return data

    # Read data file until current and last timestamp are at least WINDOW_SIZE apart
    # or end of file is reached
    def __getWindow(self):
        window = 0
        old_timestamp_num = 0
        logging.info("Get Time window")
        while True:
            if len(self.timestamp) == 0:
                self.__getRecord()

            if len(self.timestamp) == old_timestamp_num:
                break
            else:
                old_timestamp_num = len(self.timestamp)

            t0 = self.timestamp[self.cnt]
            t1 = self.timestamp[-1]
            window = t1 - t0
            if window >= self.WINDOW_SIZE:
                break
            else:
                self.__getRecord()

        self.window = window
        logging.debug(f"Window size: {self.window} ms")

    # Calculate average interval based on number of samples/blocks in current time window
    def __getInterval(self):
        logging.info("Calculate new Interval")
        if (CONTROL & CONTROL_DMA_Msk) != 0:
            size = FIFO_SIZE
        else:
            size = SAMPLE_SIZE

        num = int(sum(self.data_size[self.cnt:-1])/size)

        if num > 0:
            self.interval = round((self.window * 1000)/num)
            logging.debug(f"Number of Samples/Blocks: {num}")

            # Compensate for time drift
            record_elapsed_time = (self.timestamp[self.cnt] - self.timestamp[0]) * 1000
            if self.elapsed_time != record_elapsed_time:
                interval_correction = round((self.elapsed_time - record_elapsed_time)/num)
                self.interval -= interval_correction #us
        else:
            self.interval = 0

    # Calculate new average timer interval when current record timestamp is at least
    # SLIDE_INTERVAL ahead of last timestamp used for updating the timer
    def updateTimer(self, interval):
        logging.info("Update AVH TimerEvent interval")
        if len(self.timestamp) > self.cnt:
            time_delta = self.timestamp[self.cnt] - self.timestamp[self.cnt_old]
        elif len(self.timestamp) == 0:
            time_delta = self.SLIDE_INTERVAL
        else:
            time_delta = 0

        if time_delta >= self.SLIDE_INTERVAL:
            self.__getWindow()
            self.__getInterval()
            self.cnt_old = self.cnt

        if self.timer_event_cnt == 0:
            self.initial_interval = interval
        if self.interval > 0:
            interval = self.interval

        return interval

    # Track AVH time based on timerEvent() calls and current interval setting
    def trackTime(self):
        if self.timer_event_cnt < 2:
            # Initial interval is used for first two timerEvent() calls
            self.elapsed_time += self.initial_interval
            self.timer_event_cnt += 1
        else:
            self.elapsed_time += self.interval


class FifoBuff:
    def __init__(self, buff_size, threshold_size):
        self.data           = bytearray(buff_size)
        self.buff_size      = buff_size
        self.threshold_size = threshold_size
        self.threshold      = 0
        self.idx_put        = 0
        self.idx_get        = 0
        self.count          = 0

    def put(self, byte):
        logging.info("Put byte in FIFO")

        # Check if buffer is already full
        if self.count == self.buff_size:
            logging.info("FIFO is full")
            return None
        else:
            self.data[self.idx_put] = byte
            logging.debug(f"Byte {byte} inserted at position {self.idx_put}")
            self.idx_put = (self.idx_put + 1) % self.buff_size
            self.count += 1
            if (self.count >= self.threshold_size) and (self.threshold_size != 0):
                self.threshold = 1
            return byte

    def get(self):
        logging.info("Get byte from FIFO")

        # Check if buffer is already empty
        if self.count == 0:
            logging.info("FIFO is empty")
            return None
        else:
            byte = self.data[self.idx_get]
            logging.debug(f"Byte {byte} extracted from position {self.idx_get}")
            self.idx_get = (self.idx_get + 1) % self.buff_size
            self.count -= 1
            if self.count < self.threshold_size:
                self.threshold = 0
            return byte


# User registers
REG_IDX_MAX       = 9     # Maximum user register index used in VSI
CONTROL           = 0     #Regs[0] // Control: 1=Enabled, 0=Disabled
STATUS            = 0     #Regs[1] // Status: Bit0=Overflow
SENSOR_NAME_LEN   = 0     #Regs[2] // Sensor name length
SENSOR_NAME_CHAR  = 0     #Regs[3] // Sensor name character
SENSOR_NAME_VALID = 0     #Regs[4] // Sensor name valid flag
SAMPLE_SIZE       = 1     #Regs[5] // Sample size in bytes
SAMPLE_COUNT      = 0     #Regs[6] // Sample data count
SAMPLE_PORT       = 0     #Regs[7] // Sample data port
DATA_THRESHOLD    = 0     #Regs[8] // Data event threshold in number of samples
FIFO_SIZE         = 1     #Regs[9] // Sample FIFO size in bytes

# User CONTROL register definitions
CONTROL_ENABLE_Msk = 1<<0
CONTROL_DMA_Msk    = 1<<1

# Status register definitions
STATUS_OVERFLOW_Msk  = 1<<0

# IRQ status register definitions
IRQ_Status_Threshold_Msk = 1<<0
IRQ_Status_Overflow_Msk  = 1<<1

# Filename variables
sensor_filename = ""
sensor_name_idx = 0
sensor_idx      = 0

# FIFO buffer
FIFO = FifoBuff(1, 0)

# Record manager
Record = RecordManager()

## Open sensor recording file
#  @param name name of file to open
def openFile(name):
    global file

    logging.info(f"Open recording file (read mode): {name}")
    try:
        file = open(f"{name}", "rb")
    except Exception as e:
        logging.info(f"An error occurred when trying to open recording: {e}")


## Read data bytes from sensor recording file
#  @param n_bytes number of bytes to read
#  @return data
def readFile(n_bytes):
    global file

    try:
        logging.info("Read recording file")
        data = bytearray(file.read(n_bytes))
    except Exception as e:
        logging.debug(f"An error occurred when reading n_bytes = {n_bytes}: {e}")
        data = bytearray()

    return data


## Close sensor recording file
def closeFile():
    global file

    try:
        logging.info("Close recording file")
        file.close()
    except Exception as e:
        logging.info(f"An error occurred when closing SDS file: {e}")


## VSI IRQ Status register
# @param IRQ_Status IRQ status register to update
# @param value status bits to clear
# @return IRQ_Status return updated register
def wrIRQ(IRQ_Status, value):
    IRQ_Status_Clear = IRQ_Status & ~value
    IRQ_Status &= ~IRQ_Status_Clear

    return IRQ_Status


## Write VSI Timer Register
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrTimerInterval(value):
    if (CONTROL & CONTROL_ENABLE_Msk) != 0:
        value = Record.updateTimer(value)
    return value


## Timer Event
# @param IRQ_Status IRQ status register to update
# @return IRQ_Status return updated register
def timerEvent(IRQ_Status):
    global STATUS

    Record.trackTime()
    if (CONTROL & CONTROL_DMA_Msk) == 0:
        data = Record.getData(SAMPLE_SIZE)
        for b in range(SAMPLE_SIZE):
            byte = FIFO.put(data[b])
            if byte is None:
                STATUS |= STATUS_OVERFLOW_Msk
                IRQ_Status |= IRQ_Status_Overflow_Msk
                logging.debug("Overflow detected")
                break

        if FIFO.threshold:
            IRQ_Status |= IRQ_Status_Threshold_Msk
            logging.debug("Threshold event")
    else:
        IRQ_Status |= IRQ_Status_Threshold_Msk
        logging.debug("DMA Threshold event")

    return IRQ_Status


## Read data from peripheral for DMA P2M transfer (VSI DMA)
#  @param size size of data to read (in bytes, multiple of 4)
#  @return data data read (bytearray)
def rdDataDMA(size):
    data = Record.getData(size)

    return data


## Write CONTROL register (user register)
#  @param value value to write (32-bit)
def wrCONTROL(value):
    global CONTROL, STATUS, FIFO, sensor_idx

    if ((value ^ CONTROL) & CONTROL_ENABLE_Msk) != 0:
        STATUS = 0
        Record.flush()
        if (value & CONTROL_ENABLE_Msk) != 0:
            logging.info("Enable Sensor")
            if SENSOR_NAME_VALID:
                openFile(f"{sensor_filename}.{sensor_idx}.sds")
            if (value & CONTROL_DMA_Msk) == 0:
                FIFO = FifoBuff(((FIFO_SIZE // SAMPLE_SIZE) * SAMPLE_SIZE), (DATA_THRESHOLD * SAMPLE_SIZE))
            sensor_idx += 1
        else:
            logging.info("Disable sensor")
            if SENSOR_NAME_VALID:
                closeFile()

    CONTROL = value


## Read STATUS register (user register)
# @return current_status current STATUS User register (32-bit)
def rdSTATUS():
    global STATUS

    current_status = STATUS
    STATUS &= ~STATUS_OVERFLOW_Msk

    return current_status


## Write SENSOR_NAME_LEN register (user register)
#  @param value value to write (32-bit)
def wrSENSOR_NAME_LEN(value):
    global SENSOR_NAME_LEN, SENSOR_NAME_VALID, sensor_filename, sensor_name_idx

    logging.info("Set new sensor name length and reset filename and valid flag")
    sensor_name_idx = 0
    sensor_filename = ""
    SENSOR_NAME_VALID = 0
    SENSOR_NAME_LEN = value


## Write SENSOR_NAME_CHAR register (user register)
#  @param value value to write (32-bit)
def wrSENSOR_NAME_CHAR(value):
    global SENSOR_NAME_VALID, sensor_filename, sensor_name_idx

    if sensor_name_idx < SENSOR_NAME_LEN:
        logging.info(f"Append {value} to filename")
        sensor_filename += f"{value}"
        sensor_name_idx += 1
        logging.debug(f"Received {sensor_name_idx} of {SENSOR_NAME_LEN} characters")

    if sensor_name_idx == SENSOR_NAME_LEN:
        logging.info("Check if file exists and set VALID flag")
        logging.debug(f"Filename: {sensor_filename}.{sensor_idx}.sds")
        if path.isfile(f"{sensor_filename}.{sensor_idx}.sds"):
            SENSOR_NAME_VALID = 1
        else:
            SENSOR_NAME_VALID = 0
        logging.debug(f"Filename VALID: {SENSOR_NAME_VALID}")


## Read SAMPLE_COUNT register (user register)
# @return SAMPLE_COUNT number of samples stored in FIFO (32-bit)
def rdSAMPLE_COUNT():
    global SAMPLE_COUNT

    logging.debug(f"Fifo Count: {FIFO.count}")
    SAMPLE_COUNT = FIFO.count // SAMPLE_SIZE

    return SAMPLE_COUNT


## Read SAMPLE_PORT register (user register)
# @return data data read from FIFO buffer (32-bit)
def rdSAMPLE_PORT():
    data = FIFO.get()
    if data is None:
        data = 0

    return data


## Read user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @return value value read (32-bit)
def rdRegs(index):
    value = 0

    if index == 0:
        value = CONTROL
    elif index == 1:
        value = rdSTATUS()
    elif index == 2:
        value = SENSOR_NAME_LEN
    elif index == 3:
        value = SENSOR_NAME_CHAR
    elif index == 4:
        value = SENSOR_NAME_VALID
    elif index == 5:
        value = SAMPLE_SIZE
    elif index == 6:
        value = rdSAMPLE_COUNT()
    elif index == 7:
        value = rdSAMPLE_PORT()
    elif index == 8:
        value = DATA_THRESHOLD
    elif index == 9:
        value = FIFO_SIZE

    return value


## Write user registers (the VSI User Registers)
#  @param index user register index (zero based)
#  @param value value to write (32-bit)
#  @return value value written (32-bit)
def wrRegs(index, value):
    global SAMPLE_SIZE, DATA_THRESHOLD, FIFO_SIZE

    if index == 0:
        wrCONTROL(value)
    elif index == 1:
        value = STATUS
    elif index == 2:
        wrSENSOR_NAME_LEN(value)
    elif index == 3:
        wrSENSOR_NAME_CHAR(chr(value))
    elif index == 4:
        value = SENSOR_NAME_VALID
    elif index == 5:
        if value == 0:
            value = 1
        SAMPLE_SIZE = value
    elif index == 6:
        value = SAMPLE_COUNT
    elif index == 7:
        value = SAMPLE_PORT
    elif index == 8:
        if value == 0:
            value = 1
        DATA_THRESHOLD = value
    elif index == 9:
        if value == 0:
            value = 1
        FIFO_SIZE = value

    return value
