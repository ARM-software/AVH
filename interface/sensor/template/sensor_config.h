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

#ifndef SENSOR_CONFIG_H
#define SENSOR_CONFIG_H

// Sensor Configuration

// Sensor 0 (non-DMA)
#define SENSOR0_NAME            "Sensor 0"
#define SENSOR0_DMA_MODE        0U
#define SENSOR0_SAMPLE_SIZE     1U
#define SENSOR0_SAMPLE_INTERVAL 1000U
#define SENSOR0_FIFO_SIZE       1U
#define SENSOR0_DATA_THRESHOLD  0U

// Sensor 1 (non-DMA)
#define SENSOR1_NAME            "Sensor 1"
#define SENSOR1_DMA_MODE        0U
#define SENSOR1_SAMPLE_SIZE     2U
#define SENSOR1_SAMPLE_INTERVAL 100000U
#define SENSOR1_FIFO_SIZE       2U
#define SENSOR1_DATA_THRESHOLD  0U

// Sensor 2 (non-DMA)
#define SENSOR2_NAME            "Sensor 2"
#define SENSOR2_DMA_MODE        0U
#define SENSOR2_SAMPLE_SIZE     4U
#define SENSOR2_SAMPLE_INTERVAL 1000000U
#define SENSOR2_FIFO_SIZE       4U
#define SENSOR2_DATA_THRESHOLD  0U

// Sensor 3 (non-DMA)
#define SENSOR3_NAME            "Sensor 3"
#define SENSOR3_DMA_MODE        0U
#define SENSOR3_SAMPLE_SIZE     1U
#define SENSOR3_SAMPLE_INTERVAL 1000U
#define SENSOR3_FIFO_SIZE       8U
#define SENSOR3_DATA_THRESHOLD  0U

// Sensor 4 (non-DMA)
#define SENSOR4_NAME            "Sensor 4"
#define SENSOR4_DMA_MODE        0U
#define SENSOR4_SAMPLE_SIZE     2U
#define SENSOR4_SAMPLE_INTERVAL 100000U
#define SENSOR4_FIFO_SIZE       16U
#define SENSOR4_DATA_THRESHOLD  0U

// Sensor 5 (non-DMA)
#define SENSOR5_NAME            "Sensor 5"
#define SENSOR5_DMA_MODE        0U
#define SENSOR5_SAMPLE_SIZE     4U
#define SENSOR5_SAMPLE_INTERVAL 1000000U
#define SENSOR5_FIFO_SIZE       32U
#define SENSOR5_DATA_THRESHOLD  0U

// Sensor 6 (DMA)
#define SENSOR6_NAME            "Sensor 6"
#define SENSOR6_DMA_MODE        1U
#define SENSOR6_SAMPLE_SIZE     4U
#define SENSOR6_BLOCK_INTERVAL  10000U
#define SENSOR6_BLOCK_SIZE      1000U
#define SENSOR6_BLOCK_NUM       8U

// Sensor 7 (DMA)
#define SENSOR7_NAME            "Sensor 7"
#define SENSOR7_DMA_MODE        1U
#define SENSOR7_SAMPLE_SIZE     4U
#define SENSOR7_BLOCK_INTERVAL  10000U
#define SENSOR7_BLOCK_SIZE      1000U
#define SENSOR7_BLOCK_NUM       8U

#endif /* SENSOR_CONFIG_H */
