/*
 * Copyright 2025-2026 Arm Limited and/or its affiliates.
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

#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "cmsis_vstream.h"

#include "cmsis_os2.h"
#include "app_main.h"
#include "app_config.h"

/* Attributes for the app_main thread */
const osThreadAttr_t thread_attr_main  = { .name = "app_main" };

/* ID of the app_main thread */
osThreadId_t thread_id_main;

/* Input and output stream buffers */
uint8_t video_in_buf[VIDEO_IN_BUF_BLOCK_SIZE * VIDEO_IN_BUF_BLOCK_CNT]    __attribute__((aligned(32)));
uint8_t video_out_buf[VIDEO_OUT_BUF_BLOCK_SIZE * VIDEO_OUT_BUF_BLOCK_CNT] __attribute__((aligned(32)));

/* Define stream related thread flags */
#define FRAME_RECEIVED          (1U << 0)
#define FRAME_SENT              (1U << 1)
#define END_OF_STREAM           (1U << 2)

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
  Initialize streams.

  This function initializes the input and output streams, registers the
  event callbacks and sets up the stream buffers.
*/
static void init_streams (void) {
  int32_t rval;
  void *out_block;

  /* Setup input stream */
  rval = vStream_VideoIn->Initialize(VideoIn_Event_Callback);
  ASSERT(rval == VSTREAM_OK);

  rval = vStream_VideoIn->SetBuf(video_in_buf, sizeof(video_in_buf), VIDEO_IN_BUF_BLOCK_SIZE);
  ASSERT(rval == VSTREAM_OK);

  /* Setup output stream */
  rval = vStream_VideoOut->Initialize(VideoOut_Event_Callback);
  ASSERT(rval == VSTREAM_OK);

  rval = vStream_VideoOut->SetBuf(video_out_buf, sizeof(video_out_buf), VIDEO_OUT_BUF_BLOCK_SIZE);
  ASSERT(rval == VSTREAM_OK);

  /* Output stream will fail to start without data to output.  */
  /* Prepare first block of data and release it to the driver. */
  out_block = vStream_VideoOut->GetBlock();
  ASSERT(out_block != NULL);

  memset(out_block, 0x00, VIDEO_OUT_BUF_BLOCK_SIZE);

  rval = vStream_VideoOut->ReleaseBlock();
  ASSERT(rval == VSTREAM_OK);
}

/*
  Application main thread.
*/
__NO_RETURN void app_main_thread (void *argument) {
  int32_t  rval;
  uint32_t count;
  uint32_t flags;
  void *in_block;
  void *out_block;

  /* Initialize input and output streams */
  init_streams();

  /* Start input and output streams */
  rval = vStream_VideoIn->Start(VSTREAM_MODE_CONTINUOUS);
  ASSERT(rval == VSTREAM_OK);

  rval = vStream_VideoOut->Start(VSTREAM_MODE_CONTINUOUS);
  ASSERT(rval == VSTREAM_OK);

  printf("Video streaming started...\n");

  /* Input to Output copy loop */
  for (count = 0; (VIDEO_TOTAL_BLOCKS == 0) || (count < VIDEO_TOTAL_BLOCKS); count++) {

    /* Wait for new video input frame */
    flags = osThreadFlagsWait(FRAME_RECEIVED | END_OF_STREAM, osFlagsWaitAny, osWaitForever);

    if (flags & END_OF_STREAM) {
      /* End of Stream received, exit streaming loop */
      break;
    }

    /* Get a pointer to a block of memory holding the input frame */
    in_block = vStream_VideoIn->GetBlock();
    ASSERT(in_block != NULL);

    /* Wait for available output frame */
    osThreadFlagsWait(FRAME_SENT, osFlagsWaitAny, osWaitForever);

    /* Get a pointer to a block of memory for the output frame */
    out_block = vStream_VideoOut->GetBlock();
    ASSERT(out_block != NULL);

    /* Copy input frame to output frame with cropping */
    frame_copy(in_block, out_block);

    /* Release a block of memory holding the input frame */
    rval = vStream_VideoIn->ReleaseBlock();
    ASSERT(rval == VSTREAM_OK);

    /* Release a block of memory holding the output frame */
    rval = vStream_VideoOut->ReleaseBlock();
    ASSERT(rval == VSTREAM_OK);
  }

  /* End of stream, stop streaming */
  rval = vStream_VideoIn->Stop();
  ASSERT(rval == VSTREAM_OK);

  rval = vStream_VideoOut->Stop();
  ASSERT(rval == VSTREAM_OK);

  printf("Video streaming stopped.\x04\n");
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
