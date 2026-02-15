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

#ifndef VSTREAM_AUDIO_OUT_CONFIG_H_
#define VSTREAM_AUDIO_OUT_CONFIG_H_

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------
//------ With VS Code: Open Preview for Configuration Wizard -------------------

// <o> Number of channels <1=>Mono <2=>Stereo
// <i> Defines the number of audio channels in stream.
// <i> Default: 2
#ifndef AUDIO_OUT_CHANNELS
#define AUDIO_OUT_CHANNELS        2
#endif

// <o> Number of bits per sample <0=>8 <1=>16 <2=>24 <3=>32
// <i> Defines number of bits of information in each sample.
// <i> Default: 16
#ifndef AUDIO_OUT_SAMPLE_BITS
#define AUDIO_OUT_SAMPLE_BITS     16
#endif

// <o> Sample rate <8000=>8 kHz <16000=>16 kHz <44100=>44.1 kHz <48000=>48 kHz
// <i> Defines the number of samples captured per second.
// <i> Default: 16000
#ifndef AUDIO_OUT_SAMPLE_RATE
#define AUDIO_OUT_SAMPLE_RATE     16000
#endif

// <o> Streaming Device Index
// <i> Defines the system index of the audio streaming device.
// <i> Default: -1 (system default audio device)
#ifndef AUDIO_OUT_DEVICE
#define AUDIO_OUT_DEVICE          -1
#endif

// <s> Audio File Name
// <i> Defines the name of the audio file to be used for streaming.
// <i> Default: "" (use streaming device instead of file)
#ifndef AUDIO_OUT_FILENAME
#define AUDIO_OUT_FILENAME        "./sample/audio_out.wav"
#endif

#endif
