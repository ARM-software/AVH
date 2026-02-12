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


/* Define the video stream frame width in pixels. */
#ifndef VIDEO_FRAME_WIDTH
#define VIDEO_FRAME_WIDTH       640
#endif

/* Define the video stream frame height in pixels. */
#ifndef VIDEO_FRAME_HEIGHT
#define VIDEO_FRAME_HEIGHT      480
#endif

/* Define the video stream bytes per pixel */
#ifndef VIDEO_PIXEL_SIZE 
#define VIDEO_PIXEL_SIZE        3
#endif


/* Define input and output block size (frame width x frame height x bytes per pixel) */
#define IN_BLOCK_SIZE           (VIDEO_FRAME_WIDTH  * VIDEO_FRAME_HEIGHT  * VIDEO_PIXEL_SIZE)
#define OUT_BLOCK_SIZE          (VIDEO_FRAME_WIDTH  * VIDEO_FRAME_HEIGHT  * VIDEO_PIXEL_SIZE)

/* Define number of blocks in input and output buffers */
#define IN_BLOCK_CNT            (2U)
#define OUT_BLOCK_CNT           (2U)

/* References to the underlying CMSIS vStream driver */
extern vStreamDriver_t            Driver_vStreamVideoIn;
#define vStream_VideoIn         (&Driver_vStreamVideoIn)

extern vStreamDriver_t            Driver_vStreamVideoOut;
#define vStream_VideoOut        (&Driver_vStreamVideoOut)


/* Input and output stream buffers */
uint8_t video_in_buf[IN_BLOCK_SIZE * IN_BLOCK_CNT]    __attribute__((aligned(32)));
uint8_t video_out_buf[OUT_BLOCK_SIZE * OUT_BLOCK_CNT] __attribute__((aligned(32)));

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
void VideoIn_Event_Callback (uint32_t event) {

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
void VideoOut_Event_Callback (uint32_t event) {

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

  /* Initialize Video Input Stream */
  rval = vStream_VideoIn->Initialize(VideoIn_Event_Callback);
  if (rval != VSTREAM_OK) {
    printf("Failed to initialize video input stream.\n");
    for(;;);
  }

  /* Set Input Video buffer */
  rval = vStream_VideoIn->SetBuf(video_in_buf, sizeof(video_in_buf), IN_BLOCK_SIZE);
  if (rval != VSTREAM_OK) {
    printf("Failed to set video input buffer.\n");
    for(;;);
  }

  /* Initialize Video Output Stream */
  rval = vStream_VideoOut->Initialize(VideoOut_Event_Callback);
  if (rval != VSTREAM_OK) {
    printf("Failed to initialize video output stream.\n");
    for(;;);
  }

  /* Set Output Video buffer */
  rval = vStream_VideoOut->SetBuf(video_out_buf, sizeof(video_out_buf), OUT_BLOCK_SIZE);
  if (rval != VSTREAM_OK) {
    printf("Failed to set video output buffer.\n");
    for(;;);
  }

  /* Get a pointer to a block of memory for the output frame */
  out_block = vStream_VideoOut->GetBlock();
  if (out_block == NULL) {
    printf("Failed to get a pointer to video output block.\n");
    for(;;);
  }

  /* Clear output frame */
  memset(out_block, 0x00, OUT_BLOCK_SIZE);

  /* Release a block of memory holding the output frame */
  rval = vStream_VideoOut->ReleaseBlock();
  if (rval != VSTREAM_OK) {
    printf("Failed to release video output block.\n");
  }

  /* Start video output */
  rval = vStream_VideoOut->Start(VSTREAM_MODE_CONTINUOUS);
  if (rval != VSTREAM_OK) {
    printf("Failed to start video output stream.\n");
    for(;;);
  }

  /* Start video capture */
  rval = vStream_VideoIn->Start(VSTREAM_MODE_CONTINUOUS);
  if (rval != VSTREAM_OK) {
    printf("Failed to start video input stream.\n");
    for(;;);
  }

  /* Continuous streaming loop */
  while(1) {

    /* Wait for new video input frame */
    flags = osThreadFlagsWait(FRAME_RECEIVED | END_OF_STREAM, osFlagsWaitAny, osWaitForever);

    if (flags & END_OF_STREAM) {
      /* End of Stream received, exit streaming loop */
      break;
    }

    /* Get a pointer to a block of memory holding the input frame */
    in_block = vStream_VideoIn->GetBlock();
    if (in_block == NULL) {
      printf("Failed to get a pointer to video input block.\n");
      break;
    }

    /* Wait for available output frame */
    osThreadFlagsWait(FRAME_SENT, osFlagsWaitAny, osWaitForever);

    /* Get a pointer to a block of memory for the output frame */
    out_block = vStream_VideoOut->GetBlock();
    if (out_block == NULL) {
      printf("Failed to get a pointer to video output block.\n");
      break;
    }

    /* Copy input frame to output frame */
    memcpy(out_block, in_block, OUT_BLOCK_SIZE);


    /* Release a block of memory holding the input frame */
    rval = vStream_VideoIn->ReleaseBlock();
    if (rval != VSTREAM_OK) {
      printf("Failed to release video input block.\n");
      break;
    }

    /* Release a block of memory holding the output frame */
    rval = vStream_VideoOut->ReleaseBlock();
    if (rval != VSTREAM_OK) {
      printf("Failed to release video output block.\n");
      break;
    }
  }

  /* Stop input stream */
  rval = vStream_VideoIn->Stop();
  if (rval != VSTREAM_OK) {
    printf("Failed to stop input stream.\n");
    for(;;);
  }

  /* Stop output stream */
  rval = vStream_VideoOut->Stop();
  if (rval != VSTREAM_OK) {
    printf("Failed to stop output stream.\n");
    for(;;);
  }

  printf("Video streaming stopped.\n");
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
