/*---------------------------------------------------------------------------
 * Copyright (c) 2025 Arm Limited (or its affiliates).
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
 *
 *      Name:    retarget_stdio.c
 *      Purpose: Retarget stdio to CMSIS UART
 *
 *---------------------------------------------------------------------------*/

#ifdef   CMSIS_target_header
#include CMSIS_target_header
#else
#include "Driver_USART.h"
#endif

#ifndef RETARGET_STDIO_UART
#error "RETARGET_STDIO_UART not defined!"
#endif

/* Compile-time configuration */
#ifndef UART_BAUDRATE
#define UART_BAUDRATE     115200
#endif

/* References to the external retarget functions */
extern int stdio_init     (void);
extern int stderr_putchar (int ch);
extern int stdout_putchar (int ch);
extern int stdin_getchar  (void);

/* Reference to the underlying USART driver */
#ifndef CMSIS_target_header
extern ARM_DRIVER_USART   ARM_Driver_USART_(RETARGET_STDIO_UART);
#endif
#define ptrUSART        (&ARM_Driver_USART_(RETARGET_STDIO_UART))

/**
  Initialize stdio

  \return          0 on success, or -1 on error.
*/
int stdio_init (void) {

  if (ptrUSART->Initialize(NULL) != ARM_DRIVER_OK) {
    return -1;
  }

  if (ptrUSART->PowerControl(ARM_POWER_FULL) != ARM_DRIVER_OK) {
    return -1;
  }

  if (ptrUSART->Control(ARM_USART_MODE_ASYNCHRONOUS |
                        ARM_USART_DATA_BITS_8       |
                        ARM_USART_PARITY_NONE       |
                        ARM_USART_STOP_BITS_1       |
                        ARM_USART_FLOW_CONTROL_NONE,
                        UART_BAUDRATE) != ARM_DRIVER_OK) {
    return -1;
  }

  if (ptrUSART->Control(ARM_USART_CONTROL_RX, 1U) != ARM_DRIVER_OK) {
    return -1;
  }

  if (ptrUSART->Control(ARM_USART_CONTROL_TX, 1U) != ARM_DRIVER_OK) {
    return -1;
  }

  return 0;
}

/**
  Put a character to the stderr

  \param[in]   ch  Character to output
  \return          The character written, or -1 on write error.
*/
int stderr_putchar (int ch) {
  uint8_t buf[1];

  if (ch == '\n') {
    buf[0] = (uint8_t)'\r';

    if (ptrUSART->Send(buf, 1U) != ARM_DRIVER_OK) {
      return -1;
    }

    while (ptrUSART->GetStatus().tx_busy != 0U);
  }

  buf[0] = (uint8_t)ch;

  if (ptrUSART->Send(buf, 1U) != ARM_DRIVER_OK) {
    return -1;
  }

  while (ptrUSART->GetStatus().tx_busy != 0U);

  return ch;
}

/**
  Put a character to the stdout

  \param[in]   ch  Character to output
  \return          The character written, or -1 on write error.
*/
int stdout_putchar (int ch) {
  uint8_t buf[1];

  if (ch == '\n') {
    buf[0] = (uint8_t)'\r';

    if (ptrUSART->Send(buf, 1U) != ARM_DRIVER_OK) {
      return -1;
    }

    while (ptrUSART->GetStatus().tx_busy != 0U);
  }

  buf[0] = (uint8_t)ch;

  if (ptrUSART->Send(buf, 1U) != ARM_DRIVER_OK) {
    return -1;
  }

  while (ptrUSART->GetStatus().tx_busy != 0U);

  return ch;
}

/**
  Get a character from the stdio

  \return     The next character from the input, or -1 on read error.
*/
int stdin_getchar (void) {
  uint8_t buf[1];

  if (ptrUSART->Receive(buf, 1U) != ARM_DRIVER_OK) {
    return -1;
  }

  while (ptrUSART->GetStatus().rx_busy != 0U);

  return (int)buf[0];
}