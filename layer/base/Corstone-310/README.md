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

### CMSIS-Driver Virtual I/O mapping

The VIO driver stores and loads signal values in memory.

### FVP Configuration File

| File               | Description
|:-------------------|:-------------
| fvp_config.txt     | Corstone-310 FVP without Ethos-U or with Ethos-U55/U65

