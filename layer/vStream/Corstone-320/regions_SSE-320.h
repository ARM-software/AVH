#ifndef REGIONS_SSE_320_H
#define REGIONS_SSE_320_H

#include "sse320_memmap_s.h"
#include "sse320_memmap_ns.h"


//-------- <<< Use Configuration Wizard in Context Menu >>> --------------------
//------ With VS Code: Open Preview for Configuration Wizard -------------------

// <h> ROM Configuration
// =======================
// <h> __ROM0
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Contains Startup and Vector Table
//   <i> Default: BOOT_ROM_S_BASE
#define __ROM0_BASE   BOOT_ROM_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: BOOT_ROM_S_SIZE
#define __ROM0_SIZE   BOOT_ROM_S_SIZE
// </h>

// <h> __ROM1
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: FPGA_SRAM_S_BASE
#define __ROM1_BASE   FPGA_SRAM_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: FPGA_SRAM_S_SIZE
#define __ROM1_SIZE   FPGA_SRAM_S_SIZE
// </h>

// <h> __ROM2
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: DDR4_3_S_BASE
#define __ROM2_BASE   DDR4_3_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: DDR4_3_S_SIZE
#define __ROM2_SIZE   DDR4_3_S_SIZE
// </h>

// <h> __ROM3
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: QSPI_FLASH_S_BASE
#define __ROM3_BASE   QSPI_FLASH_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: QSPI_FLASH_S_SIZE
#define __ROM3_SIZE   QSPI_FLASH_S_SIZE
// </h>

// </h>

// <h> RAM Configuration
// =======================
// <h> __RAM0
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: DDR4_1_S_BASE
#define __RAM0_BASE   DDR4_1_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: DDR4_1_S_SIZE
#define __RAM0_SIZE   DDR4_1_S_SIZE
// </h>

// <h> __RAM1
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: SRAM_VM0_S_BASE
#define __RAM1_BASE   SRAM_VM0_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: SRAM_VM0_S_SIZE
#define __RAM1_SIZE   SRAM_VM0_S_SIZE
// </h>

// <h> __RAM2
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: SRAM_VM1_S_BASE
#define __RAM2_BASE   SRAM_VM1_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: SRAM_VM1_S_SIZE
#define __RAM2_SIZE   SRAM_VM1_S_SIZE
// </h>

// <h> __RAM3
//   <y> Base address
//   <i> Defines base address of memory region.
//   <i> Default: DTCM_S_BASE
#define __RAM3_BASE   DTCM_S_BASE
//   <y> Region size [bytes]
//   <i> Defines size of memory region.
//   <i> Default: DTCM_S_SIZE
#define __RAM3_SIZE   DTCM_S_SIZE
// </h>

// </h>

// <h> Stack / Heap Configuration
//   <o0> Stack Size (in Bytes) <0x0-0xFFFFFFFF:8>
//   <o1> Heap Size (in Bytes) <0x0-0xFFFFFFFF:8>
#define __STACK_SIZE  0x00001000
#define __HEAP_SIZE   0x00018000
// </h>

#endif /* REGIONS_SSE_320_H */
