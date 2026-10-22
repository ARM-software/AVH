# Board: Arm V2M-MPS3-SSE-310

## Board Layers for Corstone-310 FVP

These layers work for:

```yml
  board: ARM::V2M-MPS3-SSE-310
  device: ARM::SSE-310-MPS3_FVP
```

Select one layer matching the application's NPU requirements:

| Layer file           | Use in Application
|:---------------------|:------------------------
| Board.clayer.yml     | Without Ethos-U support
| Board-U55.clayer.yml | With Ethos-U55 support
| Board-U65.clayer.yml | With Ethos-U65 support

Use the corresponding FVP configuration file listed below.

### System Configuration

| System Component        | Setting
|:------------------------|:----------------------------------
| Heap                    |  96 kB (configured in regions header)
| Stack (MSP)             |  4 kB (configured in regions header)

### STDIO mapping

**STDIO** is routed to terminal via **UART0** peripheral

### CMSIS-Driver mapping

| CMSIS-Driver           | Peripheral | Connection
|:-----------------------|:-----------|:----------------------
| Driver_USART0          | UART0      | STDIN, STDOUT, STDERR
| CMSIS-Driver VIO       | VIO        | CMSIS_VIO
| Driver_vStreamAudioIn  | VSI0       | CMSIS_VSTREAM_AUDIO_IN
| Driver_vStreamAudioOut | VSI1       | CMSIS_VSTREAM_AUDIO_OUT
| Driver_vStreamVideoIn  | VSI4       | CMSIS_VSTREAM_VIDEO_IN
| Driver_vStreamVideoOut | VSI6       | CMSIS_VSTREAM_VIDEO_OUT

### CMSIS-Driver Virtual I/O mapping

VIO driver interfaces with the `arm_vio.py` Python stub implementation which
stores and loads signal values.

### CMSIS-Driver vStream configuration

| Driver                 | Stream Format Description
|:-----------------------|:----------------------------------------------------
| Driver_vStreamAudioIn  | 16-bit PCM audio,      16000 samples/second
| Driver_vStreamAudioOut | 16-bit PCM audio,      16000 samples/second
| Driver_vStreamVideoIn  | RGB888 video,          resolution 640 x 480 (W x H)
| Driver_vStreamVideoOut | RGB888 video,          resolution 640 x 480 (W x H)

### FVP Configuration File

| File               | Description
|:-------------------|:-------------
| fvp_config.txt     | Corstone-310 FVP without Ethos-U or with Ethos-U55/U65

### Python Requirements

vStream Audio and Video implementations for VSI depend on PyAudio and OpenCV
libraries for Python. Use [requirements.txt](requirements.txt) to install
required Python packages:

- opencv-python
- PyAudio

```bash
pip install -r requirements.txt
```
