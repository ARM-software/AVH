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

#ifndef CORSTONE_310_H_
#define CORSTONE_310_H_

#include "Driver_USART.h"
#include "cmsis_vstream.h"

// CMSIS Driver instances of Board peripherals
#define CMSIS_DRIVER_USART  0  // CMSIS Driver USART instance number

// Retarget stdio to CMSIS UART
#define RETARGET_STDIO_UART 0

// CMSIS Drivers
extern ARM_DRIVER_USART Driver_USART0;          /* Serial           */
extern vStreamDriver_t  Driver_vStreamAudioIn;  /* Audio In Stream  */
extern vStreamDriver_t  Driver_vStreamAudioOut; /* Audio Out Stream */
extern vStreamDriver_t  Driver_vStreamVideoIn;  /* Video In Stream  */
extern vStreamDriver_t  Driver_vStreamVideoOut; /* Video Out Stream */

#ifdef CMSIS_shield_header
#include CMSIS_shield_header
#endif

#endif /* CORSTONE_310_H_ */
