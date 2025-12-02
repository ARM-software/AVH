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
#include "vstream_video_out.h"
#include "vstream_video_out_config.h"

#ifdef _RTE_
#include "RTE_Components.h"
#endif
#include CMSIS_device_header
#include "arm_vsi.h"

/* Peripheral definitions */
#define VideoOut                ARM_VSI6              /* Video Output access struct     */
#define VideoOut_IRQn           ARM_VSI6_IRQn         /* Video Output Interrupt number  */
#define VideoOut_Handler        ARM_VSI6_Handler      /* Video Output Interrupt handler */

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
  volatile uint32_t idx_out;  /* Index of block currently being streamed            */
  volatile uint8_t  active;   /* Streaming active flag  */
  volatile uint8_t  underflow; /* Buffer underflow flag */
  volatile uint8_t  eos;      /* End of stream flag     */
  volatile uint8_t  flags;    /* Handle status flags    */
} StreamHandle_t;

/* vStream Handle */
static StreamHandle_t hVideoOut = {0};

/**
  \brief Video Output Interrupt Handler.
*/
void VideoOut_Handler (void) {
  uint32_t status;
  uint32_t event;

  status = VideoOut->STATUS;

  VideoOut->IRQ.Clear = IRQ_TIMER_OVERFLOW_Msk;
  __DSB();
  __ISB();

  event = 0U;

  if ((status & STATUS_DATA_Msk) != 0) {
    /* Data block streamed out */
    event |= VSTREAM_EVENT_DATA;

    /* Get index of the block being streamed */
    hVideoOut.idx_out = VideoOut->DMA.BlockIndex;
    /* Clear buffer full flag */
    hVideoOut.flags &= ~FLAGS_BUF_FULL;

    if (hVideoOut.idx_out == hVideoOut.idx_rel) {
      /* Buffer is empty */
      hVideoOut.flags |= FLAGS_BUF_EMPTY;

      if ((hVideoOut.flags & FLAGS_SINGLE) == 0U) {
        /* Continuous mode, no new stream buffer */
        hVideoOut.underflow = 1U;

        event |= VSTREAM_EVENT_UNDERFLOW;
      }
    }
  }

  if ((status & STATUS_EOS_Msk) != 0U) {
    /* End of stream */
    hVideoOut.eos = 1U;

    event |= VSTREAM_EVENT_EOS;
  }

  if ((hVideoOut.flags & FLAGS_SINGLE) != 0U) {
    /* Single mode, clear active flag */
    hVideoOut.active = 0U;
  }

  if ((hVideoOut.callback != NULL) && (event != 0U)) {
    /* Call application callback function */
    hVideoOut.callback(event);
  }
}

/* Initialize streaming interface */
static int32_t Initialize (vStreamEvent_t event_cb) {
  char *fn;
  uint32_t len;
  uint32_t i;

  hVideoOut.callback  = event_cb;
  hVideoOut.active    = 0U;
  hVideoOut.underflow = 0U;
  hVideoOut.eos       = 0U;
  hVideoOut.flags     = 0U;

  /* Initialize Video Output peripheral */
  VideoOut->Timer.Control = 0U;
  VideoOut->DMA.Control   = 0U;
  VideoOut->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  VideoOut->IRQ.Enable    = IRQ_TIMER_OVERFLOW_Msk;
  VideoOut->CONTROL       = CONTROL_MODE_OUT;

  /* Set video configuration */
  VideoOut->FRAME_WIDTH  = VIDEO_OUT_FRAME_WIDTH;
  VideoOut->FRAME_HEIGHT = VIDEO_OUT_FRAME_HEIGHT;
  VideoOut->FRAME_COLOR  = VIDEO_OUT_FRAME_COLOR;
  VideoOut->FRAME_RATE   = VIDEO_OUT_FRAME_RATE;

  fn = VIDEO_OUT_FILENAME;
  len = strlen(fn);

  if (len > 0U) {
    /* Add null terminator */
    len += 1U;

    /* Load filename register */
    for (i = 0; i < len; i++) {
      VideoOut->FILENAME = fn[i];
    }
  }

  /* Enable peripheral interrupts */
//NVIC_EnableIRQ(VideoIn_IRQn);
  NVIC->ISER[(((uint32_t)VideoOut_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)VideoOut_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* Driver is initialized */
  hVideoOut.flags = FLAGS_INIT;

  return VSTREAM_OK;
}

/* De-initialize streaming interface */
static int32_t Uninitialize (void) {

  /* Disable peripheral interrupts */
//NVIC_DisableIRQ(VideoIn_IRQn);
  NVIC->ICER[(((uint32_t)VideoOut_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)VideoOut_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* De-initialize Video Output peripheral */
  VideoOut->Timer.Control = 0U;
  VideoOut->DMA.Control   = 0U;
  VideoOut->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  VideoOut->IRQ.Enable    = 0U;
  VideoOut->CONTROL       = 0U;

  /* Clear video handle structure */
  memset(&hVideoOut, 0, sizeof(hVideoOut));

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
  else if ((hVideoOut.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoOut.active == 1U) {
    /* Streaming is active */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Set buffer */
    hVideoOut.buf.data       = (uint8_t *)buf;
    hVideoOut.buf.block_num  = buf_size / block_size;
    hVideoOut.buf.block_size = block_size;

    /* Buffer is empty */
    hVideoOut.flags |= FLAGS_BUF_EMPTY;

    /* Reset indexes */
    hVideoOut.idx_out = 0U;
    hVideoOut.idx_get = 0U;
    hVideoOut.idx_rel = 0U;

    /* Configure DMA */
    VideoOut->DMA.Address   = (uint32_t)buf;
    VideoOut->DMA.BlockNum  = buf_size / block_size;
    VideoOut->DMA.BlockSize = block_size;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Start streaming */
static int32_t Start (uint32_t mode) {
  int32_t rval;
  uint32_t ctrl;

  if ((hVideoOut.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoOut.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hVideoOut.flags & FLAGS_BUF_EMPTY) != 0) {
    /* Buffer is empty */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoOut.active == 1U) {
    /* Already active */
    rval = VSTREAM_OK;
  }
  else {
    rval = VSTREAM_OK;

    /* Set active status */
    hVideoOut.active = 1U;

    /* Set control register */
    ctrl = VideoOut->CONTROL | CONTROL_ENABLE_Msk;

    if (mode == VSTREAM_MODE_SINGLE) {
      /* Single mode */
      hVideoOut.flags |= FLAGS_SINGLE;
    }
    else {
      /* Continuous mode */
      hVideoOut.flags &= ~FLAGS_SINGLE;
      ctrl |= CONTROL_CONTINUOUS_Msk;
    }

    VideoOut->CONTROL = ctrl;

    if ((VideoOut->STATUS & STATUS_ACTIVE_Msk) == 0U) {
      /* Peripheral not active */
      rval = VSTREAM_ERROR;
    }
    else {
      /* Configure peripheral DMA */
      VideoOut->DMA.Control = ARM_VSI_DMA_Direction_M2P | ARM_VSI_DMA_Enable_Msk;

      /* Configure Timer */
      ctrl = ARM_VSI_Timer_Trig_DMA_Msk |
             ARM_VSI_Timer_Trig_IRQ_Msk |
             ARM_VSI_Timer_Run_Msk;

      if (mode == VSTREAM_MODE_CONTINUOUS) {
        ctrl |= ARM_VSI_Timer_Periodic_Msk;
      }

      VideoOut->Timer.Interval = 1000000U / VIDEO_OUT_FRAME_RATE;

      /* Apply configuration */
      VideoOut->Timer.Control = ctrl;
    }

    if (rval != VSTREAM_OK) {
      /* Clear active flag */
      hVideoOut.active = 0U;
    }
  }

  return rval;
}

/* Stop streaming */
static int32_t Stop (void) {
  int32_t rval;

  if ((hVideoOut.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hVideoOut.active == 0U) {
    /* Not active */
    rval = VSTREAM_OK;
  }
  else {
    /* Stop the stream */
    VideoOut->Timer.Control = 0U;
    VideoOut->DMA.Control   = 0U;
    VideoOut->CONTROL       = 0U;

    hVideoOut.active = 0U;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get pointer to a data block */
static void *GetBlock (void) {
  uint32_t buf_index;
  void *p;

  if (hVideoOut.buf.data == NULL) {
    /* Buffer not set */
    p = NULL;
  }
  else if ((hVideoOut.flags & FLAGS_LIMIT_OWN) != 0) {
    /* App already owns all the blocks */
    p = NULL;
  }
  else {
    /* Determine buffer index */
    buf_index = hVideoOut.idx_get * hVideoOut.buf.block_size;

    /* Set return pointer */
    p = &hVideoOut.buf.data[buf_index];

    /* Increment index of block returned by Get */
    hVideoOut.idx_get = (hVideoOut.idx_get + 1U) % hVideoOut.buf.block_num;

    if (hVideoOut.idx_get == hVideoOut.idx_rel) {
      /* App owns all the blocks, set the limit flag */
      hVideoOut.flags |= FLAGS_LIMIT_OWN;
    }
  }

  return p;
}

/* Release data block */
static int32_t ReleaseBlock (void) {
  int32_t  rval;

  if (hVideoOut.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hVideoOut.idx_rel == hVideoOut.idx_get) && ((hVideoOut.flags & FLAGS_LIMIT_OWN) == 0)) {
    /* No blocks to release */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Increment index of the block to be released next */
    hVideoOut.idx_rel = (hVideoOut.idx_rel + 1U) % hVideoOut.buf.block_num;

    if (hVideoOut.idx_rel == hVideoOut.idx_out) {
      /* Buffer is full */
      hVideoOut.flags |= FLAGS_BUF_FULL;
    }

    /* Clear the limit get flag */
    hVideoOut.flags &= ~FLAGS_LIMIT_OWN;

    /* Clear the buffer empty flag */
    hVideoOut.flags &= ~FLAGS_BUF_EMPTY;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get vStream Interface status */
static vStreamStatus_t GetStatus (void) {
  vStreamStatus_t status;

  /* Get status */
  status.active    = hVideoOut.active;
  status.underflow = hVideoOut.underflow;
  status.eos       = hVideoOut.eos;

  /* Clear status */
  hVideoOut.underflow = 0U;
  hVideoOut.eos       = 0U;

  return status;
}

vStreamDriver_t Driver_vStreamVideoOut = {
  Initialize,
  Uninitialize,
  SetBuf,
  Start,
  Stop,
  GetBlock,
  ReleaseBlock,
  GetStatus
};
