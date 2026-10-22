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

#include "ethosu_driver.h"
#include "cmsis_os2.h"

/* Maximum number of Ethos-U instances.                        */
/* Used as maximum semaphore count in ethosu_semaphore_create. */
#ifndef ETHOSU_MAX_INSTANCES
#define ETHOSU_MAX_INSTANCES 2
#endif

/**
  \brief Create a mutex object.
  \return Pointer to a mutex object.
*/
void *ethosu_mutex_create(void) {
  osMutexId_t mutex_id = osMutexNew(NULL);
  return (void *) mutex_id;
}

/**
  \brief Destroy a mutex object.
  \param[in]  mutex  mutex object.
*/
void ethosu_mutex_destroy(void *mutex) {
  osMutexId_t mutex_id = (osMutexId_t) mutex;
  osMutexDelete(mutex_id);
}

/**
  \brief Lock a mutex.
  \param[in] mutex  mutex object.
  \return 0 on success, else negative error codes
*/
int ethosu_mutex_lock(void *mutex) {
  osMutexId_t mutex_id = (osMutexId_t) mutex;
  osStatus_t  status;
  int         rval;

  status = osMutexAcquire(mutex_id, osWaitForever);
  if (status == osOK) {
    rval = 0;
  } else {
    rval = -1;
  }
  return rval;
}

/**
  \brief Unlock a mutex.
  \param[in] mutex  mutex object.
  \return 0 on success, else negative error codes
*/
int ethosu_mutex_unlock(void *mutex) {
  osMutexId_t mutex_id = (osMutexId_t) mutex;
  osStatus_t  status;
  int         rval;

  status = osMutexRelease(mutex_id);
  if (status == osOK) {
    rval = 0;
  } else {
    rval = -1;
  }
  return rval;
}

/**
  \brief Create a semaphore object.
  \return Pointer to a semaphore object.
*/
void *ethosu_semaphore_create(void) {
  osSemaphoreId_t sem_id;

  sem_id = osSemaphoreNew(ETHOSU_MAX_INSTANCES, 0U, NULL);
  return (void *) sem_id;
}

/**
  \brief Destroy a semaphore object.
  \param[in]  sem  semaphore object.
*/
void ethosu_semaphore_destroy(void *sem) {
  osSemaphoreId_t sem_id = (osSemaphoreId_t) sem;
  osSemaphoreDelete(sem_id);
}

/**
  \brief Take a semaphore object with timeout.
  \param[in]  sem      semaphore object.
  \param[in]  timeout  timeout value in ticks.
  \return 0 on success, else negative error codes
*/
int ethosu_semaphore_take(void *sem, uint64_t timeout) {
  osSemaphoreId_t sem_id = (osSemaphoreId_t) sem;
  osStatus_t      status;
  int             rval;

  status = osSemaphoreAcquire(sem_id, timeout);
  if (status == osOK) {
    rval = 0;
  } else {
    rval = -1;
  }
  return rval;
}

/**
  \brief Give a semaphore object.
  \param[in]  sem  semaphore object.
  \return 0 on success, else negative error codes
*/
int ethosu_semaphore_give(void *sem) {
  osSemaphoreId_t sem_id = (osSemaphoreId_t) sem;
  osStatus_t      status;
  int             rval;

  status = osSemaphoreRelease(sem_id);
  if (status == osOK) {
    rval = 0;
  } else {
    rval = -1;
  }
  return rval;
}
