/*
 * Copyright 2026 Arm Limited and/or its affiliates.
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
 */

#include <stdint.h>

#include "ethosu_driver.h"

/**
  \brief Cleans data-cache contents associated with buffers accessed by the NPU.

  Ensures that CPU writes to cacheable buffers are committed to memory before
  the NPU starts accessing them. Non-cacheable buffers require no cache clean,
  but the function ensures that all preceding memory accesses have completed
  before it returns.

  \param[in] base_addr       Array of buffer base addresses.
  \param[in] base_addr_size  Array containing the size, in bytes, of each buffer.
  \param[in] num_base_addr   Number of entries in the address and size arrays.
*/
void ethosu_flush_dcache(const uint64_t *base_addr, const size_t *base_addr_size, int num_base_addr) {

  for (int i = 0; i < num_base_addr; i++) {
    if ((base_addr[i] & 0x1F) != 0) {
      /* Base address must be cache line aligned (32 bytes) */
      // ...
      return;
    }

    /* Flush data-cache for current buffer */
    // ...
    // 32-bit system must cast base_addr to uint32_t* to avoid sign expansion
    // CleanDCache((uint32_t *)(uint32_t)base_addr[i], base_addr_size[i]);
  }
}

/**
  \brief Invalidates data-cache contents associated with buffers accessed by the NPU.

  Ensures that subsequent CPU reads observe data written by the NPU. Dirty
  cache lines may be cleaned before invalidation to preserve pending CPU
  writes. For non-cacheable buffers, no cache invalidation is required,
  but the function ensures that all preceding memory accesses have completed
  before it returns.

  \param[in] base_addr       Array of buffer base addresses.
  \param[in] base_addr_size  Array containing the size, in bytes, of each buffer.
  \param[in] num_base_addr   Number of entries in the address and size arrays.
*/
void ethosu_invalidate_dcache(const uint64_t *base_addr, const size_t *base_addr_size, int num_base_addr) {

  for (int i = 0; i < num_base_addr; i++) {
    if ((base_addr[i] & 0x1F) != 0) {
      /* Base address must be cache line aligned (32 bytes) */
      // ...
      return;
    }

    /* Invalidate data-cache for current buffer */
    // ...
    // 32-bit system must cast base_addr to uint32_t* to avoid sign expansion
    // InvalidateDCache((uint32_t *)(uint32_t)base_addr[i], base_addr_size[i]);
  }
}
