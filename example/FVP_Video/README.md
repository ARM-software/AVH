# vStream Video

The **vStream Video** project demonstrates the CMSIS-Driver vStream API for handling
video input and output streams.

It shows how to capture video frames from an input stream and output them through a video output stream.

## Operation

The application initializes both video input and output streams and then continuously
captures video frames from the input stream and copies them directly to the output
stream.

The example uses CMSIS-RTOS2 for thread management and event-driven processing.

### Configuration

Default configuration expects the following input and output stream format:

- 320 x 240 pixels, 3 byte per pixel

To change default configuration use configuration defines:

- `VIDEO_FRAME_WIDTH`  - the video stream frame width in pixels
- `VIDEO_FRAME_HEIGHT` - the video stream frame height in pixels
- `VIDEO_PIXEL_SIZE`   - the video stream bytes per pixel
