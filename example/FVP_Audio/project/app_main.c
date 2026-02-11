/*---------------------------------------------------------------------------
 * Copyright (c) 2025 Arm Limited (or its affiliates). All rights reserved.
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
 *---------------------------------------------------------------------------*/

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "cmsis_vstream.h"

#include "cmsis_os2.h"
#include "main.h"


/* Define the number of audio channels in stream (1=Mono, 2=Stereo) */
#ifndef AUDIO_CHANNELS
#define AUDIO_CHANNELS          2
#endif

/* Define the number of bits per sample (8-bit, 16-bit, 24-bit, 32-bit) */
#ifndef AUDIO_SAMPLE_BITS
#define AUDIO_SAMPLE_BITS       16
#endif

/* Define the number of samples per second (8000, 16000, 44100, 48000) */
#ifndef AUDIO_SAMPLE_RATE
#define AUDIO_SAMPLE_RATE       16000
#endif


/* Define input and output block size */
#define IN_BLOCK_SIZE           (AUDIO_SAMPLE_RATE * (AUDIO_SAMPLE_BITS/8) * AUDIO_CHANNELS)
#define OUT_BLOCK_SIZE          (AUDIO_SAMPLE_RATE * (AUDIO_SAMPLE_BITS/8) * AUDIO_CHANNELS)

/* Define number of blocks in input and output buffers */
#define IN_BLOCK_CNT            (1U)
#define OUT_BLOCK_CNT           (1U)

/* References to the underlying CMSIS vStream driver */
extern vStreamDriver_t            Driver_vStreamAudioIn;
#define vStream_AudioIn         (&Driver_vStreamAudioIn)

extern vStreamDriver_t            Driver_vStreamAudioOut;
#define vStream_AudioOut        (&Driver_vStreamAudioOut)

/* Input and output stream buffers */
uint8_t audio_in_buf[IN_BLOCK_SIZE * IN_BLOCK_CNT]    __attribute__((aligned(32)));
uint8_t audio_out_buf[OUT_BLOCK_SIZE * OUT_BLOCK_CNT] __attribute__((aligned(32)));

/* Thread attributes */
const osThreadAttr_t thread_attr_main  = { .name = "app_main" };
const osThreadAttr_t thread_attr_stdin = { .name = "stdin"    };

/* Thread IDs */
osThreadId_t thread_id_main;
osThreadId_t thread_id_stdin;

/* Define stream related thread flags */
#define FRAME_RECEIVED          1
#define FRAME_SENT              2
#define END_OF_STREAM           4

/*
  Thread that waits for stdin characters.
*/
__NO_RETURN void thread_stdin (void *argument) {
  int ch;

  printf("Press any key to stop streaming...\n");

  while (1) {
    ch = getchar();
    if (ch != EOF) {
      /* Signal end of stream */
      osThreadFlagsSet(thread_id_main, END_OF_STREAM);
    }
    osDelay(100);
  }
}

/*
  Input Stream Event Callback
*/
void AudioIn_Event_Callback (uint32_t event) {

  if (event & VSTREAM_EVENT_DATA) {
    /* Block of input data is available */
    osThreadFlagsSet(thread_id_main, FRAME_RECEIVED);
  }

  if (event & VSTREAM_EVENT_EOS) {
    /* End of Stream event */
    osThreadFlagsSet(thread_id_main, END_OF_STREAM);
  }
}

/*
  Output Stream Event Callback
*/
void AudioOut_Event_Callback (uint32_t event) {

  if (event & VSTREAM_EVENT_DATA) {
    /* Block of audio data was output */
    osThreadFlagsSet(thread_id_main, FRAME_SENT);
  }
}

/*
  Application main thread.
*/
__NO_RETURN void app_main_thread (void *argument) {
  int32_t  rval;
  uint32_t flags;
  void *in_block;
  void *out_block;

  /* Create stdin thread */
  thread_id_stdin = osThreadNew(thread_stdin, NULL, &thread_attr_stdin);
  if (thread_id_stdin == NULL) {
    printf("Failed to create stdin thread.\n");
  }

  /* Initialize Audio Input Stream */
  rval = vStream_AudioIn->Initialize(AudioIn_Event_Callback);
  if (rval != VSTREAM_OK) {
    printf("Failed to initialize audio input stream.\n");
    for(;;);
  }

  /* Set Input Audio buffer */
  rval = vStream_AudioIn->SetBuf(audio_in_buf, sizeof(audio_in_buf), IN_BLOCK_SIZE);
  if (rval != VSTREAM_OK) {
    printf("Failed to set audio input buffer.\n");
    for(;;);
  }

  /* Initialize Audio Output Stream */
  rval = vStream_AudioOut->Initialize(AudioOut_Event_Callback);
  if (rval != VSTREAM_OK) {
    printf("Failed to initialize audio output stream.\n");
    for(;;);
  }

  /* Set Output Audio buffer */
  rval = vStream_AudioOut->SetBuf(audio_out_buf, sizeof(audio_out_buf), OUT_BLOCK_SIZE);
  if (rval != VSTREAM_OK) {
    printf("Failed to set audio output buffer.\n");
    for(;;);
  }

  /* Get a pointer to a block of memory for the output samples */
  out_block = vStream_AudioOut->GetBlock();
  if (out_block == NULL) {
    printf("Failed to get a pointer to audio output block.\n");
    for(;;);
  }

  /* Clear output frame */
  memset(out_block, 0x00, OUT_BLOCK_SIZE);

  /* Release a block of memory holding the output samples */
  rval = vStream_AudioOut->ReleaseBlock();
  if (rval != VSTREAM_OK) {
    printf("Failed to release audio output block.\n");
  }

  /* Start audio output */
  rval = vStream_AudioOut->Start(VSTREAM_MODE_CONTINUOUS);
  if (rval != VSTREAM_OK) {
    printf("Failed to start audio output stream.\n");
    for(;;);
  }

  /* Start audio capture */
  rval = vStream_AudioIn->Start(VSTREAM_MODE_CONTINUOUS);
  if (rval != VSTREAM_OK) {
    printf("Failed to start audio input stream.\n");
    for(;;);
  }

  /* Continuous streaming loop */
  while(1) {

    /* Wait for new audio input samples */
    flags = osThreadFlagsWait(FRAME_RECEIVED | END_OF_STREAM, osFlagsWaitAny, osWaitForever);

    if (flags & END_OF_STREAM) {
      /* End of Stream received, exit streaming loop */
      break;
    }
    /* Get a pointer to a block of memory holding the input samples */
    in_block = vStream_AudioIn->GetBlock();
    if (in_block == NULL) {
      printf("Failed to get a pointer to audio input block.\n");
      break;
    }

    /* Wait for available output block */
    osThreadFlagsWait(FRAME_SENT, osFlagsWaitAny, osWaitForever);

    /* Get a pointer to a block of memory for the output samples */
    out_block = vStream_AudioOut->GetBlock();
    if (out_block == NULL) {
      printf("Failed to get a pointer to audio output block.\n");
      break;
    }

    /* Copy input frame to output frame */
    memcpy(out_block, in_block, OUT_BLOCK_SIZE);

    /* Release a block of memory holding the input audio */
    rval = vStream_AudioIn->ReleaseBlock();
    if (rval != VSTREAM_OK) {
      printf("Failed to release audio input block.\n");
      break;
    }

    /* Release a block of memory holding the output audio */
    rval = vStream_AudioOut->ReleaseBlock();
    if (rval != VSTREAM_OK) {
      printf("Failed to release audio output block.\n");
      break;
    }
  }

  /* Stop input stream */
  rval = vStream_AudioIn->Stop();
  if (rval != VSTREAM_OK) {
    printf("Failed to stop input stream.\n");
    for(;;);
  }

  /* Stop output stream */
  rval = vStream_AudioOut->Stop();
  if (rval != VSTREAM_OK) {
    printf("Failed to stop output stream.\n");
    for(;;);
  }

  printf("Audio streaming stopped.\n");
  for(;;);
}

/*
  Application initialization.
*/
int app_main (void) {

  /* Initialize CMSIS-RTOS2 */
  osKernelInitialize();

  /* Create application main thread */
  thread_id_main = osThreadNew(app_main_thread, NULL, &thread_attr_main);

  /* Start thread execution */
  osKernelStart();

  return 0;
}
