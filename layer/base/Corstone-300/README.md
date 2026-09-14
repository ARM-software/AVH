# Board: Arm V2M-MPS3-SSE-300-FVP

## Board Layer for Corstone-300 FVP

This layer works for:

```yml
  board: ARM::V2M-MPS3-SSE-300-FVP
  device: ARM::SSE-300-MPS3
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
| fvp_config.txt     | Corstone-300 FVP without Ethos-U or with Ethos-U55/U65
