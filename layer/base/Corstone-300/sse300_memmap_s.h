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

#ifndef SSE300_MEMMAP_S_H
#define SSE300_MEMMAP_S_H

/*============================================================================*/
/*                             SECURE MEMORY REGIONS                          */
/*============================================================================*/

/*---------------------------------------------------------------------------*/
/*                          Secure Code Regions                              */
/*---------------------------------------------------------------------------*/

/* ITCM - Secure (Startup) */
#define ITCM_S_BASE                     0x10000000
#define ITCM_S_SIZE                     0x00080000    /* 512KB */
#define ITCM_S_LIMIT                    (ITCM_S_BASE + ITCM_S_SIZE - 1)

/* FPGA SRAM - Secure */
#define FPGA_SRAM_S_BASE                0x11000000
#define FPGA_SRAM_S_SIZE                0x00100000    /* 1MB */
#define FPGA_SRAM_S_LIMIT               (FPGA_SRAM_S_BASE + FPGA_SRAM_S_SIZE - 1)

/*---------------------------------------------------------------------------*/
/*                           Secure SRAM Regions                             */
/*---------------------------------------------------------------------------*/

/* DTCM - Secure */
#define DTCM_S_BASE                     0x30000000
#define DTCM_S_SIZE                     0x00080000    /* 512KB */
#define DTCM_S_LIMIT                    (DTCM_S_BASE + DTCM_S_SIZE - 1)

/* SRAM VM0 - Secure */
#define SRAM_VM0_S_BASE                 0x31000000
#define SRAM_VM0_S_SIZE                 0x00100000    /* 1MB */
#define SRAM_VM0_S_LIMIT                (SRAM_VM0_S_BASE + SRAM_VM0_S_SIZE - 1)

/* SRAM VM1 - Secure */
#define SRAM_VM1_S_BASE                 0x31100000
#define SRAM_VM1_S_SIZE                 0x00100000    /* 1MB */
#define SRAM_VM1_S_LIMIT                (SRAM_VM1_S_BASE + SRAM_VM1_S_SIZE - 1)

/*---------------------------------------------------------------------------*/
/*                         Secure QSPI Flash Regions                         */
/*---------------------------------------------------------------------------*/

/* QSPI Flash - Secure */
#define QSPI_FLASH_S_BASE               0x38000000
#define QSPI_FLASH_S_SIZE               0x00800000    /* 8MB */
#define QSPI_FLASH_S_LIMIT              (QSPI_FLASH_S_BASE + QSPI_FLASH_S_SIZE - 1)

/*---------------------------------------------------------------------------*/
/*                          Secure DDR4 Regions                              */
/*---------------------------------------------------------------------------*/

/* DDR4 Region 1 - Secure */
#define DDR4_1_S_BASE                   0x70000000
#define DDR4_1_S_SIZE                   0x10000000    /* 256MB */
#define DDR4_1_S_LIMIT                  (DDR4_1_S_BASE + DDR4_1_S_SIZE - 1)

/* DDR4 Region 3 - Secure */
#define DDR4_3_S_BASE                   0x90000000
#define DDR4_3_S_SIZE                   0x10000000    /* 256MB */
#define DDR4_3_S_LIMIT                  (DDR4_3_S_BASE + DDR4_3_S_SIZE - 1)

/* DDR4 Region 5 - Secure */
#define DDR4_5_S_BASE                   0xB0000000
#define DDR4_5_S_SIZE                   0x10000000    /* 256MB */
#define DDR4_5_S_LIMIT                  (DDR4_5_S_BASE + DDR4_5_S_SIZE - 1)

/* DDR4 Region 7 - Secure */
#define DDR4_7_S_BASE                   0xD0000000
#define DDR4_7_S_SIZE                   0x10000000    /* 256MB */
#define DDR4_7_S_LIMIT                  (DDR4_7_S_BASE + DDR4_7_S_SIZE - 1)

#endif /* SSE300_MEMMAP_S_H */
