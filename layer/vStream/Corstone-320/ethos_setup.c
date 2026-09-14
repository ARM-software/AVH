/*---------------------------------------------------------------------------
 * Copyright (c) 2025 Arm Limited (or its affiliates). All rights reserved.
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

 #include <stdio.h>

#include "RTE_Components.h"
#include  CMSIS_device_header

#include "ethosu_driver.h"
#include "main.h"

#if defined(ETHOSU65) || defined(ETHOSU85)
/* Define Ethos-U NPU cache buffer size */
#ifndef ETHOS_CACHE_BUF_SIZE
#define ETHOS_CACHE_BUF_SIZE        393216
#endif

/* Define Ethos-U cache buffer alignment */
#ifndef ETHOS_CACHE_BUF_ALIGNMENT
#define ETHOS_CACHE_BUF_ALIGNMENT   32
#endif

/* Define Ethos-U NPU cache buffer attributes */
#ifndef ETHOS_CACHE_BUF_ATTRIBUTES
#define ETHOS_CACHE_BUF_ATTRIBUTES  __attribute__((section("ethos_cache_buf"), aligned(ETHOS_CACHE_BUF_ALIGNMENT)))
#endif
#endif

/* Define Ethos-U NPU security mode */
#ifndef ETHOS_SECURE_ENABLE
#define ETHOS_SECURE_ENABLE         1
#endif

/* Define Ethos-U NPU privilege mode */
#ifndef ETHOS_PRIVILEGE_ENABLE
#define ETHOS_PRIVILEGE_ENABLE      1
#endif

/* Ethos NPU driver instance. */
static struct ethosu_driver EthosDriver;

#if defined(ETHOSU65) || defined(ETHOSU85)
static uint8_t ethos_cache[ETHOS_CACHE_BUF_SIZE] ETHOS_CACHE_BUF_ATTRIBUTES;
#endif

/*
  Ethos NPU interrupt handler.
*/
void NPU0_Handler(void) {
  ethosu_irq_handler(&EthosDriver);
}

/*
  Initialize the Ethos NPU driver.
*/
void ethos_setup (void) {
  void * const ethos_base_addr = (void *)NPU0_APB_BASE_S;
  struct ethosu_hw_info hw_info;
  int rval;

  /*  Initialize Ethos-U NPU driver. */
  rval = ethosu_init(&EthosDriver,            /* Ethos-U device driver */
                     ethos_base_addr,         /* Ethos-U base address  */
                     #if defined(ETHOSU65) || defined(ETHOSU85)
                     ethos_cache,             /* Cache memory pointer  */
                     sizeof(ethos_cache),     /* Cache memory size     */
                     #else
                     0,                       /* Cache memory pointer  */
                     0,                       /* Cache memory size     */
                     #endif
                     ETHOS_SECURE_ENABLE,     /* Secure enable         */
                     ETHOS_PRIVILEGE_ENABLE); /* Privileged mode       */
  if (rval != 0) {
    printf("Failed to initialize Arm Ethos-U driver\n");
  }
  else {
    NVIC_EnableIRQ(NPU0_IRQn);

    ethosu_get_hw_info(&EthosDriver, &hw_info);

    printf("Ethos-U version info:\n");
    printf("\tArch:       v%u.%u.%u\n", hw_info.version.arch_major_rev,
                                        hw_info.version.arch_minor_rev,
                                        hw_info.version.arch_patch_rev);
    printf("\tMACs/cc:    %u\n", (uint32_t)(1 << hw_info.cfg.macs_per_cc));
    printf("\tCmd stream: v%u\n", hw_info.cfg.cmd_stream_version);
  }
}
