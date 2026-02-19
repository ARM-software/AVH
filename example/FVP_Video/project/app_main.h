/*
 * Copyright 2026 Arm Limited and/or its affiliates.
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

#ifndef APP_MAIN_H_
#define APP_MAIN_H_

#include <stdio.h>

#include "vstream_video_in.h"
#include "vstream_video_out.h"

#include "app_config.h"

/* References to the underlying CMSIS vStream driver */
#define vStream_VideoIn           (&Driver_vStreamVideoIn)
#define vStream_VideoOut          (&Driver_vStreamVideoOut)

/* Number of bytes per pixel for RGB888 format */
#define VIDEO_PIXEL_SIZE          (3U)

/* The size of data blocks that hold one video frame */
#define VIDEO_IN_BUF_BLOCK_SIZE   (VIDEO_IN_FRAME_WIDTH * VIDEO_IN_FRAME_HEIGHT * VIDEO_PIXEL_SIZE)
#define VIDEO_OUT_BUF_BLOCK_SIZE  (VIDEO_OUT_FRAME_WIDTH * VIDEO_OUT_FRAME_HEIGHT * VIDEO_PIXEL_SIZE)

/* The number of blocks in video buffer */
#define VIDEO_IN_BUF_BLOCK_CNT    (2U)
#define VIDEO_OUT_BUF_BLOCK_CNT   (2U)

/* Determine how many blocks to transfer for the required streaming duration */
#define VIDEO_TOTAL_BLOCKS        (VIDEO_STREAM_DURATION * VIDEO_FRAME_RATE)

/* Custom assert that uses stdout instead of stderr */
#ifndef ASSERT
#define ASSERT(expr)              do { \
                                    if (!(expr)) { \
                                      printf("ASSERT FAILED: %s, %s, line %d\n", #expr, __FILE__, __LINE__); \
                                      for(;;); \
                                    } \
                                  } while (0)
#endif

/* Function to copy a video frame from input to output */
extern int32_t frame_copy(const void *in_frame, void *out_frame);

#endif /* APP_MAIN_H_ */
