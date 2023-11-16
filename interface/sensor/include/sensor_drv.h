/*
 * Copyright (c) 2022 Arm Limited. All rights reserved.
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

#ifndef SENSOR_DRV_H
#define SENSOR_DRV_H

#ifdef  __cplusplus
extern "C"
{
#endif

#include <stdint.h>

// ==== Sensor Driver Interface ====

/// Identifier
typedef void *sensorId_t;

/// Configuration
typedef const struct {
  char    *name;                            ///< Sensor name
  uint32_t dma_mode;                        ///< DMA mode: 1=DMA, 0=non-DMA (FIFO)
  uint32_t sample_size;                     ///< Sample size in bytes
  union {
    struct {
      uint32_t sample_interval;             ///< Sample interval in microseconds
      uint32_t fifo_size;                   ///< Sample FIFO size in bytes
      uint32_t data_threshold;              ///< Data event threshold in number of samples
    } fifo;                                 ///< Structure with FIFO configuration
    struct {
      uint32_t block_interval;              ///< Block interval in microseconds
      uint32_t block_size;                  ///< Block size in bytes
      uint32_t block_num;                   ///< Number of blocks
    } dma;                                  ///< Structure with DMA configuration
  } u;                                      ///< Union with FIFO and DMA configuration structures
} sensorConfig_t;

/// Status
typedef struct {
  uint32_t active   :  1;                   ///< Active state: 1=enabled(active), 0=disabled(inactive)
  uint32_t overflow :  1;                   ///< Overflow flag (cleared on \ref sensorGetStatus)
  uint32_t reserved : 30;
} sensorStatus_t;

// Function return codes
#define SENSOR_OK               (0)         ///< Operation completed successfully
#define SENSOR_ERROR            (-1)        ///< Operation failed

// Events
#define SENSOR_EVENT_DATA       (1UL << 0)  ///< Data available
#define SENSOR_EVENT_OVERFLOW   (1UL << 1)  ///< Overflow detected

/// \brief       Sensor Events callback function type.
/// \param[in]   id        \ref sensorId_t
/// \param[in]   event     events notification mask
/// \return      none
typedef void (*sensorEvent_t) (sensorId_t id, uint32_t event);

/// \brief       Get sensor identifier.
/// \param[in]   name        sensor name (pointer to NULL terminated string)
/// \return      \ref sensorId_t
sensorId_t sensorGetId (const char *name);

/// \brief       Get sensor configuration.
/// \param[in]   id          \ref sensorId_t
/// \return      pointer to \ref sensorConfig_t
sensorConfig_t *sensorGetConfig (sensorId_t id);

/// \brief       Register sensor events.
/// \param[in]   id          \ref sensorId_t
/// \param[in]   event_cb    pointer to \ref sensorEvent_t
/// \param[in]   event_mask  event mask
/// \return      return code
int32_t sensorRegisterEvents (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask);

/// \brief       Enable sensor.
/// \param[in]   id          \ref sensorId_t
/// \return      return code
int32_t sensorEnable (sensorId_t id);

/// \brief       Disable sensor.
/// \param[in]   id          \ref sensorId_t
/// \return      return code
int32_t sensorDisable (sensorId_t id);

/// \brief       Get sensor status.
/// \param[in]   id          \ref sensorId_t
/// \return      \ref sensorStatus_t
sensorStatus_t sensorGetStatus (sensorId_t id);

/// \brief       Read samples from sensor.
/// \param[in]   id          \ref sensorId_t
/// \param[in]   num_samples maximum number of samples to read
/// \param[out]  buf         pointer to buffer for samples
/// \param[in]   buf_size    buffer size in bytes
/// \return      number of samples read
uint32_t sensorReadSamples (sensorId_t id, uint32_t num_samples, void *buf, uint32_t buf_size);

/// \brief       Get block data.
/// \param[in]   id          \ref sensorId_t
/// \return      pointer to block data
void *sensorGetBlockData (sensorId_t id);

#ifdef  __cplusplus
}
#endif

#endif  /* SENSOR_DRV_H */
