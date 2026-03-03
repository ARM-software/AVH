/*---------------------------------------------------------------------------
 * Copyright (c) 2026 Arm Limited (or its affiliates).
 * All rights reserved.
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
 * --------------------------------------------------------------------------
 *
 * Purpose:   STDIO to CMSIS Driver USART Retarget Configuration
 * Revision:  V1.0.0
 *
 * --------------------------------------------------------------------------*/

#ifndef STDIO_CMSIS_UART_CONFIG_H_
#define STDIO_CMSIS_UART_CONFIG_H_

#ifdef   CMSIS_target_header
#include CMSIS_target_header
#else
#define RETARGET_STDIO_UART       0
#endif

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------
//------ With VS Code: Open Preview for Configuration Wizard -------------------

// <y>Connect to hardware via Driver_USART#
// <i> Select driver control block for hardware interface
// <i> Default: 0
#ifndef STDIO_UART_DRIVER
#define STDIO_UART_DRIVER         RETARGET_STDIO_UART
#endif

// <o>UART baudrate
// <i> Specifies the baudrate for UART communication
// <i> Common values: 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600
// <i> Default: 115200
#ifndef STDIO_UART_BAUDRATE
#define STDIO_UART_BAUDRATE       115200
#endif

#endif /* STDIO_CMSIS_UART_CONFIG_H_ */
