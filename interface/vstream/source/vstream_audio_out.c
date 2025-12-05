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
#include "vstream_audio_out.h"
#include "vstream_audio_out_config.h"

#ifdef _RTE_
#include "RTE_Components.h"
#endif
#include CMSIS_device_header
#include "arm_vsi.h"

/* Peripheral definitions */
#define AudioOut                ARM_VSI1              /* Audio Output access struct     */
#define AudioOut_IRQn           ARM_VSI1_IRQn         /* Audio Output Interrupt number  */
#define AudioOut_Handler        ARM_VSI1_Handler      /* Audio Output Interrupt handler */

/* Peripheral registers */
#define CONTROL                 Regs[0]  /* Control: enable, mode, continuous          */
#define STATUS                  Regs[1]  /* Status: active, eos, file_name, file_valid */
#define DEVICE                  Regs[2]  /* Streaming device                           */
#define FILENAME                Regs[3]  /* Filename string array                      */
#define CHANNELS                Regs[4]  /* Number of channels                         */
#define SAMPLE_RATE             Regs[5]  /* Samples per second                         */
#define SAMPLE_BITS             Regs[6]  /* Number of bits per sample                  */

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
static StreamHandle_t hAudioOut = {0};

/**
  \brief Audio Output Interrupt Handler.
*/
void AudioOut_Handler (void) {
  uint32_t status;
  uint32_t event;

  status = AudioOut->STATUS;

  AudioOut->IRQ.Clear = IRQ_TIMER_OVERFLOW_Msk;
  __DSB();
  __ISB();

  event = 0U;

  if ((status & STATUS_DATA_Msk) != 0U) {
    /* Data block streamed out */
    event |= VSTREAM_EVENT_DATA;

    /* Increment index of the block being streamed */
    hAudioOut.idx_out = (hAudioOut.idx_out + 1) % hAudioOut.buf.block_num;

    /* Clear buffer full flag */
    hAudioOut.flags &= ~FLAGS_BUF_FULL;

    if (hAudioOut.idx_out == hAudioOut.idx_rel) {
      /* Buffer is empty */
      hAudioOut.flags |= FLAGS_BUF_EMPTY;

      if ((hAudioOut.flags & FLAGS_SINGLE) == 0U) {
        /* Continuous mode, no new stream buffer */
        hAudioOut.underflow = 1U;

        event |= VSTREAM_EVENT_UNDERFLOW;
      }
    }
  }

  if ((status & STATUS_EOS_Msk) != 0U) {
    /* End of stream */
    hAudioOut.eos = 1U;
    event |= VSTREAM_EVENT_EOS;
  }

  if ((hAudioOut.flags & FLAGS_SINGLE) != 0U) {
    /* Single mode, clear active flag */
    hAudioOut.active = 0U;
  }

  if ((hAudioOut.callback != NULL) && (event != 0U)) {
    /* Call application callback function */
    hAudioOut.callback(event);
  }
}

/* Initialize streaming interface */
static int32_t Initialize (vStreamEvent_t event_cb) {
  char *fn;
  uint32_t len;
  uint32_t i;

  hAudioOut.callback  = event_cb;
  hAudioOut.active    = 0U;
  hAudioOut.underflow = 0U;
  hAudioOut.eos       = 0U;
  hAudioOut.flags     = 0U;

  /* Initialize Audio Input peripheral */
  AudioOut->Timer.Control = 0U;
  AudioOut->DMA.Control   = 0U;
  AudioOut->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  AudioOut->IRQ.Enable    = IRQ_TIMER_OVERFLOW_Msk;
  AudioOut->CONTROL       = CONTROL_MODE_OUT;

  /* Set audio configuration */
  AudioOut->DEVICE      = AUDIO_OUT_DEVICE;
  AudioOut->CHANNELS    = AUDIO_OUT_CHANNELS;
  AudioOut->SAMPLE_BITS = AUDIO_OUT_SAMPLE_BITS;
  AudioOut->SAMPLE_RATE = AUDIO_OUT_SAMPLE_RATE;

  fn = AUDIO_OUT_FILENAME;
  len = strlen(fn);

  if (len > 0U) {
    /* Add null terminator */
    len += 1U;

    /* Load filename register */
    for (i = 0; i < len; i++) {
      AudioOut->FILENAME = fn[i];
    }
  }

  /* Enable peripheral interrupts */
//NVIC_EnableIRQ(AudioOut_IRQn);
  NVIC->ISER[(((uint32_t)AudioOut_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)AudioOut_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* Driver is initialized */
  hAudioOut.flags |= FLAGS_INIT;

  return VSTREAM_OK;
}

/* De-initialize streaming interface */
static int32_t Uninitialize (void) {

  /* Disable peripheral interrupts */
//NVIC_DisableIRQ(AudioOut_IRQn);
  NVIC->ICER[(((uint32_t)AudioOut_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)AudioOut_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* De-initialize Audio Input peripheral */
  AudioOut->Timer.Control = 0U;
  AudioOut->DMA.Control   = 0U;
  AudioOut->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  AudioOut->IRQ.Enable    = 0U;
  AudioOut->CONTROL       = 0U;

  /* Clear audio handle structure */
  memset(&hAudioOut, 0, sizeof(hAudioOut));

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
  else if ((hAudioOut.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioOut.active == 1U) {
    /* Streaming is active */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Set buffer */
    hAudioOut.buf.data       = (uint8_t *)buf;
    hAudioOut.buf.block_num  = buf_size / block_size;
    hAudioOut.buf.block_size = block_size;

    /* Buffer is empty */
    hAudioOut.flags |= FLAGS_BUF_EMPTY;

    /* Reset indexes */
    hAudioOut.idx_out = 0U;
    hAudioOut.idx_get = 0U;
    hAudioOut.idx_rel = 0U;

    /* Configure DMA */
    AudioOut->DMA.Address   = (uint32_t)buf;
    AudioOut->DMA.BlockNum  = buf_size / block_size;
    AudioOut->DMA.BlockSize = block_size;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Start streaming */
static int32_t Start (uint32_t mode) {
  int32_t  rval;
  uint32_t ctrl;
  uint32_t sample_size;
  uint32_t sample_rate;
  uint32_t block_size;

  if ((hAudioOut.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioOut.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hAudioOut.flags & FLAGS_BUF_EMPTY) != 0) {
    /* Buffer is empty */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioOut.active == 1U) {
    /* Already active */
    rval = VSTREAM_OK;
  }
  else {
    rval = VSTREAM_OK;

    /* Set active status */
    hAudioOut.active = 1U;

    /* Set control register */
    ctrl = AudioOut->CONTROL | CONTROL_ENABLE_Msk;

    if (mode == VSTREAM_MODE_SINGLE) {
      /* Single mode */
      hAudioOut.flags |= FLAGS_SINGLE;
    }
    else {
      /* Continuous mode */
      hAudioOut.flags &= ~FLAGS_SINGLE;

      ctrl |= CONTROL_CONTINUOUS_Msk;
    }

    AudioOut->CONTROL = ctrl;

    if ((AudioOut->STATUS & STATUS_ACTIVE_Msk) == 0U) {
      /* Peripheral not active */
      rval = VSTREAM_ERROR;
    }
    else {
      /* Configure peripheral DMA */
      AudioOut->DMA.Control = ARM_VSI_DMA_Direction_M2P | ARM_VSI_DMA_Enable_Msk;

      /* Configure Timer */
      ctrl = ARM_VSI_Timer_Trig_DMA_Msk |
             ARM_VSI_Timer_Trig_IRQ_Msk |
             ARM_VSI_Timer_Run_Msk;

      if (mode == VSTREAM_MODE_CONTINUOUS) {
        ctrl |= ARM_VSI_Timer_Periodic_Msk;
      }

      sample_size = AudioOut->CHANNELS * ((AudioOut->SAMPLE_BITS + 7U) / 8U);
      sample_rate = AudioOut->SAMPLE_RATE;
      block_size  = AudioOut->DMA.BlockSize;

      AudioOut->Timer.Interval = ((uint64_t)1000000U * (block_size / sample_size)) / sample_rate;

      /* Apply configuration */
      AudioOut->Timer.Control = ctrl;
    }

    if (rval != VSTREAM_OK) {
      /* Clear active flag */
      hAudioOut.active = 0U;
    }
  }

  return rval;
}

/* Stop streaming */
static int32_t Stop (void) {
  int32_t rval;

  if ((hAudioOut.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioOut.active == 0U) {
    /* Not active */
    rval = VSTREAM_OK;
  }
  else {
    /* Stop the stream */
    AudioOut->Timer.Control = 0U;
    AudioOut->DMA.Control   = 0U;
    AudioOut->CONTROL       = 0U;

    hAudioOut.active = 0U;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get pointer to a data block */
static void *GetBlock (void) {
  uint32_t buf_index;
  void *p;

  if (hAudioOut.buf.data == NULL) {
    /* Buffer not set */
    p = NULL;
  }
  else if ((hAudioOut.flags & FLAGS_LIMIT_OWN) != 0) {
    /* App already owns all the blocks */
    p = NULL;
  }
  else {
    /* Determine buffer index */
    buf_index = hAudioOut.idx_get * hAudioOut.buf.block_size;

    /* Set return pointer */
    p = &hAudioOut.buf.data[buf_index];

    /* Increment index of block returned by Get */
    hAudioOut.idx_get = (hAudioOut.idx_get + 1U) % hAudioOut.buf.block_num;

    if (hAudioOut.idx_get == hAudioOut.idx_rel) {
      /* App owns all the blocks, set the limit flag */
      hAudioOut.flags |= FLAGS_LIMIT_OWN;
    }
  }

  return p;
}

/* Release data block */
static int32_t ReleaseBlock (void) {
  int32_t rval;

  if (hAudioOut.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hAudioOut.idx_rel == hAudioOut.idx_get) && ((hAudioOut.flags & FLAGS_LIMIT_OWN) == 0)) {
    /* No blocks to release */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Increment index of the block to be released next */
    hAudioOut.idx_rel = (hAudioOut.idx_rel + 1U) % hAudioOut.buf.block_num;

    if (hAudioOut.idx_rel == hAudioOut.idx_out) {
      /* Buffer is full */
      hAudioOut.flags |= FLAGS_BUF_FULL;
    }

    /* Clear the limit get flag */
    hAudioOut.flags &= ~FLAGS_LIMIT_OWN;
    /* Clear the buffer empty flag */
    hAudioOut.flags &= ~FLAGS_BUF_EMPTY;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get vStream Interface status */
static vStreamStatus_t GetStatus (void) {
  vStreamStatus_t status;

  /* Get status */
  status.active    = hAudioOut.active;
  status.underflow = hAudioOut.underflow;
  status.eos       = hAudioOut.eos;

  /* Clear status */
  hAudioOut.underflow = 0U;
  hAudioOut.eos       = 0U;

  return status;
}

vStreamDriver_t Driver_vStreamAudioOut = {
  Initialize,
  Uninitialize,
  SetBuf,
  Start,
  Stop,
  GetBlock,
  ReleaseBlock,
  GetStatus
};
