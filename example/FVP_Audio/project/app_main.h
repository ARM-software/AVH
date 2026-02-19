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

#include "vstream_audio_in.h"
#include "vstream_audio_out.h"

#include "app_config.h"

/* References to the underlying CMSIS vStream driver */
#define vStream_AudioIn         (&Driver_vStreamAudioIn)
#define vStream_AudioOut        (&Driver_vStreamAudioOut)

/* The size of one data block that holds 100ms of audio samples */
#define AUDIO_BUF_BLOCK_SIZE    (AUDIO_SAMPLE_RATE * (AUDIO_SAMPLE_BITS/8) * AUDIO_CHANNELS / 10)

/* The number of blocks in audio buffer */
#define AUDIO_BUF_BLOCK_CNT     (2U)

/* Determine how many blocks to transfer for the required streaming duration */
#define AUDIO_TOTAL_BLOCKS      ((AUDIO_STREAM_DURATION * AUDIO_SAMPLE_RATE) / (AUDIO_BUF_BLOCK_SIZE / (AUDIO_SAMPLE_BITS/8) / AUDIO_CHANNELS))

/* Custom assert that uses stdout instead of stderr */
#ifndef ASSERT
#define ASSERT(expr)            do { \
                                  if (!(expr)) { \
                                    printf("ASSERT FAILED: %s, %s, line %d\n", #expr, __FILE__, __LINE__); \
                                    for(;;); \
                                  } \
                                } while (0)
#endif


#endif /* APP_MAIN_H_ */
