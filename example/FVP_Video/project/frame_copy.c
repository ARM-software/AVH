/*
 * Copyright 2025-2026 Arm Limited and/or its affiliates.
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
#include <string.h>

#include "app_main.h"
#include "app_config.h"

/**
  Copy a smaller or equally sized image into a destination buffer at a given offset.

  Assumes that the source image fits completely within the destination at the specified offset.
  It assumes both source and destination use the RGB888 format.

  \param src        Pointer to the source image buffer.
  \param src_width  Width of the source image in pixels.
  \param src_height Height of the source image in pixels.
  \param dst        Pointer to the destination framebuffer buffer.
  \param dst_width  Width of the destination framebuffer in pixels.
  \param dst_height Height of the destination framebuffer in pixels.
  \param x_offset   X offset in the framebuffer where the image should be placed.
  \param y_offset   Y offset in the framebuffer where the image should be placed.
  \param format     Pixel format for both source and destination (must match).
*/
static void copy_RGB888(const uint8_t *src,
                        int src_width,
                        int src_height,
                        uint8_t *dst,
                        int dst_width,
                        int dst_height,
                        int x_offset,
                        int y_offset) {
  int bpp = 3;

  for (int y = 0; y < src_height; ++y) {
    int dst_y = y + y_offset;
    if (dst_y < 0 || dst_y >= dst_height)
      continue;

    for (int x = 0; x < src_width; ++x) {
      int dst_x = x + x_offset;
      if (dst_x < 0 || dst_x >= dst_width)
        continue;

      int src_idx = (y * src_width + x) * bpp;
      int dst_idx = (dst_y * dst_width + dst_x) * bpp;

      for (int i = 0; i < bpp; ++i) {
        dst[dst_idx + i] = src[src_idx + i];
      }
    }
  }
}

/**
  \brief Crop a region from an RGB888 image.
 
  The function copies a cropped rectangle from a source RGB888 image and writes
  it to a destination buffer in RGB888 format.

  \param src           Pointer to the input RGB888 image buffer.
  \param src_width     Width of the source image in pixels.
  \param src_height    Height of the source image in pixels.
  \param dst           Pointer to the output RGB888 buffer.
  \param crop_x        X coordinate of the top-left corner of the crop region.
  \param crop_y        Y coordinate of the top-left corner of the crop region.
  \param crop_width    Width of the crop region in pixels.
  \param crop_height   Height of the crop region in pixels.
*/
static void crop_rgb888(const uint8_t *src,
                        int src_width,
                        int src_height,
                        uint8_t *dst,
                        int crop_x,
                        int crop_y,
                        int crop_width,
                        int crop_height)
{
  const int bpp = 3;

  for (int y = 0; y < crop_height; ++y) {
    int src_y = crop_y + y;
    if (src_y >= src_height) break; // Prevent out-of-bounds

    const uint8_t *src_row = src + (src_y * src_width + crop_x) * bpp;
    uint8_t *dst_row = dst + (y * crop_width) * bpp;

    for (int x = 0; x < crop_width; ++x) {
      int src_x = x;
      if ((crop_x + src_x) >= src_width) break;

      const uint8_t *src_pixel = src_row + src_x * bpp;
      uint8_t *dst_pixel = dst_row + x * bpp;

      dst_pixel[0] = src_pixel[0]; // R
      dst_pixel[1] = src_pixel[1]; // G
      dst_pixel[2] = src_pixel[2]; // B
    }
  }
}

/**
  Copy a video frame from input to output with automatic centering and/or cropping.

  This function adapts and copies input video frame to the output frame. The behavior
  depends on the relative sizes of input and output frames:
  - If dimensions are equal: Direct memory copy
  - If input is smaller (in one or both dimensions): Centers the input within the output
  - If input is larger (in one or both dimensions): Crops the center region of the input

  Centering and cropping are always applied from the center to maintain visual balance.
  The output buffer is filled with zeros (black) for any areas not covered by the input.

  The function assumes that both input and output frames are in RGB888 format.

  \param in_frame  Pointer to the input frame buffer.
  \param out_frame Pointer to the output frame buffer.
  \return int32_t  0 on success, -1 if configuration is unsupported.
*/
int32_t frame_copy(const void *in_frame, void *out_frame) {
#if (VIDEO_IN_FRAME_WIDTH == VIDEO_OUT_FRAME_WIDTH) && (VIDEO_IN_FRAME_HEIGHT == VIDEO_OUT_FRAME_HEIGHT)
  /* Input and output dimensions are the same, perform a direct copy */
  memcpy(out_frame, in_frame, VIDEO_OUT_BUF_BLOCK_SIZE);
  return 0;
#elif ((VIDEO_IN_FRAME_WIDTH < VIDEO_OUT_FRAME_WIDTH) && (VIDEO_IN_FRAME_HEIGHT <= VIDEO_OUT_FRAME_HEIGHT)) || \
      ((VIDEO_IN_FRAME_WIDTH <= VIDEO_OUT_FRAME_WIDTH) && (VIDEO_IN_FRAME_HEIGHT < VIDEO_OUT_FRAME_HEIGHT))
  /* Input frame is smaller than output frame, copy input to the output center */
  copy_RGB888((const uint8_t *)in_frame,
               VIDEO_IN_FRAME_WIDTH,
               VIDEO_IN_FRAME_HEIGHT,
               (uint8_t *)out_frame,
               VIDEO_OUT_FRAME_WIDTH,
               VIDEO_OUT_FRAME_HEIGHT,
               (VIDEO_OUT_FRAME_WIDTH - VIDEO_IN_FRAME_WIDTH) / 2,
               (VIDEO_OUT_FRAME_HEIGHT - VIDEO_IN_FRAME_HEIGHT) / 2);
  return 0;
#elif ((VIDEO_IN_FRAME_WIDTH >  VIDEO_OUT_FRAME_WIDTH) && (VIDEO_IN_FRAME_HEIGHT >= VIDEO_OUT_FRAME_HEIGHT)) || \
      ((VIDEO_IN_FRAME_WIDTH >= VIDEO_OUT_FRAME_WIDTH) && (VIDEO_IN_FRAME_HEIGHT >  VIDEO_OUT_FRAME_HEIGHT))
  /* Input frame is larger than output frame, crop center of input image and copy to output */
  crop_rgb888((const uint8_t *)in_frame,
              VIDEO_IN_FRAME_WIDTH,
              VIDEO_IN_FRAME_HEIGHT,
              (uint8_t *)out_frame,
              (VIDEO_IN_FRAME_WIDTH - VIDEO_OUT_FRAME_WIDTH) / 2,
              (VIDEO_IN_FRAME_HEIGHT - VIDEO_OUT_FRAME_HEIGHT) / 2,
              VIDEO_OUT_FRAME_WIDTH,
              VIDEO_OUT_FRAME_HEIGHT);
  return 0;
#else
  /* Unsupported configuration */
  return -1;
#endif
}
