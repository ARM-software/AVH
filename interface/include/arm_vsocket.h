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
 * Virtual Socket (VSocket) - IoT Socket
 */

#ifndef __ARM_VSOCKET_H
#define __ARM_VSOCKET_H

#ifdef  __cplusplus
extern "C" {
#endif

#include <stdint.h>

/**** VSocket function identifiers ****/
#define VSOCKET_CREATE              1   ///< iotSocketCreate
#define VSOCKET_BIND                2   ///< iotSocketBind
#define VSOCKET_LISTEN              3   ///< iotSocketListen
#define VSOCKET_ACCEPT              4   ///< iotSocketAccept
#define VSOCKET_CONNECT             5   ///< iotSocketConnect
#define VSOCKET_RECV                6   ///< iotSocketRecv
#define VSOCKET_RECV_FROM           7   ///< iotSocketRecvFrom
#define VSOCKET_SEND                8   ///< iotSocketSend
#define VSOCKET_SEND_TO             9   ///< iotSocketSendTo
#define VSOCKET_GET_SOCK_NAME       10  ///< iotSocketGetSockName
#define VSOCKET_GET_PEER_NAME       11  ///< iotSocketGetPeerName
#define VSOCKET_GET_OPT             12  ///< iotSocketGetOpt
#define VSOCKET_SET_OPT             13  ///< iotSocketSetOpt
#define VSOCKET_CLOSE               14  ///< iotSocketClose
#define VSOCKET_GET_HOST_BY_NAME    15  ///< iotSocketGetHostByName

/**
  \brief  I/O structure for iotSocketCreate.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         af;         /*!< address family */
    int32_t         type;       /*!< socket type */
    int32_t         protocol;   /*!< socket protocol */
  } param;                      /*!< parameters */
} vSocketCreateIO_t;

/**
  \brief  I/O structure for iotSocketBind.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    const uint8_t * ip;         /*!< pointer to local IP address */
    uint32_t        ip_len;     /*!< length of 'ip' address in bytes */
    uint16_t        port;       /*!< local port number */
    uint16_t        padding;
  } param;                      /*!< parameters */
} vSocketBindIO_t;

/**
  \brief  I/O structure for iotSocketListen.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    int32_t         backlog;    /*!< number of connection requests that can be queued */
  } param;                      /*!< parameters */
} vSocketListenIO_t;

/**
  \brief  I/O structure for iotSocketAccept.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    uint8_t  *      ip;         /*!< pointer to buffer where address of connecting socket shall be returned (NULL for none) */
    uint32_t *      ip_len;     /*!< pointer to length of 'ip' (or NULL if 'ip' is NULL) */
    uint16_t *      port;       /*!< pointer to buffer where port of connecting socket shall be returned (NULL for none) */
  } param;                      /*!< parameters */
} vSocketAcceptIO_t;

/**
  \brief  I/O structure for iotSocketConnect.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    const uint8_t * ip;         /*!< pointer to remote IP address */
    uint32_t        ip_len;     /*!< length of 'ip' address in bytes */
    uint16_t        port;       /*!< remote port number */
    uint16_t        padding;
  } param;                      /*!< parameters */
} vSocketConnectIO_t;

/**
  \brief  I/O structure for iotSocketRecv.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    void *          buf;        /*!< pointer to buffer where data should be stored */
    uint32_t        len;        /*!< length of buffer (in bytes) */
  } param;                      /*!< parameters */
} vSocketRecvIO_t;

/**
  \brief  I/O structure for iotSocketRecvFrom.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    void *          buf;        /*!< pointer to buffer where data should be stored */
    uint32_t        len;        /*!< length of buffer (in bytes) */
    uint8_t  *      ip;         /*!< pointer to buffer where remote source address shall be returned (NULL for none) */
    uint32_t *      ip_len;     /*!< pointer to length of 'ip' (or NULL if 'ip' is NULL) */
    uint16_t *      port;       /*!< pointer to buffer where remote source port shall be returned (NULL for none) */
  } param;                      /*!< parameters */
} vSocketRecvFromIO_t;

/**
  \brief  I/O structure for iotSocketSend.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    const void *    buf;        /*!< pointer to buffer containing data to send */
    uint32_t        len;        /*!< length of data (in bytes) */
  } param;                      /*!< parameters */
} vSocketSendIO_t;

/**
  \brief  I/O structure for iotSocketSendTo.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    const void *    buf;        /*!< pointer to buffer containing data to send */
    uint32_t        len;        /*!< length of data (in bytes) */
    const uint8_t * ip;         /*!< pointer to remote destination IP address */
    uint32_t        ip_len;     /*!< length of 'ip' address in bytes */
    uint16_t        port;       /*!< remote destination port number */
    uint16_t        padding;
  } param;                      /*!< parameters */
} vSocketSendToIO_t;

/**
  \brief  I/O structure for iotSocketGetSockName.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    uint8_t  *      ip;         /*!< pointer to buffer where local address shall be returned (NULL for none) */
    uint32_t *      ip_len;     /*!< pointer to length of 'ip' (or NULL if 'ip' is NULL) */
    uint16_t *      port;       /*!< pointer to buffer where local port shall be returned (NULL for none) */
  } param;                      /*!< parameters */
} vSocketGetSockNameIO_t;

/**
  \brief  I/O structure for iotSocketGetPeerName.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    uint8_t  *      ip;         /*!< pointer to buffer where remote address shall be returned (NULL for none) */
    uint32_t *      ip_len;     /*!< pointer to length of 'ip' (or NULL if 'ip' is NULL) */
    uint16_t *      port;       /*!< pointer to buffer where remote port shall be returned (NULL for none) */
  } param;                      /*!< parameters */
} vSocketGetPeerNameIO_t;

/**
  \brief  I/O structure for iotSocketGetOpt.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    int32_t         opt_id;     /*!< option identifier */
    void     *      opt_val;    /*!< pointer to the buffer that will receive the option value */
    uint32_t *      opt_len;    /*!< pointer to length of the option value */
  } param;                      /*!< parameters */
} vSocketGetOptIO_t;

/**
  \brief  I/O structure for iotSocketSetOpt.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
    int32_t         opt_id;     /*!< option identifier */
    const void *    opt_val;    /*!< pointer to the option value */
    uint32_t        opt_len;    /*!< length of the option value in bytes */
  } param;                      /*!< parameters */
} vSocketSetOptIO_t;

/**
  \brief  I/O structure for iotSocketClose.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    int32_t         socket;     /*!< socket identification number */
  } param;                      /*!< parameters */
} vSocketCloseIO_t;

/**
  \brief  I/O structure for iotSocketGetHostByName.
 */
typedef struct {
  int32_t           ret_val;    /*!< return value */
  struct {
    const char *    name;       /*!< host name */
    uint32_t        len;        /*!< length of host name */
    int32_t         af;         /*!< address family */
    uint8_t  *      ip;         /*!< pointer to buffer where resolved IP address shall be returned */
    uint32_t *      ip_len;     /*!< pointer to length of 'ip' */
  } param;                      /*!< parameters */
} vSocketGetHostByNameIO_t;

/**
  \brief  Structure type to access the VSocket.
 */
typedef struct
{
  volatile uint32_t                   reserved;
  volatile vSocketCreateIO_t        * vSocketCreateIO;
  volatile vSocketBindIO_t          * vSocketBindIO;
  volatile vSocketListenIO_t        * vSocketListenIO;
  volatile vSocketAcceptIO_t        * vSocketAcceptIO;
  volatile vSocketConnectIO_t       * vSocketConnectIO;
  volatile vSocketRecvIO_t          * vSocketRecvIO;
  volatile vSocketRecvFromIO_t      * vSocketRecvFromIO;
  volatile vSocketSendIO_t          * vSocketSendIO;
  volatile vSocketSendToIO_t        * vSocketSendToIO;
  volatile vSocketGetSockNameIO_t   * vSocketGetSockNameIO;
  volatile vSocketGetPeerNameIO_t   * vSocketGetPeerNameIO;
  volatile vSocketGetOptIO_t        * vSocketGetOptIO;
  volatile vSocketSetOptIO_t        * vSocketSetOptIO;
  volatile vSocketCloseIO_t         * vSocketCloseIO;
  volatile vSocketGetHostByNameIO_t * vSocketGetHostByNameIO;
} ARM_VSocket_Type;

// Memory mapping of VSocket peripheral
#define ARM_VSOCKET_BASE        (0x4FEE0000UL)                          /*!< VSocket Base Address */
#define ARM_VSOCKET             ((ARM_VSocket_Type *)ARM_VSOCKET_BASE)  /*!< VSocket struct */

#ifdef  __cplusplus
}
#endif

#endif /* __ARM_VSOCKET_H */
