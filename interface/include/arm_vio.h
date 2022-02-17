/*
 * Copyright (c) 2021-2022 Arm Limited. All rights reserved.
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

/*
 * Virtual Input/Output (VIO)
 */

#ifndef __ARM_VIO_H
#define __ARM_VIO_H

#ifdef __cplusplus
extern "C" {
#endif

#ifndef __IM
#define __IM  volatile const    /*! Defines 'read only' structure member permissions */
#endif
#ifndef __OM
#define __OM  volatile          /*! Defines 'write only' structure member permissions */
#endif
#ifndef __IOM
#define __IOM volatile          /*! Defines 'read/write' structure member permissions */
#endif

#include <stdint.h>

/// Structure type to access the virtual input/output.
typedef struct
{
  /// Signal Output
  struct {
    __IOM uint32_t mask;        /*!< (R/W) Bit Mask */
    __OM  uint32_t signal;      /*!< (-/W) Signal Value */
  } SignalOut;
  /// Signal Input
  struct {
    __IOM uint32_t mask;        /*!< (R/W) Bit Mask */
    __IM  uint32_t signal;      /*!< (R/-) Signal Value */
  } SignalIn;
  __IOM int32_t Value[64];      /*!< (R/W) Value (32-bit) */
} ARM_VIO_Type;

/* Memory mapping of VIO peripheral */
#define ARM_VIO_BASE            (0x4FEF0000UL)                          /*!< VIO Base Address */
#define ARM_VIO                 ((ARM_VIO_Type *)ARM_VIO_BASE)          /*!< VIO struct */

#ifdef __cplusplus
}
#endif

#endif /* __ARM_VIO_H */
