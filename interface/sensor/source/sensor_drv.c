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

// Sensor Driver

#include <string.h>

#include "sensor_config.h"
#include "sensor_drv.h"
#include "sensor_drv_hw.h"


#ifdef SENSOR0_NAME
static sensorConfig_t sensorConfig0 = {
  SENSOR0_NAME,
  SENSOR0_DMA_MODE,
  SENSOR0_SAMPLE_SIZE,
  #if SENSOR0_DMA_MODE == 0U
  { {
    SENSOR0_SAMPLE_INTERVAL,
    SENSOR0_FIFO_SIZE,
    SENSOR0_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR0_BLOCK_INTERVAL,
    SENSOR0_BLOCK_SIZE,
    SENSOR0_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR1_NAME
static sensorConfig_t sensorConfig1 = {
  SENSOR1_NAME,
  SENSOR1_DMA_MODE,
  SENSOR1_SAMPLE_SIZE,
  #if SENSOR1_DMA_MODE == 0U
  { {
    SENSOR1_SAMPLE_INTERVAL,
    SENSOR1_FIFO_SIZE,
    SENSOR1_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR1_BLOCK_INTERVAL,
    SENSOR1_BLOCK_SIZE,
    SENSOR1_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR2_NAME
static sensorConfig_t sensorConfig2 = {
  SENSOR2_NAME,
  SENSOR2_DMA_MODE,
  SENSOR2_SAMPLE_SIZE,
  #if SENSOR2_DMA_MODE == 0U
  { {
    SENSOR2_SAMPLE_INTERVAL,
    SENSOR2_FIFO_SIZE,
    SENSOR2_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR2_BLOCK_INTERVAL,
    SENSOR2_BLOCK_SIZE,
    SENSOR2_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR3_NAME
static sensorConfig_t sensorConfig3 = {
  SENSOR3_NAME,
  SENSOR3_DMA_MODE,
  SENSOR3_SAMPLE_SIZE,
  #if SENSOR3_DMA_MODE == 0U
  { {
    SENSOR3_SAMPLE_INTERVAL,
    SENSOR3_FIFO_SIZE,
    SENSOR3_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR3_BLOCK_INTERVAL,
    SENSOR3_BLOCK_SIZE,
    SENSOR3_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR4_NAME
static sensorConfig_t sensorConfig4 = {
  SENSOR4_NAME,
  SENSOR4_DMA_MODE,
  SENSOR4_SAMPLE_SIZE,
  #if SENSOR4_DMA_MODE == 0U
  { {
    SENSOR4_SAMPLE_INTERVAL,
    SENSOR4_FIFO_SIZE,
    SENSOR4_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR4_BLOCK_INTERVAL,
    SENSOR4_BLOCK_SIZE,
    SENSOR4_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR5_NAME
static sensorConfig_t sensorConfig5 = {
  SENSOR5_NAME,
  SENSOR5_DMA_MODE,
  SENSOR5_SAMPLE_SIZE,
  #if SENSOR5_DMA_MODE == 0U
  { {
    SENSOR5_SAMPLE_INTERVAL,
    SENSOR5_FIFO_SIZE,
    SENSOR5_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR5_BLOCK_INTERVAL,
    SENSOR5_BLOCK_SIZE,
    SENSOR5_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR6_NAME
static sensorConfig_t sensorConfig6 = {
  SENSOR6_NAME,
  SENSOR6_DMA_MODE,
  SENSOR6_SAMPLE_SIZE,
  #if SENSOR6_DMA_MODE == 0U
  { {
    SENSOR6_SAMPLE_INTERVAL,
    SENSOR6_FIFO_SIZE,
    SENSOR6_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR6_BLOCK_INTERVAL,
    SENSOR6_BLOCK_SIZE,
    SENSOR6_BLOCK_NUM
  } }
  #endif
};
#endif

#ifdef SENSOR7_NAME
static sensorConfig_t sensorConfig7 = {
  SENSOR7_NAME,
  SENSOR7_DMA_MODE,
  SENSOR7_SAMPLE_SIZE,
  #if SENSOR7_DMA_MODE == 0U
  { {
    SENSOR7_SAMPLE_INTERVAL,
    SENSOR7_FIFO_SIZE,
    SENSOR7_DATA_THRESHOLD
  } }
  #else
  { {
    SENSOR7_BLOCK_INTERVAL,
    SENSOR7_BLOCK_SIZE,
    SENSOR7_BLOCK_NUM
  } }
  #endif
};
#endif


// Control block
typedef struct {
  sensorConfig_t *config;
  sensorDrvHW_t  *drw_hw;
  sensorStatus_t  status;
} sensor_t;

static sensor_t Sensors[8] = {
#ifdef SENSOR0_NAME
  { &sensorConfig0, &sensorDrvHW_0, {0U, 0U, 0U} },
#endif
#ifdef SENSOR1_NAME
  { &sensorConfig1, &sensorDrvHW_1, {0U, 0U, 0U} },
#endif
#ifdef SENSOR2_NAME
  { &sensorConfig2, &sensorDrvHW_2, {0U, 0U, 0U} },
#endif
#ifdef SENSOR3_NAME
  { &sensorConfig3, &sensorDrvHW_3, {0U, 0U, 0U} },
#endif
#ifdef SENSOR4_NAME
  { &sensorConfig4, &sensorDrvHW_4, {0U, 0U, 0U} },
#endif
#ifdef SENSOR5_NAME
  { &sensorConfig5, &sensorDrvHW_5, {0U, 0U, 0U} },
#endif
#ifdef SENSOR6_NAME
  { &sensorConfig6, &sensorDrvHW_6, {0U, 0U, 0U} },
#endif
#ifdef SENSOR7_NAME
  { &sensorConfig7, &sensorDrvHW_7, {0U, 0U, 0U} },
#endif
};


// Get sensor identifier
sensorId_t sensorGetId (const char *name) {
  sensor_t *sensor = NULL;
  uint32_t n;

  if (name != NULL) {
    for (n = 0U; n < (sizeof(Sensors) / sizeof(sensor_t)); n++) {
      if (strcmp(name, Sensors[n].config->name) == 0) {
        sensor = &Sensors[n];
        break;
      }
    }
  }
  return sensor;
}

// Get sensor configuration
sensorConfig_t *sensorGetConfig (sensorId_t id) {
  sensor_t *sensor = id;
  sensorConfig_t *cfg = NULL;

  if (sensor != NULL) {
    cfg = sensor->config;
  }
  return cfg;
}

// Register sensor events
int32_t sensorRegisterEvents (sensorId_t id, sensorEvent_t event_cb, uint32_t event_mask) {
  sensor_t *sensor = id;
  int32_t ret = SENSOR_ERROR;

  if ((sensor != NULL) && (event_cb != NULL) && (event_mask != 0U)) {
    if (sensor->drw_hw->RegisterEvents != NULL) {
      ret = sensor->drw_hw->RegisterEvents(id, event_cb, event_mask);
    }
  }

  return ret;
}

// Enable sensor
int32_t sensorEnable (sensorId_t id) {
  sensor_t *sensor = id;
  int32_t ret = SENSOR_ERROR;

  if (sensor != NULL) {
    if (sensor->status.active == 0U) {
      if (sensor->drw_hw->Enable() == SENSOR_OK) {
        sensor->status.active = 1U;
        ret = SENSOR_OK;
      }
    }
  }
  return ret;
}

// Disable sensor
int32_t sensorDisable (sensorId_t id) {
  sensor_t *sensor = id;
  int32_t ret = SENSOR_ERROR;

  if (sensor != NULL) {
    if (sensor->status.active == 1U) {
      if (sensor->drw_hw->Disable() == SENSOR_OK) {
        sensor->status.active = 0U;
        ret = SENSOR_OK;
      }
    }
  }
  return ret;
}

// Get sensor status
sensorStatus_t sensorGetStatus (sensorId_t id) {
  sensor_t *sensor = id;
  sensorStatus_t stat = {0U, 0U, 0U};

  if (sensor != NULL) {
    stat.active   = sensor->status.active;
    stat.overflow = sensor->drw_hw->GetOverflow();
  }
  return stat;
}

// Read samples from sensor
uint32_t sensorReadSamples (sensorId_t id, uint32_t num_samples, void *buf, uint32_t buf_size) {
  sensor_t *sensor = id;
  uint32_t num = 0U;

  if ((sensor != NULL) && (num_samples != 0U) && (buf != NULL) &&
      (buf_size >= (num_samples * sensor->config->sample_size))) {
    if (sensor->drw_hw->ReadSamples != NULL) {
      num = sensor->drw_hw->ReadSamples(num_samples, buf);
    }
  }
  return num;
}

// Get block data
void *sensorGetBlockData (sensorId_t id) {
  sensor_t *sensor = id;
  void *block_data = NULL;

  if ((sensor != NULL) && (sensor->drw_hw->GetBlockData != NULL)) {
    block_data = sensor->drw_hw->GetBlockData();
  }

  return block_data;
}
