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
#include "vstream_audio_in.h"
#include "vstream_audio_in_config.h"

#ifdef _RTE_
#include "RTE_Components.h"
#endif
#include CMSIS_device_header
#include "arm_vsi.h"

/* Peripheral definitions */
#define AudioIn                 ARM_VSI0              /* Audio Input access struct     */
#define AudioIn_IRQn            ARM_VSI0_IRQn         /* Audio Input Interrupt number  */
#define AudioIn_Handler         ARM_VSI0_Handler      /* Audio Input Interrupt handler */

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
  volatile uint32_t idx_in;   /* Index of block currently being streamed            */
  volatile uint8_t  active;   /* Streaming active flag */
  volatile uint8_t  overflow; /* Buffer overflow flag  */
  volatile uint8_t  eos;      /* End of stream flag    */
  volatile uint8_t  flags;    /* Handle status flags   */
} StreamHandle_t;

/* vStream Handle */
static StreamHandle_t hAudioIn = {0};

/**
  \brief Audio Input Interrupt Handler.
*/
void AudioIn_Handler (void) {
  uint32_t status;
  uint32_t event;

  status = AudioIn->STATUS;

  AudioIn->IRQ.Clear = IRQ_TIMER_OVERFLOW_Msk;
  __DSB();
  __ISB();

  event = 0U;

  if ((status & STATUS_DATA_Msk) != 0U) {
    /* Data block streamed in */
    event |= VSTREAM_EVENT_DATA;

    /* Increment index of the block being streamed */
    hAudioIn.idx_in = (hAudioIn.idx_in + 1U) % hAudioIn.buf.block_num;

    /* Clear buffer empty flag */
    hAudioIn.flags &= ~FLAGS_BUF_EMPTY;

    if (hAudioIn.idx_in == hAudioIn.idx_rel) {
      /* Buffer is full */
      hAudioIn.flags |= FLAGS_BUF_FULL;

      if ((hAudioIn.flags & FLAGS_SINGLE) == 0U) {
        /* Continuous mode, no free stream buffer */
        hAudioIn.overflow = 1U;

        event |= VSTREAM_EVENT_OVERFLOW;
      }
    }
  }

  if ((status & STATUS_EOS_Msk) != 0U) {
    /* End of stream */
    hAudioIn.eos = 1U;
    event |= VSTREAM_EVENT_EOS;
  }

  if ((hAudioIn.flags & FLAGS_SINGLE) != 0U) {
    /* Single mode, clear active flag */
    hAudioIn.active = 0U;
  }

  if ((hAudioIn.callback != NULL) && (event != 0U)) {
    /* Call application callback function */
    hAudioIn.callback(event);
  }
}

/* Initialize streaming interface */
static int32_t Initialize (vStreamEvent_t event_cb) {
  char *fn;
  uint32_t len;
  uint32_t i;

  hAudioIn.callback = event_cb;
  hAudioIn.active   = 0U;
  hAudioIn.overflow = 0U;
  hAudioIn.eos      = 0U;
  hAudioIn.flags    = 0U;

  /* Initialize Audio Input peripheral */
  AudioIn->Timer.Control = 0U;
  AudioIn->DMA.Control   = 0U;
  AudioIn->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  AudioIn->IRQ.Enable    = IRQ_TIMER_OVERFLOW_Msk;
  AudioIn->CONTROL       = CONTROL_MODE_IN;

  /* Set audio configuration */
  AudioIn->DEVICE      = AUDIO_IN_DEVICE;
  AudioIn->CHANNELS    = AUDIO_IN_CHANNELS;
  AudioIn->SAMPLE_BITS = AUDIO_IN_SAMPLE_BITS;
  AudioIn->SAMPLE_RATE = AUDIO_IN_SAMPLE_RATE;

  fn = AUDIO_IN_FILENAME;
  len = strlen(fn);

  if (len > 0U) {
    /* Add null terminator */
    len += 1U;

    /* Load filename register */
    for (i = 0; i < len; i++) {
      AudioIn->FILENAME = fn[i];
    }
  }

  /* Enable peripheral interrupts */
//NVIC_EnableIRQ(AudioIn_IRQn);
  NVIC->ISER[(((uint32_t)AudioIn_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)AudioIn_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* Driver is initialized */
  hAudioIn.flags |= FLAGS_INIT;

  return VSTREAM_OK;
}

/* De-initialize streaming interface */
static int32_t Uninitialize (void) {

  /* Disable peripheral interrupts */
//NVIC_DisableIRQ(AudioIn_IRQn);
  NVIC->ICER[(((uint32_t)AudioIn_IRQn) >> 5UL)] = (uint32_t)(1UL << (((uint32_t)AudioIn_IRQn) & 0x1FUL));
  __DSB();
  __ISB();

  /* De-initialize Audio Input peripheral */
  AudioIn->Timer.Control = 0U;
  AudioIn->DMA.Control   = 0U;
  AudioIn->IRQ.Clear     = IRQ_TIMER_OVERFLOW_Msk;
  AudioIn->IRQ.Enable    = 0U;
  AudioIn->CONTROL       = 0U;

  /* Clear audio handle structure */
  memset(&hAudioIn, 0, sizeof(hAudioIn));

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
  else if ((hAudioIn.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioIn.active == 1U) {
    /* Streaming is active */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Set buffer */
    hAudioIn.buf.data       = (uint8_t *)buf;
    hAudioIn.buf.block_num  = buf_size / block_size;
    hAudioIn.buf.block_size = block_size;

    /* Buffer is empty */
    hAudioIn.flags |= FLAGS_BUF_EMPTY;

    /* Reset indexes */
    hAudioIn.idx_in  = 0U;
    hAudioIn.idx_get = 0U;
    hAudioIn.idx_rel = 0U;

    /* Configure DMA */
    AudioIn->DMA.Address   = (uint32_t)buf;
    AudioIn->DMA.BlockNum  = buf_size / block_size;
    AudioIn->DMA.BlockSize = block_size;

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

  if ((hAudioIn.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioIn.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hAudioIn.flags & FLAGS_BUF_FULL) != 0) {
    /* Buffer is full */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioIn.active == 1U) {
    /* Already active */
    rval = VSTREAM_OK;
  }
  else {
    rval = VSTREAM_OK;

    /* Set active status */
    hAudioIn.active = 1U;

    /* Set control register */
    ctrl = AudioIn->CONTROL | CONTROL_ENABLE_Msk;

    if (mode == VSTREAM_MODE_SINGLE) {
      /* Single mode */
      hAudioIn.flags |= FLAGS_SINGLE;
    }
    else {
      /* Continuous mode */
      hAudioIn.flags &= ~FLAGS_SINGLE;

      ctrl |= CONTROL_CONTINUOUS_Msk;
    }

    AudioIn->CONTROL = ctrl;

    if ((AudioIn->STATUS & STATUS_ACTIVE_Msk) == 0U) {
      /* Peripheral not active */
      rval = VSTREAM_ERROR;
    }
    else {
      /* Configure peripheral DMA */
      AudioIn->DMA.Control = ARM_VSI_DMA_Direction_P2M | ARM_VSI_DMA_Enable_Msk;

      /* Configure Timer */
      ctrl = ARM_VSI_Timer_Trig_DMA_Msk |
             ARM_VSI_Timer_Trig_IRQ_Msk |
             ARM_VSI_Timer_Run_Msk;

      if (mode == VSTREAM_MODE_CONTINUOUS) {
        ctrl |= ARM_VSI_Timer_Periodic_Msk;
      }

      sample_size = AudioIn->CHANNELS * ((AudioIn->SAMPLE_BITS + 7U) / 8U);
      sample_rate = AudioIn->SAMPLE_RATE;
      block_size  = AudioIn->DMA.BlockSize;

      AudioIn->Timer.Interval = ((uint64_t)1000000U * (block_size / sample_size)) / sample_rate;

      /* Apply configuration */
      AudioIn->Timer.Control = ctrl;
    }

    if (rval != VSTREAM_OK) {
      /* Clear active flag */
      hAudioIn.active = 0U;
    }
  }

  return rval;
}

/* Stop streaming */
static int32_t Stop (void) {
  int32_t rval;

  if ((hAudioIn.flags & FLAGS_INIT) == 0) {
    /* Not initialized */
    rval = VSTREAM_ERROR;
  }
  else if (hAudioIn.active == 0U) {
    /* Not active */
    rval = VSTREAM_OK;
  }
  else {
    /* Stop the stream */
    AudioIn->Timer.Control = 0U;
    AudioIn->DMA.Control   = 0U;
    AudioIn->CONTROL       = 0U;

    hAudioIn.active = 0U;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get pointer to a data block */
static void *GetBlock (void) {
  uint32_t buf_index;
  void *p;

  if (hAudioIn.buf.data == NULL) {
    /* Buffer not set */
    p = NULL;
  }
  else if ((hAudioIn.flags & FLAGS_BUF_EMPTY) != 0) {
    /* Buffer is empty, no data available */
    p = NULL;
  }
  else if ((hAudioIn.flags & FLAGS_LIMIT_OWN) != 0) {
    /* App already owns all the blocks */
    p = NULL;
  }
  else {
    /* Determine buffer index */
    buf_index = hAudioIn.idx_get * hAudioIn.buf.block_size;

    /* Set return pointer */
    p = &hAudioIn.buf.data[buf_index];

    /* Increment index of block returned by Get */
    hAudioIn.idx_get = (hAudioIn.idx_get + 1U) % hAudioIn.buf.block_num;

    if (hAudioIn.idx_get == hAudioIn.idx_rel) {
      /* App owns all the blocks, set the limit flag */
      hAudioIn.flags |= FLAGS_LIMIT_OWN;
    }
    if (hAudioIn.idx_get == hAudioIn.idx_in) {
      /* Buffer is empty */
      hAudioIn.flags |= FLAGS_BUF_EMPTY;
    }
    /* Clear buffer full flag */
    hAudioIn.flags &= ~FLAGS_BUF_FULL;
  }

  return p;
}

/* Release data block */
static int32_t ReleaseBlock (void) {
  int32_t rval;

  if (hAudioIn.buf.data == NULL) {
    /* Buffer not set */
    rval = VSTREAM_ERROR;
  }
  else if ((hAudioIn.idx_rel == hAudioIn.idx_get) && ((hAudioIn.flags & FLAGS_LIMIT_OWN) == 0)) {
    /* No blocks to release */
    rval = VSTREAM_ERROR;
  }
  else {
    /* Increment index of the block to be released next */
    hAudioIn.idx_rel = (hAudioIn.idx_rel + 1U) % hAudioIn.buf.block_num;

    /* Clear the limit get flag */
    hAudioIn.flags &= ~FLAGS_LIMIT_OWN;

    /* Clear buffer full flag as we made space available */
    hAudioIn.flags &= ~FLAGS_BUF_FULL;

    rval = VSTREAM_OK;
  }

  return rval;
}

/* Get vStream Interface status */
static vStreamStatus_t GetStatus (void) {
  vStreamStatus_t status;

  /* Get status */
  status.active   = hAudioIn.active;
  status.overflow = hAudioIn.overflow;
  status.eos      = hAudioIn.eos;

  /* Clear status */
  hAudioIn.overflow = 0U;
  hAudioIn.eos      = 0U;

  return status;
}

vStreamDriver_t Driver_vStreamAudioIn = {
  Initialize,
  Uninitialize,
  SetBuf,
  Start,
  Stop,
  GetBlock,
  ReleaseBlock,
  GetStatus
};
