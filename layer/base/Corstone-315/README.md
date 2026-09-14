# Board: Arm SSE-315

## Board Layer for Corstone-315 FVP

This layer works for:

```yml
  board: ARM::SSE-315
  device: ARM::SSE-315-FVP
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
| fvp_config.txt     | Corstone-315 FVP without Ethos-U or with Ethos-U65

