# Virtual Interfaces

**Virtual Interfaces** enable the firmware application that runs on the FVP simulation model to interact with external resources on the host computer.

The FVP simulation models support the following Virtual Interface types:

- **VIO** interface controls simple binary state I/O, such as LEDs and switches (maps to [CMSIS-Driver VIO](https://arm-software.github.io/CMSIS_6/latest/Driver/group__vio__interface__gr.html)).
- **VSocket** interface for IP socket connectivity (maps to [IOT-Socket](https://www.keil.arm.com/packs/iot_socket-mdk-packs)).
- **VSI** interface for 8 independent data streaming channels (maps to [CMSIS-Driver vStream](https://arm-software.github.io/CMSIS_6/latest/Driver/group__vstream__interface__gr.html)).

The folder `interface` contains:

```txt
interface/
├── include/          # C header files for firmware (arm_vio.h, arm_vsi.h, arm_vsocket.h)
├── python/           # VSI Python template scripts to implement host-side peripheral behavior for VSI
├── audio/            # VSI Audio interface implementation (legacy, use vstream_audio instead)
├── video/            # VSI Video interface implementation (legacy, use vstream_video instead)
├── sensor/           # VSI Sensor interface templates and examples
├── vio/              # VIO implementation for FVPs
├── vsocket/          # VSocket implementation
└── vstream/          # VSI VStream interface for data streaming
```

## VSI Channel Mapping

The VSI channels (VSI0 .. VSI7) for data streaming use Python scripts to interact with external resources.

The folder `python` contains vanilla VSI Python template scripts that provide the basic framework for implementing peripheral behavior.
These templates serve as starting points for creating custom VSI peripheral implementations.

- `arm_vsi0.py` - `arm_vsi7.py`: Template implementations for all 8 VSI channels
- `arm_vio.py`: Template for Virtual I/O interface

The following table shows how VSI channels are assigned in the provided implementations:

| VSI | Folder    | Purpose                | Description                                          | Port |
|:---:|-----------|------------------------|------------------------------------------------------|------|
|  0  | `vstream` | Audio Input            | vStream Audio In - streams audio data into FVP       | 6000 |
|  1  | `vstream` | Audio Output           | vStream Audio Out - streams audio data from FVP      | 6001 |
|  2  | `sensor`  | Sensor Interface       | Generic sensor data streaming (accelerometer, etc.)  | -    |
|  3  | -         | Available              | Used in SDS Framework for data streaming             | -    |
|  4  | `vstream` | Video Input            | vStream Video In - streams video frames into FVP     | 6004 |
|  5  | `vstream` | Video Output           | vStream Video Out - streams video frames from FVP    | 6005 |
|  6  | `vstream` | Video (Additional)     | Additional video channel for multi-stream scenarios  | 6006 |
|  7  | `vstream` | Video (Additional)     | Additional video channel for multi-stream scenarios  | 6007 |

### Implementation Details

**vStream Implementations** (`vstream/` folder):
- **Audio Channels (VSI 0-1)**: Implement CMSIS-Driver vStream_AudioIn and vStream_AudioOut interfaces
  - Support various audio formats (8/16/24/32-bit samples, mono/stereo, multiple sample rates)
  - Connect to system audio devices or audio files (WAV format)
  - Use audio servers for inter-process communication with the FVP
  
- **Video Channels (VSI 4-7)**: Implement CMSIS-Driver vStream_VideoIn and vStream_VideoOut interfaces
  - Support multiple color formats (Grayscale, RGB888, BGR565)
  - Configurable frame dimensions and frame rates
  - Connect to system cameras, video files, or display windows
  - Use video servers for efficient frame data transfer

**Sensor Implementation** (`sensor/` folder):
- **VSI 2**: Generic sensor interface with templates for various sensor types
  - Supports accelerometer, gyroscope, temperature, and other sensor data
  - Flexible data injection from files or algorithmic generation
  - Configurable sampling rates and data formats

**Legacy Implementations**:
- `audio/` folder contains legacy audio implementations (replaced by vstream)
- `video/` folder contains legacy video implementations (replaced by vstream)

### Usage Guidelines

When developing applications using VSI channels:

1. **Choose the appropriate channel** based on your peripheral type
2. **Start from templates** in the `python/` folder for new custom peripherals
3. **Multiple instances**: Applications can use multiple VSI channels simultaneously for complex system simulations

### Custom Implementations

For custom peripherals, you can reassign VSI channels as needed:

- Copy and modify template scripts from `python/` folder.
- Configure the firmware to use the corresponding VSI base address.
- Implement custom peripheral behavior in the Python script.

This flexibility allows you to simulate virtually any memory-mapped peripheral with streaming data requirements.



