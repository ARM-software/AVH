# Board: Arm SSE-320

## Board Layer for Corstone-320 FVP

This layer works for:

```yml
  board: ARM::SSE-320
  device: ARM::SSE-320-FVP
```

### System Configuration

| System Component        | Setting
|:------------------------|:----------------------------------
| Heap                    | 768 kB (configured in linker file)
| Stack (MSP)             |  32 kB (configured in linker file)

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
| Driver_vStreamVideoIn  | RGB888 video,          resolution 1280 x 720 (W x H)
| Driver_vStreamVideoOut | RGB888 video,          resolution  480 x 800 (W x H)

### FVP Configuration File

| File               | Description
|:-------------------|:-------------
| fvp_config.txt     | Corstone-320 FVP without Ethos-U or with Ethos-U85

### Python Requirements

vStream Audio and Video implementations for VSI depend on PyAudio and OpenCV
libraries for Python. Use [requirements.txt](requirements.txt) to install
required Python packages:

- opencv-python
- PyAudio

```bash
pip install -r requirements.txt
```
