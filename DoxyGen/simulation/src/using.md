# Using AVH FVPs {#Using}

[comment]:[TOC]
This section gives an overview on how to use the **Arm Fixed Virtual Platforms (FVPs)** in AVH context.

The FVP simulation models in AVH correspond to a subset of [Arm Fast Models Fixed Virtual Platforms](https://developer.arm.com/tools-and-software/simulation-models/fixed-virtual-platforms) with extensions for \ref arm_cmvp.

They can be accessed in cloud-native and desktop environments as explained in [Infrastructure chapter](../../infrastructure/html/index.html). The table below lists the available models:

<table>
<tr>
<th style="width:30%">FVP Simulation Model Name   </th><th style="width:16%">Processor Cores   </th><th>Overview Description    </th></tr>
<tr>
<td>FVP_MPS2_Cortex-M0        </td><td>Cortex-M0   </td><td><a href="https://developer.arm.com/documentation/dai0382">ARM Cortex-M0 SMM on V2M-MPS2 (AppNote AN382)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M0plus   </td><td>Cortex-M0+   </td><td><a href="https://developer.arm.com/documentation/dai0383">ARM Cortex-M0+ SMM on V2M-MPS2 (AppNote AN383)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M3       </td><td>Cortex-M3   </td><td><a href="https://developer.arm.com/documentation/dai0385">ARM Cortex-M3 SMM on V2M-MPS2 (AppNote AN385)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M4       </td><td>Cortex-M4   </td><td><a href="https://developer.arm.com/documentation/dai0386">ARM Cortex-M4 SMM on V2M-MPS2 (AppNote AN386)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M7       </td><td>Cortex-M7   </td><td><a href="https://developer.arm.com/documentation/dai0386">ARM Cortex-M7 SMM on V2M-MPS2 (AppNote AN399)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M23      </td><td>Cortex-M23 (2x)   </td><td><a href="https://developer.arm.com/documentation/dai0519">ARM Cortex-M23 IoT Subsystem for V2M-MPS2+ (AppNote AN519)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M33      </td><td>Cortex-M33 (2x)   </td><td><a href="https://developer.arm.com/documentation/dai0505">ARM Cortex-M33 IoT Subsystem for V2M-MPS2+ (AppNote AN505)</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M35P     </td><td>Cortex-M35P (2x)   </td><td><a href="https://developer.arm.com/documentation/100966/latest/MPS2-Platform-FVPs/FVP-MPS2-Cortex-M35P">FVP_MPS2_Cortex-M35P in FVP Reference Guide</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M52      </td><td>Cortex-M52 (2x)   </td><td><a href="https://developer.arm.com/documentation/100966/latest/MPS2-Platform-FVPs/FVP-MPS2-Cortex-M52">FVP_MPS2_Cortex-M52 in FVP Reference Guide</a>    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M55      </td><td>Cortex-M55 (2x)  </td><td><a href="https://developer.arm.com/documentation/100966/latest/MPS2-Platform-FVPs/FVP-MPS2-Cortex-M55">FVP_MPS2_Cortex-M55 in FVP Reference Guide</a>.<br  />
It is recommended to use Corstone-300 FVP models for Cortex-M55.    </td></tr>
<tr>
<td>FVP_MPS2_Cortex-M85   </td><td>Cortex-M85 (2x)  </td><td><a href="https://developer.arm.com/documentation/100966/latest/MPS2-Platform-FVPs/FVP-MPS2-Cortex-M55">FVP_MPS2_Cortex-M85 in FVP Reference Guide</a>.<br  />
It is recommended to use Corstone-310/315 FVP models for Cortex-M85.    </td></tr>
<tr>
<td>FVP_MPS3_Corstone_SSE-300   </td><td>Cortex-M55   </td><td><a href="https://developer.arm.com/documentation/100966/latest/Arm--Corstone-SSE-300-FVP">Arm Corstone SSE-300 FVP</a>    </td></tr>
<tr>
<td>FVP_Corstone_SSE-300_Ethos-U55   </td><td>Cortex-M55,<br/>Ethos-U55   </td><td><a href="https://developer.arm.com/documentation/100966/latest/Arm--Corstone-SSE-300-FVP">Arm Corstone SSE-300 FVP</a>    </td></tr>
<tr>
<td>FVP_Corstone_SSE-300_Ethos-U65   </td><td>Cortex-M55,<br/>Ethos-U65   </td><td><a href="https://developer.arm.com/documentation/100966/latest/Arm--Corstone-SSE-300-FVP">Arm Corstone SSE-300 FVP</a>    </td></tr>
<tr>
<td>FVP_Corstone_SSE-310   </td><td>Cortex-M85<br/>Ethos-U55   </td><td><a href="https://developer.arm.com/documentation/100966/latest/Arm--Corstone-SSE-310-FVP">Arm Corstone SSE-310 FVP</a>    </td></tr>
<tr>
<td>FVP_Corstone_SSE-310_Ethos-U65   </td><td>Cortex-M85,<br/>Ethos-U65   </td><td><a href="https://developer.arm.com/documentation/100966/latest/Arm--Corstone-SSE-310-FVP">Arm Corstone SSE-310 FVP</a>    </td></tr>
<tr>
<td>FVP_Corstone_SSE-315   </td><td>Cortex-M85,<br/>Ethos-U65,<br/>Mali-C55   </td><td>Public documentation pending   </td></tr>
</table>


## Running User Applications {#Execution}

The FVP models can be executed from command prompt by using the model name followed by the model options. Development tools may abstract the execution with GUI, but the underlying approach stays the same.

Below is an example of the command for running a program on the FVP model for Corstone-300 with Ethos-U55 in Linux environment:

```bash
FVP_Corstone_SSE-300_Ethos-U55 -a Objects\microspeech.axf -C mps3_board.v_path= ../VSI/audio/python/ -f fvp_config.txt  --stat --simlimit 24
```

Where:
  - `FVP_Corstone_SSE-300_Ethos-U55` is the simulation model name. Note that on Windows the executable files shall be used, for example `FVP_Corestone_SSE-300_Ethos-U55.exe`. 
  - `-a` (or `--application`) option specifies the application binary file to run on the model (`Objects\microspeech.axf` in this example).
  - `-f` (or `--config-file`) specifies the configuration file for the simulation model (`fvp_config.txt` in this case). See \ref Config.
  - `-C mp3_board.v_path` specifies model configuration parameter for VSI python scripts for \ref arm_cmvp (`"../VSI/audio/python"` here). Use `mp2_board.v_path`, `mps3_board.v_path` or `mps4_board.v_path`, depending on the underlying board.
  - `--stat` instructs to print run statistics on simulation exit.
  - `--simlimit` specifies the maximum number of seconds to simulate.

The available command options can be listed using the `--help` option. See chapter [FVP-command-line-options](https://developer.arm.com/documentation/100966/latest/Getting-Started-with-Fixed-Virtual-Platforms/FVP-command-line-options) in the FVP Reference Guide for additional documentations.

## Model Configuration {#Config}

The operation of the FVP models can be configured at start-time by providing following command-line options:
 - using `-C` (or `--parameter`) option to configure individual parameters.
 - using option `-f` (or `--config-file`) followed by path to the text file with configuration parameters.

The configuration parameters are model-specific and follow syntax `instance.parameter= <value>`, where `instance` specifies a simulated instance, such as CPU, interface, bus, memory, peripheral,  etc. and can be also hierarchical.

All parameters available for a target model including default setting and brief description can be obtained with the command option `-l` (or `--list-params`). Because of the large number of parameters, it is convinient to print them into a text file. For example:

```
FVP_Corstone_SSE-300_Ethos-U55 --list-params > config.txt
```

In a simple case the content of the configuration file could be as shown below for FVP_Corstone_SSE-300 targets:

```
# Parameters:
# instance.parameter=value       #(type, mode) default = 'def value' : description : [min..max]
#------------------------------------------------------------------------------
core_clk.mul=100000000                              # (int   , init-time) default = '0x17d7840' : Clock Rate Multiplier. This parameter is not exposed via CADI and can only be set in LISA
mps3_board.telnetterminal0.start_telnet=0           # (bool  , init-time) default = '1'      : Start telnet if nothing connected
mps3_board.uart0.out_file=-                         # (string, init-time) default = ''       : Output file to hold data written by the UART (use '-' to send all output to stdout)
mps3_board.visualisation.disable-visualisation=1    # (bool  , init-time) default = '0'      : Enable/disable visualisation
cpu0.semihosting-enable=1                           # (bool  , init-time) default = '0'      : Enable semihosting SVC traps. Applications that do not use semihosting must set this parameter to false.
#------------------------------------------------------------------------------
```

Where:
 - **core_clk.mul=100000000** specifies the virtual time, in this case 100MHz CPU clock.
 - **mps3_board.telnetterminal0.start_telnet=0** disables the Telnet connectivity.
 - **mps3_board.uart0.out_file=-** UART output is send to stdout.
 - **mps3_board.visualisation.disable-visualisation=1** disables the graphical user interface of the FVP.
 - **cpu0.semihosting-enable=1** enables \ref semihosting "semihosting in the FVP".

Note that instances implemented in the model can be obtained with the command option `--list-instances` that returns instance names and corresponding Fast Model component type, version and brief description. Section [Fast Models components](https://developer.arm.com/documentation/100964/latest/Fast-Models-components) explains all the components available with FastModel technology and can be used for finding more information about a specific instance in the FVP.

For additional details also see chapter [Configuring the model](https://developer.arm.com/documentation/100966/latest/Getting-Started-with-Fixed-Virtual-Platforms/Configuring-the-model) in the Getting Started with Fixed Virtual Platforms Guide.

## Useful Hints and Tips {#Hints}

Below are some useful tips for using FVP models in common AVH scenarios.

### Execution stop {#stop}

Embedded applications typically run with an infinite loop that ensures continuous program execution. But for executing regression tests as part of Continuous Integration (CI) workflows it is often required that program execution is stopped after a test is completed, so that the next test can be started.

FVP models have `shutdown_on_eot` parameter that enables simple implementation of such program exit. The parameter should be set in the \ref Config, for example for FPV_Corstone_SSE-300:

```
mps3_board.uart0.shutdown_on_eot=1   # (bool, init-time) default = '0' : Shutdown simulation when a EOT (ASCII 4) char is transmitted (useful for regression tests when semihosting is not available)
```

And then to trigger the shutdown, a EOT (ASCII 4) symbol can be transmitted to the corresponding serial interface from the program. The code below demonstrates an example, where the execution is stopped after target execution count is achieved. In this implementation the STDIO is assumed to be retargeted to the UART0:

```c
  while (1)  {
    printf ("Hello World %d\r\n", count);
    if (count > 100) printf ("\x04");  // EOT (0x04) stops simulation
    count++;
    osDelay (1000);
  }
```

### Execution timing {#timing}

FVP simulation models are targeted to software development and functional testing, and are not  suitable for accurate performance comparisons on the CPU level. However, they can be well used to analyze timing on the program level, such as for scheduling RTOS tasks, detecting deadlocks, but also identifying overall performance trends.

Following mechanisms and settings can be used for timing control and measurements:
- FVP model can be started with command-line option `--stat` to print the execution statistics on simulation exit. Here is an example of such statistics output:
  ```
  --- cpu_core statistics: ------------------------------------------------------
  Simulated time                          : 0.651964s
  User time                               : 0.843750s
  System time                             : 0.109375s
  Wall time                               : 1.503559s
  Performance index                       : 0.43
  cpu_core.cpu0                           :  68.40 MIPS (    65196784 Inst)
  -------------------------------------------------------------------------------
  ```
  Also see [corresponding section](https://developer.arm.com/documentation/100965/latest/Timing-Annotation/Timing-annotation-tutorial/Setting-up-the-environment/Displaying-the-total-execution-time-of-the-simulation) in the Fast Models User Guide.

- [CMSIS-View](https://github.com/ARM-software/CMSIS-View) utility can be used to measure and analyze timing between events in the program, including statistical data. To store the log files on FVPs, \ref semihosting "semihosting" shall be enabled. CMSIS-View annotations can also be reused for event analysis and time measurement on real hardware.
- \ref Config parameters can be used to control and impact the execution timing:
  - With Cycle Per Instruction (CPI) settings `cpi_div` and `cpi_mul`.
  - With clock configurations such as Clock Rate Multiplier, for example `core_clk.mul` on Corstone-300.
  - With pipeline-impacting parameters such as for memory caches, Floating-Point-Unit (FPU) or M-Profile Vector Extensions (MVE), etc.
  .
Chapter [Timing Annotations](https://developer.arm.com/documentation/100965/latest/Timing-Annotation) in the Fast Models User Guide explains the performance estimation concept as implemented in the underlying FastModels technology. Note that the FVPs are built with Timing Annotations enabled (`FASTSIM_DISABLE_TA` set to 0).

### Semihosting {#semihosting}

Semihosting is a mechanism that enables code running on an FVP model to directly access the Input/Output facilities on a host computer, such as console I/O and file I/O.

This is often useful for testing and debugging your software when use of HW I/O interfaces in the model is not strictly required or would unnecessary complicate the program.

By default semihosting is disabled in FVPs and can be enabled with `semihosting-enable` configuration parameter on the CPU instance . For example for FVP_Corstone_SSE-300/310:

```
cpu0.semihosting-enable=1
```
and for FVP_MPS2_Cortex-M4:
```
armcortexm4ct.semihosting-enable=1
```

Semihosting can be useful in various scenarios with some of them listed below:
- [CMSIS-View](https://github.com/ARM-software/CMSIS-View) utility can be used with FVPs in semihosting mode to store the events into the log file on the host. See more in [Event Recorder semihosting](https://arm-software.github.io/CMSIS-View/main/er_use.html#er_semihosting).
- Direct use of the host platform when invoking `stdio.h` functions. This for example allows to bypass message redirection via UART.
