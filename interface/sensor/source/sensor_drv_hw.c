/*
 * Copyright (c) 2022 Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Sensor driver for VSI (Virtual Streaming Interface) on AVH (Arm Virtual Hardware)

#include <string.h>

#include "sensor_config.h"
#include "sensor_drv.h"
#include "sensor_drv_hw.h"

#include "RTE_Components.h"
#include CMSIS_device_header


// VSI user registers
#define CONTROL                 Regs[0] // Control: 1=Enabled, 0=Disabled
#define STATUS                  Regs[1] // Status: Bit0=Overflow
#define SENSOR_NAME_LEN         Regs[2] // Sensor name length
#define SENSOR_NAME_CHAR        Regs[3] // Sensor name character
#define SENSOR_NAME_VALID       Regs[4] // Sensor name valid flag
#define SAMPLE_SIZE             Regs[5] // Sample size in bytes
#define SAMPLE_COUNT            Regs[6] // Sample data count
#define SAMPLE_PORT             Regs[7] // Sample data port
#define DATA_THRESHOLD          Regs[8] // Data event threshold in number of samples
#define FIFO_SIZE               Regs[9] // Sample FIFO size in bytes

// Control register definitions
#define CONTROL_ENABLE_Pos      0U                              // CONTROL: ENABLE Position
#define CONTROL_ENABLE_Msk      (1UL << CONTROL_ENABLE_Pos)     // CONTROL: ENABLE Mask
#define CONTROL_DMA_Pos         1U                              // CONTROL: DMA Position
#define CONTROL_DMA_Msk         (1UL << CONTROL_DMA_Pos)        // CONTROL: DMA Mask

// Status register definitions
#define STATUS_OVERFLOW_Pos     0U                              // STATUS: OVERFLOW Position
#define STATUS_OVERFLOW_Msk     (1UL << STATUS_OVERFLOW_Pos)    // STATUS: OVERFLOW Mask


// Sensor0 using VSI0
#ifdef SENSOR0_NAME

#if (SENSOR0_DMA_MODE == 0U)
#if (SENSOR0_FIFO_SIZE == 0U)
#error "Sensor0: Invalid FIFO Size!
#endif
#else
#if (SENSOR0_BLOCK_NUM == 0U) || (SENSOR0_BLOCK_SIZE == 0U)
#error "Sensor0: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_0;
static sensorEvent_t EventFunc_0 = NULL;
static uint32_t      EventMask_0 = 0U;

// Block memory
#if (SENSOR0_DMA_MODE != 0U)
static uint8_t       BlockMem_0[SENSOR0_BLOCK_NUM][SENSOR0_BLOCK_SIZE];
static uint32_t      BlockCnt_0 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI0_Handler (void);
void ARM_VSI0_Handler (void) {
  uint32_t event;

  event = ARM_VSI0->IRQ.Status;
  ARM_VSI0->IRQ.Clear = event;
  #if (SENSOR0_DMA_MODE == 0U)
    ARM_VSI0->Timer.Interval = SENSOR0_SAMPLE_INTERVAL;
  #else
    ARM_VSI0->Timer.Interval = SENSOR0_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_0 != NULL) && ((event & EventMask_0) != 0U)) {
    EventFunc_0(SensorId_0, event);
  }
}

// Initialize VSI
int32_t VSI0_Initialize (void);
int32_t VSI0_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR0_NAME);
  ARM_VSI0->SENSOR_NAME_LEN = n;
  for (p = SENSOR0_NAME ; n!= 0U; n--) {
    ARM_VSI0->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI0->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI0->Timer.Control = 0U;
  ARM_VSI0->DMA.Control   = 0U;
  ARM_VSI0->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI0->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI0->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI0_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI0_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI0_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI0_Uninitialize (void);
int32_t VSI0_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI0_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI0_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI0_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI0->Timer.Control = 0U;
  ARM_VSI0->DMA.Control   = 0U;
  ARM_VSI0->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI0->IRQ.Enable    = 0U;
  ARM_VSI0->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_0 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_0  = id;
  EventFunc_0 = event_cb;
  EventMask_0 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_0 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI0->SAMPLE_SIZE    = SENSOR0_SAMPLE_SIZE;
  #if (SENSOR0_DMA_MODE == 0U)
    ARM_VSI0->DATA_THRESHOLD = SENSOR0_DATA_THRESHOLD;
    ARM_VSI0->FIFO_SIZE      = SENSOR0_FIFO_SIZE;
    ARM_VSI0->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI0->Timer.Interval = SENSOR0_SAMPLE_INTERVAL;
    ARM_VSI0->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI0->FIFO_SIZE      = SENSOR0_BLOCK_SIZE;
    ARM_VSI0->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_0               = 0U;
    ARM_VSI0->DMA.Address    = (uint32_t)BlockMem_0;
    ARM_VSI0->DMA.BlockNum   = SENSOR0_BLOCK_NUM;
    ARM_VSI0->DMA.BlockSize  = SENSOR0_BLOCK_SIZE;
    ARM_VSI0->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI0->Timer.Interval = SENSOR0_BLOCK_INTERVAL;
    ARM_VSI0->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_0 (void) {

  #if (SENSOR0_DMA_MODE == 0U)
    ARM_VSI0->Timer.Control  = 0U;
    ARM_VSI0->CONTROL        = 0U;
  #else
    ARM_VSI0->Timer.Control  = 0U;
    ARM_VSI0->DMA.Control    = 0U;
    ARM_VSI0->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_0 (void) {
  return (ARM_VSI0->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR0_DMA_MODE == 0U)
static uint32_t ReadSamples_0 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI0->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR0_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI0->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR0_DMA_MODE != 0U)
static void * GetBlockData_0 (void) {
  void *p = NULL;

  if (ARM_VSI0->Timer.Count > BlockCnt_0) {
    p = &BlockMem_0[BlockCnt_0 & (SENSOR0_BLOCK_NUM - 1U)][0];
    BlockCnt_0++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_0 = {
  RegisterEvents_0,
  Enable_0,
  Disable_0,
  GetOverflow_0,
#if (SENSOR0_DMA_MODE == 0U)
  ReadSamples_0,
#else
  NULL,
#endif
#if (SENSOR0_DMA_MODE != 0U)
  GetBlockData_0
#else
  NULL
#endif
};

#endif


// Sensor1 using VSI1
#ifdef SENSOR1_NAME

#if (SENSOR1_DMA_MODE == 0U)
#if (SENSOR1_FIFO_SIZE == 0U)
#error "Sensor1: Invalid FIFO Size!
#endif
#else
#if (SENSOR1_BLOCK_NUM == 0U) || (SENSOR1_BLOCK_SIZE == 0U)
#error "Sensor1: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_1;
static sensorEvent_t EventFunc_1 = NULL;
static uint32_t      EventMask_1 = 0U;

// Block memory
#if (SENSOR1_DMA_MODE != 0U)
static uint8_t       BlockMem_1[SENSOR1_BLOCK_NUM][SENSOR1_BLOCK_SIZE];
static uint32_t      BlockCnt_1 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI1_Handler (void);
void ARM_VSI1_Handler (void) {
  uint32_t event;

  event = ARM_VSI1->IRQ.Status;
  ARM_VSI1->IRQ.Clear = event;
  #if (SENSOR1_DMA_MODE == 0U)
    ARM_VSI1->Timer.Interval = SENSOR1_SAMPLE_INTERVAL;
  #else
    ARM_VSI1->Timer.Interval = SENSOR1_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_1 != NULL) && ((event & EventMask_1) != 0U)) {
    EventFunc_1(SensorId_1, event);
  }
}

// Initialize VSI
int32_t VSI1_Initialize (void);
int32_t VSI1_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR1_NAME);
  ARM_VSI1->SENSOR_NAME_LEN = n;
  for (p = SENSOR1_NAME ; n!= 0U; n--) {
    ARM_VSI1->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI1->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI1->Timer.Control = 0U;
  ARM_VSI1->DMA.Control   = 0U;
  ARM_VSI1->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI1->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI1->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI1_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI1_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI1_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI1_Uninitialize (void);
int32_t VSI1_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI1_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI1_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI1_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI1->Timer.Control = 0U;
  ARM_VSI1->DMA.Control   = 0U;
  ARM_VSI1->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI1->IRQ.Enable    = 0U;
  ARM_VSI1->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_1 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_1  = id;
  EventFunc_1 = event_cb;
  EventMask_1 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_1 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI1->SAMPLE_SIZE    = SENSOR1_SAMPLE_SIZE;
  #if (SENSOR1_DMA_MODE == 0U)
    ARM_VSI1->DATA_THRESHOLD = SENSOR1_DATA_THRESHOLD;
    ARM_VSI1->FIFO_SIZE      = SENSOR1_FIFO_SIZE;
    ARM_VSI1->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI1->Timer.Interval = SENSOR1_SAMPLE_INTERVAL;
    ARM_VSI1->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI1->FIFO_SIZE      = SENSOR1_BLOCK_SIZE;
    ARM_VSI1->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_1               = 0U;
    ARM_VSI1->DMA.Address    = (uint32_t)BlockMem_1;
    ARM_VSI1->DMA.BlockNum   = SENSOR1_BLOCK_NUM;
    ARM_VSI1->DMA.BlockSize  = SENSOR1_BLOCK_SIZE;
    ARM_VSI1->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI1->Timer.Interval = SENSOR1_BLOCK_INTERVAL;
    ARM_VSI1->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_1 (void) {

  #if (SENSOR1_DMA_MODE == 0U)
    ARM_VSI1->Timer.Control  = 0U;
    ARM_VSI1->CONTROL        = 0U;
  #else
    ARM_VSI1->Timer.Control  = 0U;
    ARM_VSI1->DMA.Control    = 0U;
    ARM_VSI1->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_1 (void) {
  return (ARM_VSI1->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR1_DMA_MODE == 0U)
static uint32_t ReadSamples_1 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI1->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR1_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI1->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR1_DMA_MODE != 0U)
static void * GetBlockData_1 (void) {
  void *p = NULL;

  if (ARM_VSI1->Timer.Count > BlockCnt_1) {
    p = &BlockMem_1[BlockCnt_1 & (SENSOR1_BLOCK_NUM - 1U)][0];
    BlockCnt_1++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_1 = {
  RegisterEvents_1,
  Enable_1,
  Disable_1,
  GetOverflow_1,
#if (SENSOR1_DMA_MODE == 0U)
  ReadSamples_1,
#else
  NULL,
#endif
#if (SENSOR1_DMA_MODE != 0U)
  GetBlockData_1
#else
  NULL
#endif
};

#endif


// Sensor2 using VSI2
#ifdef SENSOR2_NAME

#if (SENSOR2_DMA_MODE == 0U)
#if (SENSOR2_FIFO_SIZE == 0U)
#error "Sensor2: Invalid FIFO Size!
#endif
#else
#if (SENSOR2_BLOCK_NUM == 0U) || (SENSOR2_BLOCK_SIZE == 0U)
#error "Sensor2: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_2;
static sensorEvent_t EventFunc_2 = NULL;
static uint32_t      EventMask_2 = 0U;

// Block memory
#if (SENSOR2_DMA_MODE != 0U)
static uint8_t       BlockMem_2[SENSOR2_BLOCK_NUM][SENSOR2_BLOCK_SIZE];
static uint32_t      BlockCnt_2 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI2_Handler (void);
void ARM_VSI2_Handler (void) {
  uint32_t event;

  event = ARM_VSI2->IRQ.Status;
  ARM_VSI2->IRQ.Clear = event;
  #if (SENSOR2_DMA_MODE == 0U)
    ARM_VSI2->Timer.Interval = SENSOR2_SAMPLE_INTERVAL;
  #else
    ARM_VSI2->Timer.Interval = SENSOR2_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_2 != NULL) && ((event & EventMask_2) != 0U)) {
    EventFunc_2(SensorId_2, event);
  }
}

// Initialize VSI
int32_t VSI2_Initialize (void);
int32_t VSI2_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR2_NAME);
  ARM_VSI2->SENSOR_NAME_LEN = n;
  for (p = SENSOR2_NAME ; n!= 0U; n--) {
    ARM_VSI2->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI2->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI2->Timer.Control = 0U;
  ARM_VSI2->DMA.Control   = 0U;
  ARM_VSI2->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI2->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI2->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI2_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI2_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI2_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI2_Uninitialize (void);
int32_t VSI2_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI2_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI2_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI2_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI2->Timer.Control = 0U;
  ARM_VSI2->DMA.Control   = 0U;
  ARM_VSI2->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI2->IRQ.Enable    = 0U;
  ARM_VSI2->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_2 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_2  = id;
  EventFunc_2 = event_cb;
  EventMask_2 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_2 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI2->SAMPLE_SIZE    = SENSOR2_SAMPLE_SIZE;
  #if (SENSOR2_DMA_MODE == 0U)
    ARM_VSI2->DATA_THRESHOLD = SENSOR2_DATA_THRESHOLD;
    ARM_VSI2->FIFO_SIZE      = SENSOR2_FIFO_SIZE;
    ARM_VSI2->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI2->Timer.Interval = SENSOR2_SAMPLE_INTERVAL;
    ARM_VSI2->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI2->FIFO_SIZE      = SENSOR2_BLOCK_SIZE;
    ARM_VSI2->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_2               = 0U;
    ARM_VSI2->DMA.Address    = (uint32_t)BlockMem_2;
    ARM_VSI2->DMA.BlockNum   = SENSOR2_BLOCK_NUM;
    ARM_VSI2->DMA.BlockSize  = SENSOR2_BLOCK_SIZE;
    ARM_VSI2->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI2->Timer.Interval = SENSOR2_BLOCK_INTERVAL;
    ARM_VSI2->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_2 (void) {

  #if (SENSOR2_DMA_MODE == 0U)
    ARM_VSI2->Timer.Control  = 0U;
    ARM_VSI2->CONTROL        = 0U;
  #else
    ARM_VSI2->Timer.Control  = 0U;
    ARM_VSI2->DMA.Control    = 0U;
    ARM_VSI2->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_2 (void) {
  return (ARM_VSI2->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR2_DMA_MODE == 0U)
static uint32_t ReadSamples_2 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI2->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR2_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI2->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR2_DMA_MODE != 0U)
static void * GetBlockData_2 (void) {
  void *p = NULL;

  if (ARM_VSI2->Timer.Count > BlockCnt_2) {
    p = &BlockMem_2[BlockCnt_2 & (SENSOR2_BLOCK_NUM - 1U)][0];
    BlockCnt_2++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_2 = {
  RegisterEvents_2,
  Enable_2,
  Disable_2,
  GetOverflow_2,
#if (SENSOR2_DMA_MODE == 0U)
  ReadSamples_2,
#else
  NULL,
#endif
#if (SENSOR2_DMA_MODE != 0U)
  GetBlockData_2
#else
  NULL
#endif
};

#endif


// Sensor3 using VSI3
#ifdef SENSOR3_NAME

#if (SENSOR3_DMA_MODE == 0U)
#if (SENSOR3_FIFO_SIZE == 0U)
#error "Sensor3: Invalid FIFO Size!
#endif
#else
#if (SENSOR3_BLOCK_NUM == 0U) || (SENSOR3_BLOCK_SIZE == 0U)
#error "Sensor3: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_3;
static sensorEvent_t EventFunc_3 = NULL;
static uint32_t      EventMask_3 = 0U;

// Block memory
#if (SENSOR3_DMA_MODE != 0U)
static uint8_t       BlockMem_3[SENSOR3_BLOCK_NUM][SENSOR3_BLOCK_SIZE];
static uint32_t      BlockCnt_3 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI3_Handler (void);
void ARM_VSI3_Handler (void) {
  uint32_t event;

  event = ARM_VSI3->IRQ.Status;
  ARM_VSI3->IRQ.Clear = event;
  #if (SENSOR3_DMA_MODE == 0U)
    ARM_VSI3->Timer.Interval = SENSOR3_SAMPLE_INTERVAL;
  #else
    ARM_VSI3->Timer.Interval = SENSOR3_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_3 != NULL) && ((event & EventMask_3) != 0U)) {
    EventFunc_3(SensorId_3, event);
  }
}

// Initialize VSI
int32_t VSI3_Initialize (void);
int32_t VSI3_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR3_NAME);
  ARM_VSI3->SENSOR_NAME_LEN = n;
  for (p = SENSOR3_NAME ; n!= 0U; n--) {
    ARM_VSI3->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI3->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI3->Timer.Control = 0U;
  ARM_VSI3->DMA.Control   = 0U;
  ARM_VSI3->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI3->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI3->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI3_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI3_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI3_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI3_Uninitialize (void);
int32_t VSI3_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI3_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI3_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI3_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI3->Timer.Control = 0U;
  ARM_VSI3->DMA.Control   = 0U;
  ARM_VSI3->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI3->IRQ.Enable    = 0U;
  ARM_VSI3->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_3 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_3  = id;
  EventFunc_3 = event_cb;
  EventMask_3 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_3 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI3->SAMPLE_SIZE    = SENSOR3_SAMPLE_SIZE;
  #if (SENSOR3_DMA_MODE == 0U)
    ARM_VSI3->DATA_THRESHOLD = SENSOR3_DATA_THRESHOLD;
    ARM_VSI3->FIFO_SIZE      = SENSOR3_FIFO_SIZE;
    ARM_VSI3->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI3->Timer.Interval = SENSOR3_SAMPLE_INTERVAL;
    ARM_VSI3->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI3->FIFO_SIZE      = SENSOR3_BLOCK_SIZE;
    ARM_VSI3->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_3               = 0U;
    ARM_VSI3->DMA.Address    = (uint32_t)BlockMem_3;
    ARM_VSI3->DMA.BlockNum   = SENSOR3_BLOCK_NUM;
    ARM_VSI3->DMA.BlockSize  = SENSOR3_BLOCK_SIZE;
    ARM_VSI3->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI3->Timer.Interval = SENSOR3_BLOCK_INTERVAL;
    ARM_VSI3->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_3 (void) {

  #if (SENSOR3_DMA_MODE == 0U)
    ARM_VSI3->Timer.Control  = 0U;
    ARM_VSI3->CONTROL        = 0U;
  #else
    ARM_VSI3->Timer.Control  = 0U;
    ARM_VSI3->DMA.Control    = 0U;
    ARM_VSI3->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_3 (void) {
  return (ARM_VSI3->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR3_DMA_MODE == 0U)
static uint32_t ReadSamples_3 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI3->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR3_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI3->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR3_DMA_MODE != 0U)
static void * GetBlockData_3 (void) {
  void *p = NULL;

  if (ARM_VSI3->Timer.Count > BlockCnt_3) {
    p = &BlockMem_3[BlockCnt_3 & (SENSOR3_BLOCK_NUM - 1U)][0];
    BlockCnt_3++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_3 = {
  RegisterEvents_3,
  Enable_3,
  Disable_3,
  GetOverflow_3,
#if (SENSOR3_DMA_MODE == 0U)
  ReadSamples_3,
#else
  NULL,
#endif
#if (SENSOR3_DMA_MODE != 0U)
  GetBlockData_3
#else
  NULL
#endif
};

#endif


// Sensor4 using VSI4
#ifdef SENSOR4_NAME

#if (SENSOR4_DMA_MODE == 0U)
#if (SENSOR4_FIFO_SIZE == 0U)
#error "Sensor4: Invalid FIFO Size!
#endif
#else
#if (SENSOR4_BLOCK_NUM == 0U) || (SENSOR4_BLOCK_SIZE == 0U)
#error "Sensor4: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_4;
static sensorEvent_t EventFunc_4 = NULL;
static uint32_t      EventMask_4 = 0U;

// Block memory
#if (SENSOR4_DMA_MODE != 0U)
static uint8_t       BlockMem_4[SENSOR4_BLOCK_NUM][SENSOR4_BLOCK_SIZE];
static uint32_t      BlockCnt_4 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI4_Handler (void);
void ARM_VSI4_Handler (void) {
  uint32_t event;

  event = ARM_VSI4->IRQ.Status;
  ARM_VSI4->IRQ.Clear = event;
  #if (SENSOR4_DMA_MODE == 0U)
    ARM_VSI4->Timer.Interval = SENSOR4_SAMPLE_INTERVAL;
  #else
    ARM_VSI4->Timer.Interval = SENSOR4_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_4 != NULL) && ((event & EventMask_4) != 0U)) {
    EventFunc_4(SensorId_4, event);
  }
}

// Initialize VSI
int32_t VSI4_Initialize (void);
int32_t VSI4_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR4_NAME);
  ARM_VSI4->SENSOR_NAME_LEN = n;
  for (p = SENSOR4_NAME ; n!= 0U; n--) {
    ARM_VSI4->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI4->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI4->Timer.Control = 0U;
  ARM_VSI4->DMA.Control   = 0U;
  ARM_VSI4->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI4->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI4->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI4_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI4_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI4_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI4_Uninitialize (void);
int32_t VSI4_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI4_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI4_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI4_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI4->Timer.Control = 0U;
  ARM_VSI4->DMA.Control   = 0U;
  ARM_VSI4->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI4->IRQ.Enable    = 0U;
  ARM_VSI4->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_4 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_4  = id;
  EventFunc_4 = event_cb;
  EventMask_4 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_4 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI4->SAMPLE_SIZE    = SENSOR4_SAMPLE_SIZE;
  #if (SENSOR4_DMA_MODE == 0U)
    ARM_VSI4->DATA_THRESHOLD = SENSOR4_DATA_THRESHOLD;
    ARM_VSI4->FIFO_SIZE      = SENSOR4_FIFO_SIZE;
    ARM_VSI4->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI4->Timer.Interval = SENSOR4_SAMPLE_INTERVAL;
    ARM_VSI4->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI4->FIFO_SIZE      = SENSOR4_BLOCK_SIZE;
    ARM_VSI4->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_4               = 0U;
    ARM_VSI4->DMA.Address    = (uint32_t)BlockMem_4;
    ARM_VSI4->DMA.BlockNum   = SENSOR4_BLOCK_NUM;
    ARM_VSI4->DMA.BlockSize  = SENSOR4_BLOCK_SIZE;
    ARM_VSI4->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI4->Timer.Interval = SENSOR4_BLOCK_INTERVAL;
    ARM_VSI4->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_4 (void) {

  #if (SENSOR4_DMA_MODE == 0U)
    ARM_VSI4->Timer.Control  = 0U;
    ARM_VSI4->CONTROL        = 0U;
  #else
    ARM_VSI4->Timer.Control  = 0U;
    ARM_VSI4->DMA.Control    = 0U;
    ARM_VSI4->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_4 (void) {
  return (ARM_VSI4->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR4_DMA_MODE == 0U)
static uint32_t ReadSamples_4 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI4->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR4_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI4->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR4_DMA_MODE != 0U)
static void * GetBlockData_4 (void) {
  void *p = NULL;

  if (ARM_VSI4->Timer.Count > BlockCnt_4) {
    p = &BlockMem_4[BlockCnt_4 & (SENSOR4_BLOCK_NUM - 1U)][0];
    BlockCnt_4++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_4 = {
  RegisterEvents_4,
  Enable_4,
  Disable_4,
  GetOverflow_4,
#if (SENSOR4_DMA_MODE == 0U)
  ReadSamples_4,
#else
  NULL,
#endif
#if (SENSOR4_DMA_MODE != 0U)
  GetBlockData_4
#else
  NULL
#endif
};

#endif


// Sensor5 using VSI5
#ifdef SENSOR5_NAME

#if (SENSOR5_DMA_MODE == 0U)
#if (SENSOR5_FIFO_SIZE == 0U)
#error "Sensor5: Invalid FIFO Size!
#endif
#else
#if (SENSOR5_BLOCK_NUM == 0U) || (SENSOR5_BLOCK_SIZE == 0U)
#error "Sensor5: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_5;
static sensorEvent_t EventFunc_5 = NULL;
static uint32_t      EventMask_5 = 0U;

// Block memory
#if (SENSOR5_DMA_MODE != 0U)
static uint8_t       BlockMem_5[SENSOR5_BLOCK_NUM][SENSOR5_BLOCK_SIZE];
static uint32_t      BlockCnt_5 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI5_Handler (void);
void ARM_VSI5_Handler (void) {
  uint32_t event;

  event = ARM_VSI5->IRQ.Status;
  ARM_VSI5->IRQ.Clear = event;
  #if (SENSOR5_DMA_MODE == 0U)
    ARM_VSI5->Timer.Interval = SENSOR5_SAMPLE_INTERVAL;
  #else
    ARM_VSI5->Timer.Interval = SENSOR5_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_5 != NULL) && ((event & EventMask_5) != 0U)) {
    EventFunc_5(SensorId_5, event);
  }
}

// Initialize VSI
int32_t VSI5_Initialize (void);
int32_t VSI5_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR5_NAME);
  ARM_VSI5->SENSOR_NAME_LEN = n;
  for (p = SENSOR5_NAME ; n!= 0U; n--) {
    ARM_VSI5->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI5->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI5->Timer.Control = 0U;
  ARM_VSI5->DMA.Control   = 0U;
  ARM_VSI5->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI5->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI5->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI5_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI5_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI5_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI5_Uninitialize (void);
int32_t VSI5_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI5_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI5_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI5_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI5->Timer.Control = 0U;
  ARM_VSI5->DMA.Control   = 0U;
  ARM_VSI5->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI5->IRQ.Enable    = 0U;
  ARM_VSI5->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_5 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_5  = id;
  EventFunc_5 = event_cb;
  EventMask_5 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_5 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI5->SAMPLE_SIZE    = SENSOR5_SAMPLE_SIZE;
  #if (SENSOR5_DMA_MODE == 0U)
    ARM_VSI5->DATA_THRESHOLD = SENSOR5_DATA_THRESHOLD;
    ARM_VSI5->FIFO_SIZE      = SENSOR5_FIFO_SIZE;
    ARM_VSI5->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI5->Timer.Interval = SENSOR5_SAMPLE_INTERVAL;
    ARM_VSI5->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI5->FIFO_SIZE      = SENSOR5_BLOCK_SIZE;
    ARM_VSI5->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_5               = 0U;
    ARM_VSI5->DMA.Address    = (uint32_t)BlockMem_5;
    ARM_VSI5->DMA.BlockNum   = SENSOR5_BLOCK_NUM;
    ARM_VSI5->DMA.BlockSize  = SENSOR5_BLOCK_SIZE;
    ARM_VSI5->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI5->Timer.Interval = SENSOR5_BLOCK_INTERVAL;
    ARM_VSI5->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_5 (void) {

  #if (SENSOR5_DMA_MODE == 0U)
    ARM_VSI5->Timer.Control  = 0U;
    ARM_VSI5->CONTROL        = 0U;
  #else
    ARM_VSI5->Timer.Control  = 0U;
    ARM_VSI5->DMA.Control    = 0U;
    ARM_VSI5->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_5 (void) {
  return (ARM_VSI5->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR5_DMA_MODE == 0U)
static uint32_t ReadSamples_5 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI5->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR5_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI5->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR5_DMA_MODE != 0U)
static void * GetBlockData_5 (void) {
  void *p = NULL;

  if (ARM_VSI5->Timer.Count > BlockCnt_5) {
    p = &BlockMem_5[BlockCnt_5 & (SENSOR5_BLOCK_NUM - 1U)][0];
    BlockCnt_5++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_5 = {
  RegisterEvents_5,
  Enable_5,
  Disable_5,
  GetOverflow_5,
#if (SENSOR5_DMA_MODE == 0U)
  ReadSamples_5,
#else
  NULL,
#endif
#if (SENSOR5_DMA_MODE != 0U)
  GetBlockData_5
#else
  NULL
#endif
};

#endif


// Sensor6 using VSI6
#ifdef SENSOR6_NAME

#if (SENSOR6_DMA_MODE == 0U)
#if (SENSOR6_FIFO_SIZE == 0U)
#error "Sensor6: Invalid FIFO Size!
#endif
#else
#if (SENSOR6_BLOCK_NUM == 0U) || (SENSOR6_BLOCK_SIZE == 0U)
#error "Sensor6: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_6;
static sensorEvent_t EventFunc_6 = NULL;
static uint32_t      EventMask_6 = 0U;

// Block memory
#if (SENSOR6_DMA_MODE != 0U)
static uint8_t       BlockMem_6[SENSOR6_BLOCK_NUM][SENSOR6_BLOCK_SIZE];
static uint32_t      BlockCnt_6 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI6_Handler (void);
void ARM_VSI6_Handler (void) {
  uint32_t event;

  event = ARM_VSI6->IRQ.Status;
  ARM_VSI6->IRQ.Clear = event;
  #if (SENSOR6_DMA_MODE == 0U)
    ARM_VSI6->Timer.Interval = SENSOR6_SAMPLE_INTERVAL;
  #else
    ARM_VSI6->Timer.Interval = SENSOR6_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_6 != NULL) && ((event & EventMask_6) != 0U)) {
    EventFunc_6(SensorId_6, event);
  }
}

// Initialize VSI
int32_t VSI6_Initialize (void);
int32_t VSI6_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR6_NAME);
  ARM_VSI6->SENSOR_NAME_LEN = n;
  for (p = SENSOR6_NAME ; n!= 0U; n--) {
    ARM_VSI6->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI6->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI6->Timer.Control = 0U;
  ARM_VSI6->DMA.Control   = 0U;
  ARM_VSI6->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI6->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI6->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI6_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI6_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI6_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI6_Uninitialize (void);
int32_t VSI6_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI6_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI6_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI6_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI6->Timer.Control = 0U;
  ARM_VSI6->DMA.Control   = 0U;
  ARM_VSI6->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI6->IRQ.Enable    = 0U;
  ARM_VSI6->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_6 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_6  = id;
  EventFunc_6 = event_cb;
  EventMask_6 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_6 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI6->SAMPLE_SIZE    = SENSOR6_SAMPLE_SIZE;
  #if (SENSOR6_DMA_MODE == 0U)
    ARM_VSI6->DATA_THRESHOLD = SENSOR6_DATA_THRESHOLD;
    ARM_VSI6->FIFO_SIZE      = SENSOR6_FIFO_SIZE;
    ARM_VSI6->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI6->Timer.Interval = SENSOR6_SAMPLE_INTERVAL;
    ARM_VSI6->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI6->FIFO_SIZE      = SENSOR6_BLOCK_SIZE;
    ARM_VSI6->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_6               = 0U;
    ARM_VSI6->DMA.Address    = (uint32_t)BlockMem_6;
    ARM_VSI6->DMA.BlockNum   = SENSOR6_BLOCK_NUM;
    ARM_VSI6->DMA.BlockSize  = SENSOR6_BLOCK_SIZE;
    ARM_VSI6->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI6->Timer.Interval = SENSOR6_BLOCK_INTERVAL;
    ARM_VSI6->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_6 (void) {

  #if (SENSOR6_DMA_MODE == 0U)
    ARM_VSI6->Timer.Control  = 0U;
    ARM_VSI6->CONTROL        = 0U;
  #else
    ARM_VSI6->Timer.Control  = 0U;
    ARM_VSI6->DMA.Control    = 0U;
    ARM_VSI6->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_6 (void) {
  return (ARM_VSI6->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR6_DMA_MODE == 0U)
static uint32_t ReadSamples_6 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI6->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR6_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI6->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR6_DMA_MODE != 0U)
static void * GetBlockData_6 (void) {
  void *p = NULL;

  if (ARM_VSI6->Timer.Count > BlockCnt_6) {
    p = &BlockMem_6[BlockCnt_6 & (SENSOR6_BLOCK_NUM - 1U)][0];
    BlockCnt_6++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_6 = {
  RegisterEvents_6,
  Enable_6,
  Disable_6,
  GetOverflow_6,
#if (SENSOR6_DMA_MODE == 0U)
  ReadSamples_6,
#else
  NULL,
#endif
#if (SENSOR6_DMA_MODE != 0U)
  GetBlockData_6
#else
  NULL
#endif
};

#endif


// Sensor7 using VSI7
#ifdef SENSOR7_NAME

#if (SENSOR7_DMA_MODE == 0U)
#if (SENSOR7_FIFO_SIZE == 0U)
#error "Sensor7: Invalid FIFO Size!
#endif
#else
#if (SENSOR7_BLOCK_NUM == 0U) || (SENSOR7_BLOCK_SIZE == 0U)
#error "Sensor7: Invalid Block Configuration!
#endif
#endif

// Registered event variables
static sensorId_t    SensorId_7;
static sensorEvent_t EventFunc_7 = NULL;
static uint32_t      EventMask_7 = 0U;

// Block memory
#if (SENSOR7_DMA_MODE != 0U)
static uint8_t       BlockMem_7[SENSOR7_BLOCK_NUM][SENSOR7_BLOCK_SIZE];
static uint32_t      BlockCnt_7 = 0U;
#endif

// VSI interrupt handler
void ARM_VSI7_Handler (void);
void ARM_VSI7_Handler (void) {
  uint32_t event;

  event = ARM_VSI7->IRQ.Status;
  ARM_VSI7->IRQ.Clear = event;
  #if (SENSOR7_DMA_MODE == 0U)
    ARM_VSI7->Timer.Interval = SENSOR7_SAMPLE_INTERVAL;
  #else
    ARM_VSI7->Timer.Interval = SENSOR7_BLOCK_INTERVAL;
  #endif
  __DSB();
  __ISB();

  if ((EventFunc_7 != NULL) && ((event & EventMask_7) != 0U)) {
    EventFunc_7(SensorId_7, event);
  }
}

// Initialize VSI
int32_t VSI7_Initialize (void);
int32_t VSI7_Initialize (void) {
  uint32_t n;
  char *p;

  // Register sensor name
  n = strlen(SENSOR7_NAME);
  ARM_VSI7->SENSOR_NAME_LEN = n;
  for (p = SENSOR7_NAME ; n!= 0U; n--) {
    ARM_VSI7->SENSOR_NAME_CHAR = *p++;
  }
  if (ARM_VSI7->SENSOR_NAME_VALID == 0U) {
    return SENSOR_ERROR;
  }

  // Initialize VSI peripheral
  ARM_VSI7->Timer.Control = 0U;
  ARM_VSI7->DMA.Control   = 0U;
  ARM_VSI7->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI7->IRQ.Enable    = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI7->CONTROL       = 0U;

  // Enable peripheral interrupts
//NVIC_EnableIRQ(ARM_VSI7_IRQn);
  NVIC->ISER[(((uint32_t)ARM_VSI7_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI7_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  return SENSOR_OK;
}

// Uninitialize VSI
int32_t VSI7_Uninitialize (void);
int32_t VSI7_Uninitialize (void) {

  // Disable peripheral interrupts
//NVIC_DisableIRQ(ARM_VSI7_IRQn);
  NVIC->ICER[(((uint32_t)ARM_VSI7_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)ARM_VSI7_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  // Uninitialize VSI peripheral
  ARM_VSI7->Timer.Control = 0U;
  ARM_VSI7->DMA.Control   = 0U;
  ARM_VSI7->IRQ.Clear     = SENSOR_EVENT_DATA | SENSOR_EVENT_OVERFLOW;
  ARM_VSI7->IRQ.Enable    = 0U;
  ARM_VSI7->CONTROL       = 0U;

  return SENSOR_OK;
}

// Register sensor events
static int32_t RegisterEvents_7 (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {

  SensorId_7  = id;
  EventFunc_7 = event_cb;
  EventMask_7 = event_mask;

  return SENSOR_OK;
}

// Enable sensor
static int32_t Enable_7 (void) {
  int32_t ret = SENSOR_ERROR;

    ARM_VSI7->SAMPLE_SIZE    = SENSOR7_SAMPLE_SIZE;
  #if (SENSOR7_DMA_MODE == 0U)
    ARM_VSI7->DATA_THRESHOLD = SENSOR7_DATA_THRESHOLD;
    ARM_VSI7->FIFO_SIZE      = SENSOR7_FIFO_SIZE;
    ARM_VSI7->CONTROL        = CONTROL_ENABLE_Msk;
    ARM_VSI7->Timer.Interval = SENSOR7_SAMPLE_INTERVAL;
    ARM_VSI7->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #else
    ARM_VSI7->FIFO_SIZE      = SENSOR7_BLOCK_SIZE;
    ARM_VSI7->CONTROL        = CONTROL_ENABLE_Msk |
                               CONTROL_DMA_Msk;
    BlockCnt_7               = 0U;
    ARM_VSI7->DMA.Address    = (uint32_t)BlockMem_7;
    ARM_VSI7->DMA.BlockNum   = SENSOR7_BLOCK_NUM;
    ARM_VSI7->DMA.BlockSize  = SENSOR7_BLOCK_SIZE;
    ARM_VSI7->DMA.Control    = ARM_VSI_DMA_Direction_P2M |
                               ARM_VSI_DMA_Enable_Msk;
    ARM_VSI7->Timer.Interval = SENSOR7_BLOCK_INTERVAL;
    ARM_VSI7->Timer.Control  = ARM_VSI_Timer_Periodic_Msk |
                               ARM_VSI_Timer_Trig_DMA_Msk |
                               ARM_VSI_Timer_Trig_IRQ_Msk |
                               ARM_VSI_Timer_Run_Msk;
    ret = SENSOR_OK;
  #endif

  return ret;
}

// Disable sensor
static int32_t Disable_7 (void) {

  #if (SENSOR7_DMA_MODE == 0U)
    ARM_VSI7->Timer.Control  = 0U;
    ARM_VSI7->CONTROL        = 0U;
  #else
    ARM_VSI7->Timer.Control  = 0U;
    ARM_VSI7->DMA.Control    = 0U;
    ARM_VSI7->CONTROL        = 0U;
  #endif

  return SENSOR_OK;
}

// Get overflow status
static uint32_t GetOverflow_7 (void) {
  return (ARM_VSI7->STATUS & STATUS_OVERFLOW_Msk);
}

// Read samples from sensor
#if (SENSOR7_DMA_MODE == 0U)
static uint32_t ReadSamples_7 (uint32_t num_samples, void *buf) {
  uint32_t num;
  uint32_t n, m;
  uint8_t *p;

  num = ARM_VSI7->SAMPLE_COUNT;
  if (num > num_samples) {
    num = num_samples;
  }

  p = (uint8_t *)buf;
  for (n = num; n != 0U; n--) {
    for (m = SENSOR7_SAMPLE_SIZE; m != 0U; m--) {
      *p++ = (uint8_t)ARM_VSI7->SAMPLE_PORT;
    }
  }

  return num;
}
#endif

// Get block data
#if (SENSOR7_DMA_MODE != 0U)
static void * GetBlockData_7 (void) {
  void *p = NULL;

  if (ARM_VSI7->Timer.Count > BlockCnt_7) {
    p = &BlockMem_7[BlockCnt_7 & (SENSOR7_BLOCK_NUM - 1U)][0];
    BlockCnt_7++;
  }

  return p;
}
#endif

// Exported sensor functions
sensorDrvHW_t sensorDrvHW_7 = {
  RegisterEvents_7,
  Enable_7,
  Disable_7,
  GetOverflow_7,
#if (SENSOR7_DMA_MODE == 0U)
  ReadSamples_7,
#else
  NULL,
#endif
#if (SENSOR7_DMA_MODE != 0U)
  GetBlockData_7
#else
  NULL
#endif
};

#endif
