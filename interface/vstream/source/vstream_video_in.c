/*---------------------------------------------------------------------------
 * Copyright (c) 2025 Arm Limited (or its affiliates).
 * All rights reserved.
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
 *---------------------------------------------------------------------------*/

#include <stdint.h>
#include <string.h>
#include "vstream_video_in.h"
#include "vstream_video_in_config.h"

#ifdef _RTE_
#include "RTE_Components.h"
#endif
#include CMSIS_device_header
#include "arm_vsi.h"

/* Peripheral definitions */
#define VideoIn                 ARM_VSI4              /* Video Input access struct     */
#define VideoIn_IRQn            ARM_VSI4_IRQn         /* Video Input Interrupt number  */
#define VideoIn_Handler         ARM_VSI4_Handler      /* Video Input Interrupt handler */

/* Peripheral registers */
#define CONTROL                 Regs[0]  /* Control: enable, mode, continuous          */
#define STATUS                  Regs[1]  /* Status: active, eos, file_name, file_valid */
#define DEVICE                  Regs[2]  /* Streaming device                           */
#define FILENAME                Regs[3]  /* Filename string array                      */
#define FRAME_WIDTH             Regs[4]  /* Requested frame width                      */
#define FRAME_HEIGHT            Regs[5]  /* Requested frame height                     */
#define FRAME_RATE              Regs[6]  /* Frame rate                                 */
#define FRAME_COLOR             Regs[7]  /* Frame color space                          */

/* CONTROL register definitions */
#define CONTROL_ENABLE_Pos      0U                             /* Cleared= Disabled, Set= Enabled  */
#define CONTROL_ENABLE_Msk      (1UL << CONTROL_ENABLE_Pos)
#define CONTROL_MODE_Pos        1U                             /* Bits 2:1                         */
#define CONTROL_MODE_Msk        (3UL << CONTROL_MODE_Pos)      /* 0= Disabled, 1= Input, 2= Output */
#define CONTROL_MODE_NONE       (0U << CONTROL_MODE_Pos)
#define CONTROL_MODE_IN         (1U << CONTROL_MODE_Pos)
#define CONTROL_MODE_OUT        (2U << CONTROL_MODE_Pos)
#define CONTROL_CONTINUOUS_Pos  3U                             /* Cleared= Single, Set= Continuous */
#define CONTROL_CONTINUOUS_Msk  (1UL << CONTROL_CONTINUOUS_Pos)

/* STATUS register definitions */
#define STATUS_ACTIVE_Pos       0U
#define STATUS_ACTIVE_Msk       (1UL << STATUS_ACTIVE_Pos)
#define STATUS_DATA_Pos         1U
#define STATUS_DATA_Msk         (1UL << STATUS_DATA_Pos)
#define STATUS_EOS_Pos          2U
#define STATUS_EOS_Msk          (1UL << STATUS_EOS_Pos)
#define STATUS_FILE_NAME_Pos    3U
#define STATUS_FILE_NAME_Msk    (1UL << STATUS_FILE_NAME_Pos)
#define STATUS_FILE_VALID_Pos   4U
#define STATUS_FILE_VALID_Msk   (1UL << STATUS_FILE_VALID_Pos)

/* IRQ_* register definitions */
#define IRQ_TIMER_OVERFLOW_Pos  0U
#define IRQ_TIMER_OVERFLOW_Msk  (1UL << IRQ_TIMER_OVERFLOW_Pos)


/* Handle Flags Definitions */
#define FLAGS_INIT              (1U << 0)
#define FLAGS_START             (1U << 1)
#define FLAGS_SINGLE            (1U << 2)
#define FLAGS_LIMIT_OWN         (1U << 3)
#define FLAGS_BUF_EMPTY         (1U << 4)
#define FLAGS_BUF_FULL          (1U << 5)

/* Stream Buffer Type Definition */
typedef struct {
  uint8_t *data;              /* Data buffer pointer             */
  uint32_t block_num;         /* Number of blocks in data buffer */
  uint32_t block_size;        /* Size of block in data buffer    */
} StreamBuf_t;

/* vStream Handle Type Definition */
typedef struct {
  vStreamEvent_t    callback; /* Callback from vStream driver                       */
  StreamBuf_t       buf;      /* Stream buffer                                      */
  volatile uint32_t idx_get;  /* Index of block to be returned on GetBlock call     */
  volatile uint32_t idx_rel;  /* Index of block to be released on ReleaseBlock call */
  volatile uint32_t idx_in;   /* Index of block currently being streamed            */
  volatile uint8_t  active;   /* Streaming active flag */
  volatile uint8_t  overflow; /* Buffer overflow flag  */
  volatile uint8_t  eos;      /* End of stream flag    */
  volatile uint8_t  flags;    /* Handle status flags   */
} StreamHandle_t;

/* vStream Handle */
static StreamHandle_t hVideoIn = {0};

/**
  \brief Video Input Interrupt Handler.
*/
void VideoIn_Handler (void) {
  uint32_t status;
  uint32_t event;

  status = VideoIn->STATUS;

  VideoIn->IRQ.Clear = IRQ_TIMER_OVERFLOW_Msk;
  __DSB();
  __ISB();

  event = 0U;

  if ((status & STATUS_DATA_Msk) != 0U) {
    /* Data block streamed in */
    event |= VSTREAM_EVENT_DATA;

    /* Get index of the block being streamed */
    hVideoIn.idx_in = VideoIn->DMA.BlockIndex;

    /* Clear buffer empty flag */
    hVideoIn.flags &= ~FLAGS_BUF_EMPTY;

    if (hVideoIn.idx_in == hVideoIn.idx_rel) {
      /* Buffer is full */
      hVideoIn.flags |= FLAGS_BUF_FULL;

      if ((hVideoIn.flags & FLAGS_SINGLE) == 0U) {
        /* Continuous mode, no free stream buffer */
        hVideoIn.overflow = 1U;

        event |= VSTREAM_EVENT_OVERFLOW;
      }
    }
  }

  if ((status & STATUS_EOS_Msk) != 0U) {
    /* End of stream */
    hVideoIn.eos = 1U;

    event |= VSTREAM_EVENT_EOS;
  }

  if ((hVideoIn.flags & FLAGS_SINGLE) != 0U) {
    /* Single mode, clear active flag */
    hVideoIn.active = 0U;
  }

  if ((hVideoIn.callback != NULL) && (event != 0U)) {
    /* Call application callback function */
    hVideoIn.callback(event);
  }
}

/* Initialize streaming interface */
static int32_t Initialize (vStreamEvent_t event_cb) {
  char *fn;
  uint32_t len;
  uint32_t i;

  hVideoIn.callback = event_cb;
  hVideoIn.active   = 0U;
  hVideoIn.overflow = 0U;
  hVideoIn.eos      = 0U;
  hVideoIn.flags    = 0U;

  /* Initialize Video Input peripheral */
  VideoIn->Timer.Control = 0U;
  VideoIn->DMA.Control   = 0U;
  VideoIn->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  VideoIn->IRQ.Enable    = IRQ_TIMER_OVERFLOW_Msk;
  VideoIn->CONTROL       = CONTROL_MODE_IN;

  /* Set video configuration */
  VideoIn->DEVICE       = VIDEO_IN_DEVICE;
  VideoIn->FRAME_WIDTH  = VIDEO_IN_FRAME_WIDTH;
  VideoIn->FRAME_HEIGHT = VIDEO_IN_FRAME_HEIGHT;
  VideoIn->FRAME_COLOR  = VIDEO_IN_FRAME_COLOR;
  VideoIn->FRAME_RATE   = VIDEO_IN_FRAME_RATE;

  fn = VIDEO_IN_FILENAME;
  len = strlen(fn);

  if (len > 0U) {
    /* Add null terminator */
    len += 1U;

    /* Load filename register */
    for (i = 0; i < len; i++) {
      VideoIn->FILENAME = fn[i];
    }
  }

  /* Enable peripheral interrupts */
//NVIC_EnableIRQ(VideoIn_IRQn);
  NVIC->ISER[(((uint32_t)VideoIn_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)VideoIn_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* Driver is initialized */
  hVideoIn.flags = FLAGS_INIT;

  return VSTREAM_OK;
}

/* De-initialize streaming interface */
static int32_t Uninitialize (void) {

  /* Disable peripheral interrupts */
//NVIC_DisableIRQ(VideoIn_IRQn);
  NVIC->ICER[(((uint32_t)VideoIn_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)VideoIn_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* De-initialize Video Input peripheral */
  VideoIn->Timer.Control = 0U;
  VideoIn->DMA.Control   = 0U;
  VideoIn->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  VideoIn->IRQ.Enable    = 0U;
  VideoIn->CONTROL       = 0U;

  /* Clear video handle structure */
  memset(&hVideoIn, 0, sizeof(hVideoIn));

  return VSTREAM_OK;
}

/* Set streaming data buffer */
static int32_t SetBuf (void *buf, uint32_t buf_size, uint32_t block_size) {
  int32_t rval;

  if (buf == NULL) {
    rval = VSTREAM_ERROR_PARAMETER;
  }
  else if ((buf_size == 0U) || (block_size == 0U) || (block_size > buf_size)) {
    rval = VSTREAM_ERROR_PARAMETER;
  }
  else if ((hVideoIn.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoIn.active == 1U) {
    /* Streaming is active */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Set buffer */
    hVideoIn.buf.data       = (uint8_t *)buf;
    hVideoIn.buf.block_num  = buf_size / block_size;
    hVideoIn.buf.block_size = block_size;

    /* Buffer is empty */
    hVideoIn.flags |= FLAGS_BUF_EMPTY;

    /* Reset indexes */
    hVideoIn.idx_in  = 0U;
    hVideoIn.idx_get = 0U;
    hVideoIn.idx_rel = 0U;

    /* Configure DMA */
    VideoIn->DMA.Address   = (uint32_t)buf;
    VideoIn->DMA.BlockNum  = buf_size / block_size;
    VideoIn->DMA.BlockSize = block_size;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Start streaming */
static int32_t Start (uint32_t mode) {
  int32_t rval;
  uint32_t ctrl;

  if ((hVideoIn.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoIn.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hVideoIn.flags & FLAGS_BUF_FULL) != 0) {
    /* Buffer is full */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoIn.active == 1U) {
    /* Already active */
    rval = VSTREAM_OK;
  }
  else {
    rval = VSTREAM_OK;

    /* Set active status */
    hVideoIn.active = 1U;

    /* Set control register */
    ctrl = VideoIn->CONTROL | CONTROL_ENABLE_Msk;

    if (mode == VSTREAM_MODE_SINGLE) {
      /* Single mode */
      hVideoIn.flags |= FLAGS_SINGLE;
    }
    else {
      /* Continuous mode */
      hVideoIn.flags &= ~FLAGS_SINGLE;

      ctrl |= CONTROL_CONTINUOUS_Msk;
    }

    VideoIn->CONTROL = ctrl;

    if ((VideoIn->STATUS & STATUS_ACTIVE_Msk) == 0U) {
      /* Peripheral not active */
      rval = VSTREAM_ERROR;
    }
    else {
      /* Configure peripheral DMA */
      VideoIn->DMA.Control = ARM_VSI_DMA_Direction_P2M | ARM_VSI_DMA_Enable_Msk;

      /* Configure Timer */
      ctrl = ARM_VSI_Timer_Trig_DMA_Msk |
             ARM_VSI_Timer_Trig_IRQ_Msk |
             ARM_VSI_Timer_Run_Msk;

      if (mode == VSTREAM_MODE_CONTINUOUS) {
        ctrl |= ARM_VSI_Timer_Periodic_Msk;
      }

      VideoIn->Timer.Interval = 1000000U / VIDEO_IN_FRAME_RATE;

      /* Apply configuration */
      VideoIn->Timer.Control = ctrl;
    }

    if (rval != VSTREAM_OK) {
      /* Clear active flag */
      hVideoIn.active = 0U;
    }
  }

  return rval;
}

/* Stop streaming */
static int32_t Stop (void) {
  int32_t rval;

  if ((hVideoIn.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoIn.active == 0U) {
    /* Not active */
    rval = VSTREAM_OK;
  }
  else {
    /* Stop the stream */
    VideoIn->Timer.Control = 0U;
    VideoIn->DMA.Control   = 0U;
    VideoIn->CONTROL       = 0U;

    hVideoIn.active = 0U;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get pointer to a data block */
static void *GetBlock (void) {
  uint32_t buf_index;
  void *p;

  if (hVideoIn.buf.data == NULL) {
    /* Buffer not set */
    p = NULL;
  }
  else if ((hVideoIn.flags & FLAGS_BUF_EMPTY) != 0) {
    /* Buffer is empty, no data available */
    p = NULL;
  }
  else if ((hVideoIn.flags & FLAGS_LIMIT_OWN) != 0) {
    /* App already owns all the blocks */
    p = NULL;
  }
  else {
    /* Determine buffer index */
    buf_index = hVideoIn.idx_get * hVideoIn.buf.block_size;

    /* Set return pointer */
    p = &hVideoIn.buf.data[buf_index];

    /* Increment index of block returned by Get */
    hVideoIn.idx_get = (hVideoIn.idx_get + 1U) % hVideoIn.buf.block_num;

    if (hVideoIn.idx_get == hVideoIn.idx_rel) {
      /* App owns all the blocks, set the limit flag */
      hVideoIn.flags |= FLAGS_LIMIT_OWN;
    }
    if (hVideoIn.idx_get == hVideoIn.idx_in) {
      /* Buffer is empty */
      hVideoIn.flags |= FLAGS_BUF_EMPTY;
    }
    /* Clear buffer full flag */
    hVideoIn.flags &= ~FLAGS_BUF_FULL;
  }

  return p;
}

/* Release data block */
static int32_t ReleaseBlock (void) {
  int32_t rval;

  if (hVideoIn.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hVideoIn.idx_rel == hVideoIn.idx_get) && ((hVideoIn.flags & FLAGS_LIMIT_OWN) == 0)) {
    /* No blocks to release */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Increment index of the block to be released next */
    hVideoIn.idx_rel = (hVideoIn.idx_rel + 1U) % hVideoIn.buf.block_num;

    /* Clear the limit get flag */
    hVideoIn.flags &= ~FLAGS_LIMIT_OWN;

    /* Clear buffer full flag as we made space available */
    hVideoIn.flags &= ~FLAGS_BUF_FULL;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get vStream Interface status */
static vStreamStatus_t GetStatus (void) {
  vStreamStatus_t status;

  /* Get status */
  status.active   = hVideoIn.active;
  status.overflow = hVideoIn.overflow;
  status.eos      = hVideoIn.eos;

  /* Clear status */
  hVideoIn.overflow = 0U;
  hVideoIn.eos      = 0U;

  return status;
}

vStreamDriver_t Driver_vStreamVideoIn = {
  Initialize,
  Uninitialize,
  SetBuf,
  Start,
  Stop,
  GetBlock,
  ReleaseBlock,
  GetStatus
};
