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
 * Purpose:   Configure STDOUT to CMSIS-Driver USART retarget implementation
 * Revision:  V1.0.0
 *
 * --------------------------------------------------------------------------*/

#ifndef STDOUT_CMSIS_UART_CONFIG_H_
#define STDOUT_CMSIS_UART_CONFIG_H_

//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------
//------ With VS Code: Open Preview for Configuration Wizard -------------------

// <o>UART STDOUT Buffer Size
// <i> UART STDOUT buffer is used to store STDOUT data before sending it via UART
// <i> Default: 0 (unbuffered)
#ifndef STDOUT_UART_BUFFER_SIZE
#define STDOUT_UART_BUFFER_SIZE         0
#endif

// <s>UART STDOUT Buffer Section Name
// <i> Specify the memory section name for UART STDOUT buffer
// <i> Default: .stdout_uart_buf
#ifndef STDOUT_UART_BUFFER_SECTION
#define STDOUT_UART_BUFFER_SECTION      ".stdout_uart_buf"
#endif

// <o>UART STDOUT Buffer Alignment
// <i> Define the buffer alignment in bytes
// <i> Default: 32
#ifndef STDOUT_UART_BUFFER_ALIGNMENT
#define STDOUT_UART_BUFFER_ALIGNMENT    32
#endif

// <q>Convert LF to CRLF
// <i> If enabled, LF characters are preceded by CR characters on output
// <i> Default: 0
#ifndef STDOUT_CR_LF
#define STDOUT_CR_LF                    0
#endif

#endif /* STDOUT_CMSIS_UART_CONFIG_H_ */
