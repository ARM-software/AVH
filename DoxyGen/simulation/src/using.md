# Using AVH FVPs {#using}

This section gives an overview on how to use the **Arm Fixed Virtual Platforms (FVPs)** in command line interface.

[Infrastructure chapter](../../infrastructure/html/index.html) provides details on how to obtain AVH FVPs and use them in various cloud-native workflows or desktop setups, such as GitHub and Keil MDK.

## Running User Applications in CLI {#Execution}

The FVP models can be executed from command prompt by using the model name followed by the model options. Development tools may abstract the execution with GUI, but the underlying approach stays the same.

Below is an example of the command for running a program on the FVP model for Corstone-300 with Ethos-U55 in Linux environment:

```bash
FVP_Corstone_SSE-300_Ethos-U55 -a project.axf -C mps3_board.v_path=./vsi_py/ -f fvp_config.txt --simlimit 24 --stat
```

Where:
 - `FVP_Corstone_SSE-300_Ethos-U55` is the simulation model name. Note that on Windows the executable files shall be used, for example `FVP_Corestone_SSE-300_Ethos-U55.exe`. 
 - `-a` (or `--application`) option specifies the application binary file to run on the model (`project.axf` in this example).
 - `-f` (or `--config-file`) specifies the configuration file for the simulation model (`fvp_config.txt` in this case). See \ref Config.
 - `-C mp3_board.v_path` specifies model configuration parameter for VSI python scripts for \ref arm_cmvp (`"./vsi_py/"` here). Use `mp2_board.v_path`, `mps3_board.v_path` or `mps4_board.v_path`, depending on the underlying board.
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

