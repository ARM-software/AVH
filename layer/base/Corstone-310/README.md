# Board: Arm V2M-MPS3-SSE-310

## Board Layer for Corstone-310 FVP

This layer works for:

```yml
  board: ARM::V2M-MPS3-SSE-310
  device: ARM::SSE-310-MPS3_FVP
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

### CMSIS-Driver Virtual I/O mapping

VIO driver interfaces with the `arm_vio.py` Python stub implementation which
stores and loads signal values.

### FVP Configuration File

| File               | Description
|:-------------------|:-------------
| fvp_config.txt     | Corstone-310 FVP without Ethos-U or with Ethos-U55/U65

