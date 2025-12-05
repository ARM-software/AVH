# vStream via VSI

This directory contains the implementation of vStream interface for audio and video streaming
using Virtual Streaming Interface (VSI). The vStream interface is defined by CMSIS-Driver and
offers standardized interface to interact with various streaming devices to allow seamless
development on one platform and deployment on another.

Implementation consists of two components

- vStream driver implementation in C (targeting embedded application)
- implementation of VSI Python interface in Python (targeting host PC)

## vStream Drivers

Directory `source` contains CMSIS-Driver vStream implementations for audio input/output
and video input/output streaming.

**Audio Drivers**:

- `vstream_audio_in.c/h`  - vStream_AudioIn implementation
- `vstream_audio_out.c/h` - vStream_AudioOut implementation

**Video Drivers**:

- `vstream_video_in.c/h`  - vStream_VideoIn implementation
- `vstream_video_out.c/h` - vStream_VideoOut implementation

### Configuration for vStream Drivers

Directory `config` contains configuration headers for vStream drivers.

Configuration enables user to configure basic audio and video stream parameters
to adapt vStream driver to embedded application expectation.

**Configuration Files**:

- `vstream_audio_in_config.h`  - configures vStream_AudioIn
- `vstream_audio_out_config.h` - configures vStream_AudioOut
- `vstream_video_in_config.h`  - configures vStream_VideoIn
- `vstream_video_out_config.h` - configures vStream_VideoOut

**Audio Stream Configuration**:

Configuration options for configuring vStream audio drivers are:

| Parameter                 | Description                                          | Available Options               | Configuration Macro          |
|---------------------------|------------------------------------------------------|---------------------------------|------------------------------|
| Number of channels        | Defines the number of audio channels in stream       | Mono (1), Stereo (2)            | `AUDIO_[IN/OUT]_CHANNELS`    |
| Number of bits per sample | Defines number of bits of information in each sample | 8-bit, 16-bit, 24-bit, 32-bit   | `AUDIO_[IN/OUT]_SAMPLE_BITS` |
| Sample rate               | Defines the number of samples per second             | 8 kHz, 16 kHz, 44.1 kHz, 48 kHz | `AUDIO_[IN/OUT]_SAMPLE_RATE` |

**Video Stream Configuration**:

Configuration options for configuring vStream Video drivers are:

| Parameter    | Description                                              | Available Options               | Configuration Macro           |
|--------------|----------------------------------------------------------|---------------------------------|-------------------------------|
| Frame width  | Defines the video stream frame width in pixels           | User-defined (e.g., 320, 640)   | `VIDEO_[IN/OUT]_FRAME_WIDTH`  |
| Frame height | Defines the video stream frame height in pixels          | User-defined (e.g., 240, 480)   | `VIDEO_[IN/OUT]_FRAME_HEIGHT` |
| Frame rate   | Defines the video stream frame rate in frames per second | User-defined (e.g., 15, 30, 60) | `VIDEO_[IN/OUT]_FRAME_RATE`   |
| Color format | Defines the video frame color space                      | Grayscale, RGB888, BGR565       | `VIDEO_[IN/OUT]_FRAME_COLOR`  |

**Common Configuration**:

Besides stream configuration there are configuration options related to stream source selection. The below table shows possible stream sources:

| Stream Type   | Stream Source         | Description                                   | Configuration                            |
|---------------|-----------------------|-----------------------------------------------|------------------------------------------|
| **Audio In**  | System Default Input  | Uses the system's default audio input device  | `AUDIO_IN_DEVICE = -1`                   |
|               | Specific Audio Device | Uses a specific audio input device by index   | `AUDIO_IN_DEVICE = <device_index>`       |
|               | Audio File            | Reads audio data from a file                  | `AUDIO_IN_FILENAME = "path/to/file.wav"` |
| **Audio Out** | System Default Output | Uses the system's default audio output device | `AUDIO_OUT_DEVICE = -1`                  |
|               | Specific Audio Device | Uses a specific audio output device by index  | `AUDIO_OUT_DEVICE = <device_index>`      |
|               | Audio File            | Writes audio data to a file                   | `AUDIO_OUT_FILENAME = "path/to/file.wav"`|
| **Video In**  | System Default Input  | Uses the system's default video input device  | `VIDEO_IN_DEVICE = -1`                   |
|               | Specific Input Device | Uses a specific camera device by index        | `VIDEO_IN_DEVICE = <device_index>`       |
|               | Video File            | Reads video frames from a file                | `VIDEO_IN_FILENAME = "path/to/file.mp4"` |
| **Video Out** | Display Window        | Displays video frames in a window             | No device configuration needed           |
|               | Video File            | Writes video frames to a file                 | `VIDEO_OUT_FILENAME = "path/to/file.mp4"`|

> [!NOTE]
>
> OpenCV is not able to automatically detect system default device. Instead it enumerates devices, for example:
>
> - 0 being the internal camera
> - 1 is the first external camera

## Virtual Streaming Interface for Python

Directory `python` contains Python scripts that implement [VSI for Python](https://arm-software.github.io/AVH/main/simulation/html/group__arm__vsi__py.html)
and execute on host PC. Audio and video servers are implemented independently to support access to audio and video streams.

**VSI scripts for Python**:

The `arm_vsi*.py` files provide VSI implementations for different channels.

- `arm_vsi0.py` and `arm_vsi1.py` implement Audio streaming channels
- `arm_vsi4/vsi5/vsi6/vsi7.py` - implement Video streaming channels

**Audio Server**:

- `vsi_audio_server.py` and
- `vsi_audio.py`

  implement Python server and client for audio streaming using PyAudio.

**Video Server**:

- `vsi_video_server.py` and
- `vsi_video.py`

  implement Python server and client for video streaming using OpenCV.

### Audio Server

The Audio Server implements a TCP-based server for audio streaming operations using PyAudio. It provides comprehensive audio I/O capabilities for both real-time audio devices and file-based streaming.

**Key Features**:

- Supports both audio input (microphone/file recording) and audio output (speaker/file playback)
- Supports automatic detection and configuration of system audio devices
- Supports WAV file reading and writing
- Allows multiple client connections

### Video Server

The Video Server implements a TCP-based server for video streaming operations using OpenCV. It provides video I/O capabilities for accessing cameras and video files.

**Key Features**:

- Supports both video input (camera/file capture) and video output (display/file recording)
- Supports access to system cameras and USB video devices
- Supports multiple video formats (AVI, MP4, WMV) and image formats (BMP, PNG, JPG)
- Supports frame-by-frame processing with automatic format conversion
- Allows multiple client connections
