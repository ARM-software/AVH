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

#ifndef VSTREAM_VIDEO_OUT_CONFIG_H_
#define VSTREAM_VIDEO_OUT_CONFIG_H_

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------
//------ With VS Code: Open Preview for Configuration Wizard -------------------

// <o> Frame width
// <i> Defines the video stream frame width in pixels.
#ifndef VIDEO_OUT_FRAME_WIDTH
#define VIDEO_OUT_FRAME_WIDTH     320
#endif

// <o> Frame height
// <i> Defines the video stream frame height in pixels.
#ifndef VIDEO_OUT_FRAME_HEIGHT
#define VIDEO_OUT_FRAME_HEIGHT    240
#endif

// <o> Frame rate
// <i> Defines the video stream frame rate in frames per second.
#ifndef VIDEO_OUT_FRAME_RATE
#define VIDEO_OUT_FRAME_RATE      30
#endif

// <o> Color format <0=>Grayscale(8-bit) <1=>RGB888 <2=>BGR565 <3=>YUV420 <4=>NV12 <5=>NV21
// <i> Defines the video frame color space.
#ifndef VIDEO_OUT_FRAME_COLOR
#define VIDEO_OUT_FRAME_COLOR     1
#endif

#endif
