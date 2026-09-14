/*---------------------------------------------------------------------------
 * Copyright (c) 2024 Arm Limited (or its affiliates). All rights reserved.
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
 *---------------------------------------------------------------------------*/

#include "RTE_Components.h"
#include  CMSIS_device_header

#include "main.h"

#ifdef UART0_BASE_S_TMP
/* Workaround for UART0 CMSDK base address mismatch */
#include "uart_cmsdk_drv.h"

static const struct uart_cmsdk_dev_cfg_t UART0_CMSDK_DEV_CFG_S_TMP = {
  .base = 0x58203000 + 0x01100000,
  .default_baudrate = 115200
};
static struct uart_cmsdk_dev_data_t UART0_CMSDK_DEV_DATA_S_TMP = {
  .state = 0,
  .system_clk = 0,
  .baudrate = 0
};
struct uart_cmsdk_dev_t UART0_CMSDK_DEV_S_TMP = {
  &(UART0_CMSDK_DEV_CFG_S_TMP),
  &(UART0_CMSDK_DEV_DATA_S_TMP)
};
#endif

int main (void) {

  /* Initialize STDIO */
  stdio_init();

  #if defined(ETHOSU_ARCH)
  /* Initialize Ethos NPU */
  ethos_setup();
  #endif

  return (app_main());
}
