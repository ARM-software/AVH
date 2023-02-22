\page Using Using Arm Fixed Virtual Platforms

This section gives an overview on how to use the **Arm Fixed Virtual Platforms (FVPs)** in AVH context.

The FVP simulation models in AVH correspond to a subset of [Arm Fast Models Fixed Virtual Platforms](https://developer.arm.com/tools-and-software/simulation-models/fixed-virtual-platforms) with extensions for \ref arm_cmvp. 
They can be accessed in cloud-native and desktop environments as explained in [Infrastructure chapter](../../infrastructure/index.html). The table below lists the available models:

FVP Simulation Model           | Processor Core        | Overview Description
:------------------------------|:----------------------|:----------------------------------------
VHT_MPS2_Cortex-M0             | Cortex-M0             | [ARM Cortex-M0 SMM on V2M-MPS2 (AppNote AN382)](https://developer.arm.com/documentation/dai0382)
VHT_MPS2_Cortex-M0plus         | Cortex-M0+            | [ARM Cortex-M0+ SMM on V2M-MPS2 (AppNote AN383)](https://developer.arm.com/documentation/dai0383)
VHT_MPS2_Cortex-M3             | Cortex-M3             | [ARM Cortex-M3 SMM on V2M-MPS2 (AppNote AN385)](https://developer.arm.com/documentation/dai0385)
VHT_MPS2_Cortex-M4             | Cortex-M4             | [ARM Cortex-M4 SMM on V2M-MPS2 (AppNote AN386)](https://developer.arm.com/documentation/dai0386)
VHT_MPS2_Cortex-M7             | Cortex-M7             | [ARM Cortex-M7 SMM on V2M-MPS2 (AppNote AN399)](https://developer.arm.com/documentation/dai0386)
VHT_MPS2_Cortex-M23            | Cortex-M23            | [ARM Cortex-M23 IoT Subsystem for V2M-MPS2+ (AppNote AN519)](https://developer.arm.com/documentation/dai0519)
VHT_MPS2_Cortex-M33            | Cortex-M33            | [ARM Cortex-M33 IoT Subsystem for V2M-MPS2+ (AppNote AN505)](https://developer.arm.com/documentation/dai0505)
VHT_MPS3_Corstone_SSE-300      | Cortex-M55            | [Corstone-300 FVP Technical Overview (PDF)](./Corstone_SSE-300_Ethos-U55_FVP_MPS3_Technical_Overview.pdf),  [Memory map overview](https://developer.arm.com/documentation/100966/1118/Arm--Corstone-SSE-300-FVP/Memory-map-overview-for-Corstone-SSE-300)
VHT_Corstone_SSE-300_Ethos-U55 | Cortex-M55, Ethos-U55 | [Corstone-300 FVP Technical Overview (PDF)](./Corstone_SSE-300_Ethos-U55_FVP_MPS3_Technical_Overview.pdf),  [Memory map overview](https://developer.arm.com/documentation/100966/1118/Arm--Corstone-SSE-300-FVP/Memory-map-overview-for-Corstone-SSE-300)
VHT_Corstone_SSE-300_Ethos-U65 | Cortex-M55, Ethos-U65 | [Corstone-300 FVP Technical Overview (PDF)](./Corstone_SSE-300_Ethos-U55_FVP_MPS3_Technical_Overview.pdf),  [Memory map overview](https://developer.arm.com/documentation/100966/1118/Arm--Corstone-SSE-300-FVP/Memory-map-overview-for-Corstone-SSE-300)
VHT_Corstone_SSE-310           | Cortex-M85, Ethos-U55 | [Corstone-310 FVP Technical Overview (PDF)](./Corstone_SSE-310_FVP_Technical_Overview.pdf),  [Memory map overview](https://developer.arm.com/documentation/100966/1118/Arm--Corstone-SSE-310-FVP/Corstone-SSE-310-FVP-memory-map-overview)
VHT_Corstone_SSE-310_Ethos-U65 | Cortex-M85, Ethos-U65 | [Corstone-310 FVP Technical Overview (PDF)](./Corstone_SSE-310_FVP_Technical_Overview.pdf),  [Memory map overview](https://developer.arm.com/documentation/100966/1118/Arm--Corstone-SSE-310-FVP/Corstone-SSE-310-FVP-memory-map-overview)

Additionally following FVP models are provided without support of Virtual Peripherals:

Simulation Model               | Processor Core        | Overview Description
:------------------------------|:----------------------|:----------------------------------------
FVP_Corstone-1000              | Cortex-A35, Cortex-M0+, Cortex-M3 | [Arm Corstone-1000 for MPS3 (AppNote AN550)](https://developer.arm.com/documentation/dai0550/)


# Running User Applications {#Execution}

The FVP models can be executed from command prompt by using the model name followed by the model options. Development tools may abstract the execution with GUI, but the underlying approach stays the same.

Below is an example of the command for running a program on the FVP model for Corstone-300 with Ethos-U55 in Linux environment:

```
VHT_Corstone_SSE-300_Ethos-U55 -a Objects\microspeech.axf -V "..\VSI\audio\python" -f fvp_config.txt  --stat --simlimit 24
```

Where:
  - `VHT_Corstone_SSE-300_Ethos-U55` is the simulation model name. Note that on Windows the executable files shall be used, for example `VHT_Corestone_SSE-300_Ethos-U55.exe`. 
  - `-a` (or `--application`) option specifies the application binary file to run on the model (`Objects\microspeech.axf` in this example).
  - `-f` (or `--config-file`) specifies the configuration file for the simulation model (`fvp_config.txt` in this case). See \ref Config.
  - `-V` (or `--v_path`) specifies the path to python scripts for \ref arm_cmvp (`"..\VSI\audio\python"` here).
  - `--stat` instructs to print run statistics on simulation exit.
  - `--simlimit` specifies the maximum number of seconds to simulate.

The availalable command options can be listed using the `--help` option. See chapter [FVP-command-line-options](https://developer.arm.com/documentation/100966/latest/Getting-Started-with-Fixed-Virtual-Platforms/FVP-command-line-options) in the FVP Reference Guide for additional documentations.

# Model Configuration {#Config}

The operation of the FVP models can be configured at start-time by providing following command-line options:
 - using `-C` (or `--parameter`) option to configure individual parameters.
 - using option `-f` (or `--config-file`) followed by path to the text file with configuration parameters.

The configuration parameters are model-specific and follow syntax `instance.parameter= <value>`, where `instance` specifies a simulated instance, such as CPU, interface, bus, memory, peripheral,  etc. and can be also hierarchical. Available instances can be obtained with the command option `--list-instances`.

All parameters available for a target model including default setting and brief description can be obtained with the command option `-l` (or `--list-params`). Because of the large number of parameters, it is convinient to print them into a text file. For example:

```
VHT_Corstone_SSE-300_Ethos-U55 --list-params > config.txt
```

For additional details see chapter [Configuring-the-model](https://developer.arm.com/documentation/100966/1120/Getting-Started-with-Fixed-Virtual-Platforms/Configuring-the-model) in the 
Getting Started with Fixed Virtual Platforms Guide.

In a simple case the content of the configuration file could be as shown below for VHT_Corstone_SSE-300 targets:

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


## Execution stop

Embedded applications typically run with an infinite loop that ensures continuous program execution. But for executing regression tests as part of Continuous Integration (CI) workflows it is often required that program execution is stopped after a test is completed, so that the next test can be started.

FVP models have `shutdown_on_eot` parameter that enables simple implementation of such program exit. The parameter should be set in the model configuration file (*fvp_config.txt* explained above), for example for VHT_Corstone_SSE-300:

```
mps3_board.uart0.shutdown_on_eot=1   # (bool, init-time) default = '0' : Shutdown simulation when a EOT (ASCII 4) char is transmitted (useful for regression tests when semihosting is not available)
```

And then to trigger the shutdown, a EOT (ASCII 4) symbol can be transmitted to the corresponding serial interface from the program. The code below demonstrates an example, where the execution is stopped after target execution count is achieved. In this implementation the STDIO is assumed to be retargeted to the UART0:

```
  while (1)  {
    printf ("Hello World %d\r\n", count);
    if (count > 100) printf ("\x04");  // EOT (0x04) stops simulation
    count++;
    osDelay (1000);
  }
```
