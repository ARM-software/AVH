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

#ifndef APP_CONFIG_H_
#define APP_CONFIG_H_

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------
//------ With VS Code: Open Preview for Configuration Wizard -------------------


// <o> Stream duration (seconds)
// <i> Defines the streaming duration in seconds.
// <i> Default: 0 (stream indefinitely)
#ifndef VIDEO_STREAM_DURATION
#define VIDEO_STREAM_DURATION   0
#endif

// <h>Video Configuration
// ======================

//  <o>Input Frame Width
//  <i> Define the input video frame width.
//  <i> Default: 640
#ifndef VIDEO_IN_FRAME_WIDTH
#define VIDEO_IN_FRAME_WIDTH    640
#endif

//  <o>Input Frame Height
//  <i> Define the input video frame height.
//  <i> Default: 480
#ifndef VIDEO_IN_FRAME_HEIGHT
#define VIDEO_IN_FRAME_HEIGHT   480
#endif

//  <o>Output Frame Width
//  <i> Define the output video frame width.
//  <i> Default: 640
#ifndef VIDEO_OUT_FRAME_WIDTH
#define VIDEO_OUT_FRAME_WIDTH   640
#endif

//  <o>Output Frame Height
//  <i> Define the output video frame height.
//  <i> Default: 480
#ifndef VIDEO_OUT_FRAME_HEIGHT
#define VIDEO_OUT_FRAME_HEIGHT  480
#endif

// <o>Frame Rate
// <i> Define the video frame rate in frames per second (fps).
// <i> Default: 30
#ifndef VIDEO_FRAME_RATE
#define VIDEO_FRAME_RATE        30
#endif

// </h>

#endif /* APP_CONFIG_H_ */
