# FVP Video

The **FVP Video** project demonstrates the CMSIS-Driver vStream API for handling
video input and output streams.

It shows how to capture video frames from an input stream and output them through a video output stream.

## Operation

The application initializes both video input and output streams and then continuously
captures video frames from the input stream and copies them to the output stream.
Application assumes that the video frame pixel format is RGB888.

If input and output stream resolutions differ the input frame is centered within the
output frame and/or cropped when required.

Streaming stops after receiving the `END_OF_STREAM` event or can be configured to
stop after `AUDIO_STREAM_DURATION` seconds.

The example uses CMSIS-RTOS2 for thread management and event-driven processing.

### Configuration

Default configuration ([app_config.h](project/app_config.h)) expects the following input
and output stream format:

- 640 x 480 pixels, 30FPS

To change the default configuration use the following defines:

- `VIDEO_IN_FRAME_WIDTH`   - the input video stream frame width in pixels
- `VIDEO_IN_FRAME_HEIGHT`  - the input video stream frame height in pixels
- `VIDEO_OUT_FRAME_WIDTH`  - the output video stream frame width in pixels
- `VIDEO_OUT_FRAME_HEIGHT` - the output video stream frame height in pixels
- `VIDEO_FRAME_RATE`       - the video frame rate in frames per second

The default streaming duration is indefinite. To change this, use:

- `VIDEO_STREAM_DURATION` - sets the streaming duration in seconds (0: stream indefinitely)
