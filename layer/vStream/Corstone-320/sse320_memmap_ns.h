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

#ifndef SSE320_MEMMAP_NS_H
#define SSE320_MEMMAP_NS_H

/*============================================================================*/
/*                           NON-SECURE MEMORY REGIONS                        */
/*============================================================================*/

/*---------------------------------------------------------------------------*/
/*                        Non-Secure Code Regions                            */
/*---------------------------------------------------------------------------*/

/* ITCM - Non-Secure */
#define ITCM_NS_BASE                    0x00000000
#define ITCM_NS_SIZE                    0x00008000    /* 32KB */
#define ITCM_NS_LIMIT                   (ITCM_NS_BASE + ITCM_NS_SIZE - 1)

/* FPGA SRAM - Non-Secure */
#define FPGA_SRAM_NS_BASE               0x01000000
#define FPGA_SRAM_NS_SIZE               0x00200000    /* 2MB */
#define FPGA_SRAM_NS_LIMIT              (FPGA_SRAM_NS_BASE + FPGA_SRAM_NS_SIZE - 1)

/* DMA ITCM - Non-Secure */
#define DMA_ITCM_NS_BASE                0x0A000000
#define DMA_ITCM_NS_SIZE                0x00008000    /* 32KB */
#define DMA_ITCM_NS_LIMIT               (DMA_ITCM_NS_BASE + DMA_ITCM_NS_SIZE - 1)

/*---------------------------------------------------------------------------*/
/*                         Non-Secure SRAM Regions                           */
/*---------------------------------------------------------------------------*/

/* DTCM - Non-Secure */
#define DTCM_NS_BASE                    0x20000000
#define DTCM_NS_SIZE                    0x00008000    /* 32KB */
#define DTCM_NS_LIMIT                   (DTCM_NS_BASE + DTCM_NS_SIZE - 1)

/* SRAM VM0 - Non-Secure */
#define SRAM_VM0_NS_BASE                0x21000000
#define SRAM_VM0_NS_SIZE                0x00200000    /* 2MB */
#define SRAM_VM0_NS_LIMIT               (SRAM_VM0_NS_BASE + SRAM_VM0_NS_SIZE - 1)

/* SRAM VM1 - Non-Secure */
#define SRAM_VM1_NS_BASE                0x21200000
#define SRAM_VM1_NS_SIZE                0x00200000    /* 2MB */
#define SRAM_VM1_NS_LIMIT               (SRAM_VM1_NS_BASE + SRAM_VM1_NS_SIZE - 1)

/* DMA DTCM - Non-Secure */
#define DMA_DTCM_NS_BASE                0x24000000
#define DMA_DTCM_NS_SIZE                0x00008000    /* 32KB */
#define DMA_DTCM_NS_LIMIT               (DMA_DTCM_NS_BASE + DMA_DTCM_NS_SIZE - 1)

/*---------------------------------------------------------------------------*/
/*                       Non-Secure Flash Regions                            */
/*---------------------------------------------------------------------------*/

/* QSPI Flash - Non-Secure */
#define QSPI_FLASH_NS_BASE              0x28000000
#define QSPI_FLASH_NS_SIZE              0x08000000    /* 128MB */
#define QSPI_FLASH_NS_LIMIT             (QSPI_FLASH_NS_BASE + QSPI_FLASH_NS_SIZE - 1)

/*---------------------------------------------------------------------------*/
/*                        Non-Secure DDR4 Regions                            */
/*---------------------------------------------------------------------------*/

/* DDR4 Region 0 - Non-Secure */
#define DDR4_0_NS_BASE                  0x60000000
#define DDR4_0_NS_SIZE                  0x10000000    /* 256MB */
#define DDR4_0_NS_LIMIT                 (DDR4_0_NS_BASE + DDR4_0_NS_SIZE - 1)

/* DDR4 Region 2 - Non-Secure */
#define DDR4_2_NS_BASE                  0x80000000
#define DDR4_2_NS_SIZE                  0x10000000    /* 256MB */
#define DDR4_2_NS_LIMIT                 (DDR4_2_NS_BASE + DDR4_2_NS_SIZE - 1)

/* DDR4 Region 4 - Non-Secure */
#define DDR4_4_NS_BASE                  0xA0000000
#define DDR4_4_NS_SIZE                  0x10000000    /* 256MB */
#define DDR4_4_NS_LIMIT                 (DDR4_4_NS_BASE + DDR4_4_NS_SIZE - 1)

/* DDR4 Region 6 - Non-Secure */
#define DDR4_6_NS_BASE                  0xC0000000
#define DDR4_6_NS_SIZE                  0x10000000    /* 256MB */
#define DDR4_6_NS_LIMIT                 (DDR4_6_NS_BASE + DDR4_6_NS_SIZE - 1)

#endif /* SSE320_MEMMAP_NS_H */
