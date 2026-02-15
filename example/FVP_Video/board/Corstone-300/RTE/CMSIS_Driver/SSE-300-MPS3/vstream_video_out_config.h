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
// <i> Common frame widths: 320, 640, 800, 1024.
// <i> Default: 640
#ifndef VIDEO_OUT_FRAME_WIDTH
#define VIDEO_OUT_FRAME_WIDTH     640
#endif

// <o> Frame height
// <i> Defines the video stream frame height in pixels.
// <i> Common frame heights: 240, 480, 600, 768.
// <i> Default: 480
#ifndef VIDEO_OUT_FRAME_HEIGHT
#define VIDEO_OUT_FRAME_HEIGHT    480
#endif

// <o> Frame rate
// <i> Defines the video stream frame rate in frames per second.
// <i> Common frame rates: 15, 25, 30, 60.
// <i> Default: 30
#ifndef VIDEO_OUT_FRAME_RATE
#define VIDEO_OUT_FRAME_RATE      30
#endif

// <o> Color format <0=>Grayscale(8-bit) <1=>RGB888 <2=>BGR565 <3=>YUV420 <4=>NV12 <5=>NV21
// <i> Defines the video frame color space.
// <i> Default: 1
#ifndef VIDEO_OUT_FRAME_COLOR
#define VIDEO_OUT_FRAME_COLOR     1
#endif

// <s> Video File Name
// <i> Defines the name of the video file to be used for streaming.
// <i> Default: "" (use streaming device instead of file)
#ifndef VIDEO_OUT_FILENAME
#define VIDEO_OUT_FILENAME        "./sample/video_out.mp4"
#endif

#endif
