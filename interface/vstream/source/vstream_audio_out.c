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
#include "cmsis_vstream.h"

#ifdef _RTE_
#include "RTE_Components.h"
#endif
#include CMSIS_device_header
#include "arm_vsi.h"

/* Number of channels 1=Mono, 2=Stereo            */
/* Defines the number of audio channels in stream */
#ifndef AUDIO_OUT_CHANNELS
#define AUDIO_OUT_CHANNELS     2U
#endif

/* Number of bits per sample <0=>8 <1=>16 <2=>24 <3=>32  */
/* Defines number of bits of information in each sample. */
#ifndef AUDIO_OUT_SAMPLE_BITS
#define AUDIO_OUT_SAMPLE_BITS  16U
#endif

/* Sample rate (samples per second)                   */
/* Defines the number of samples captured per second. */
#ifndef AUDIO_OUT_SAMPLE_RATE
#define AUDIO_OUT_SAMPLE_RATE  16000U
#endif


/* Audio Peripheral definitions */
#define AudioOut              ARM_VSI1                /* Audio Output access struct     */
#define AudioOut_IRQn         ARM_VSI1_IRQn           /* Audio Output Interrupt number  */
#define AudioOut_Handler      ARM_VSI1_Handler        /* Audio Output Interrupt handler */

/* Audio Peripheral registers */
#define STATUS                Regs[0]                 /* Status register           */
#define CONTROL               Regs[1]                 /* Control receiver          */
#define CHANNELS              Regs[2]                 /* Number of channels        */
#define SAMPLE_BITS           Regs[3]                 /* Number of bits per sample */
#define SAMPLE_RATE           Regs[4]                 /* Samples per second        */

/* STATUS register definitions */
#define STATUS_OPEN_Msk       (1UL << 0)              /* Stream Open    */
#define STATUS_DATA_Msk       (1UL << 1)              /* Data Available */
#define STATUS_EOS_Msk        (1UL << 2)              /* End of Stream  */

/* Audio Control register definitions */
#define CONTROL_ENABLE_Msk    (1UL << 0)              /* CONTROL: ENABLE Streaming */

/* Handle Flags Definitions */
#define FLAGS_INIT            (1U << 0)
#define FLAGS_START           (1U << 1)
#define FLAGS_SINGLE          (1U << 2)
#define FLAGS_LIMIT_OWN       (1U << 3)
#define FLAGS_BUF_EMPTY       (1U << 4)
#define FLAGS_BUF_FULL        (1U << 5)

/* Stream Buffer Type Definition */
typedef struct stream_buf_s {
  uint8_t *data;              /* Data buffer pointer             */
  uint32_t block_num;         /* Number of blocks in data buffer */
  uint32_t block_size;        /* Size of block in data buffer    */
} StreamBuf_t;

/* vStream Handle Type Definition */
typedef struct {
  vStreamEvent_t    callback; /* Callback from vStream driver */
  StreamBuf_t       buf;      /* Stream buffer    */
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

  AudioOut->IRQ.Clear = 0x00000001U;
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

  if (hAudioOut.flags & FLAGS_SINGLE) {
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

  hAudioOut.callback  = event_cb;
  hAudioOut.active    = 0U;
  hAudioOut.underflow = 0U;
  hAudioOut.eos       = 0U;
  hAudioOut.flags     = 0U;

  /* Initialize Audio Input peripheral */
  AudioOut->Timer.Control = 0U;
  AudioOut->DMA.Control   = 0U;
  AudioOut->IRQ.Clear     = 0x00000001U;
  AudioOut->IRQ.Enable    = 0x00000001U;
  AudioOut->CONTROL       = 0U;

  /* Set audio configuration */
  AudioOut->CHANNELS    = AUDIO_OUT_CHANNELS;
  AudioOut->SAMPLE_BITS = AUDIO_OUT_SAMPLE_BITS;
  AudioOut->SAMPLE_RATE = AUDIO_OUT_SAMPLE_RATE;

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
  AudioOut->IRQ.Clear     = 0x00000001U;
  AudioOut->IRQ.Enable    = 0x00000000U;
  AudioOut->CONTROL       = 0U;

  /* Clear audio control block structure */
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
    hAudioOut.buf.data       = (uint8_t *)buf;
    hAudioOut.buf.block_num  = buf_size / block_size;
    hAudioOut.buf.block_size = block_size;

    /* Buffer is empty */
    hAudioOut.flags |= FLAGS_BUF_EMPTY;

    /* Reset indexes */
    hAudioOut.idx_out = 0U;
    hAudioOut.idx_get = 0U;
    hAudioOut.idx_rel = 0U;

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

    if (mode == VSTREAM_MODE_SINGLE) {
      /* Single mode */
      hAudioOut.flags |= FLAGS_SINGLE;

      /* Initialize timer control register for one-shot mode */
      ctrl = ARM_VSI_Timer_Trig_DMA_Msk | ARM_VSI_Timer_Trig_IRQ_Msk;
    }
    else {
      /* Continuous mode */
      hAudioOut.flags &= ~FLAGS_SINGLE;

      /* Initialize timer control register for continuous mode */
      ctrl = ARM_VSI_Timer_Trig_DMA_Msk | ARM_VSI_Timer_Trig_IRQ_Msk | ARM_VSI_Timer_Periodic_Msk;
    }

    AudioOut->CONTROL     = CONTROL_ENABLE_Msk;
    AudioOut->DMA.Control = ARM_VSI_DMA_Direction_M2P | ARM_VSI_DMA_Enable_Msk;

    sample_size = AudioOut->CHANNELS * ((AudioOut->SAMPLE_BITS + 7U) / 8U);
    sample_rate = AudioOut->SAMPLE_RATE;
    block_size  = AudioOut->DMA.BlockSize;

    AudioOut->Timer.Interval = ((uint64_t)1000000U * (block_size / sample_size)) / sample_rate;

    /* Apply configuration and start the timer */
    AudioOut->Timer.Control = ctrl | ARM_VSI_Timer_Run_Msk;
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
