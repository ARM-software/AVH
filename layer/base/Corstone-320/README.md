# Board: Arm SSE-320

## Board Layers for Corstone-320 FVP

These layers work for:

```yml
  board: ARM::SSE-320
  device: ARM::SSE-320-FVP
```

Select one layer matching the application's NPU requirements:

| Layer file           | Use in Application
|:---------------------|:------------------------
| Board.clayer.yml     | Without Ethos-U support
| Board-U85.clayer.yml | With Ethos-U85 support

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
| fvp_config.txt     | Corstone-320 FVP without or with an Ethos-U85-256
