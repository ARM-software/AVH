\page Using Using \prj_name Targets

This section describes how to use the **\prj_name Targets (VHT)**.  

The VHT simulation models are based on the [Arm Fast Models Fix Virtual Platforms](https://developer.arm.com/tools-and-software/simulation-models/fixed-virtual-platforms) with extensions for \ref arm_cmvp.  The table below shows the available models:

VHT Simulation Models | Processors                           | Overview Description
:---------------------|:-------------------------------------|:-------------------------------------------
VHT-Corstone-300      | Cortex-M55, Ethos-U55                | [Corstone-300 FVP Technical Overview (PDF)](./Corstone_SSE-300_Ethos-U55_FVP_MPS3_Technical_Overview.pdf)

\note 
ON ROADMAP: Extensions that capture Event Recorder annotations are in development.
\note 
ON ROADMAP: VHT simulation models for other Cortex-M processors.

# Command Line Options {#Options}

The command line options can be listed using the -help command. For example:

```
VHT-Corstone-300.exe -help
```

The VHT simulation models can be configured using the option *-f FILE* that specifies a *config-file*. The available *config-file* options can be listed with the option *-l*.

# Usage Example {#Example}
```
VHT-Corstone-300.exe -V "..\VSI\audio\python" -f fvp_config.txt -a Objects\microspeech.axf --stat --cyclelimit 768000000
```

Where:
  - **-V** specifies that path to the Python scripts for \ref arm_cmvp.
  - **-f** specifies the *config-file* for the VHT simulation model.
  - **-a** specifies the application to load.
  - **--stat** instructs to print run statistics on simulation exit.
  - **--cyclelimit** specifies a cycle limit where the simulation terminates.

The content of the *fvp_config.txt* could be:
```
# Parameters:
# instance.parameter=value       #(type, mode) default = 'def value' : description : [min..max]
#------------------------------------------------------------------------------
cpu_core.core_clk.mul=32000000                                 # (int   , init-time) default = '0x17d7840' : Clock Rate Multiplier. This parameter is not exposed via CADI and can only be set in LISA
cpu_core.mps3_board.telnetterminal0.start_telnet=0             # (bool  , init-time) default = '1'      : Start telnet if nothing connected
cpu_core.mps3_board.uart0.out_file=-                           # (string, init-time) default = ''       : Output file to hold data written by the UART (use '-' to send all output to stdout)
cpu_core.mps3_board.visualisation.disable-visualisation=1      # (bool  , init-time) default = '0'      : Enable/disable visualisation
#------------------------------------------------------------------------------
```

Where:
 - **cpu_core.core_clk.mul=32000000** specifies the virtual time, in this case 32MHz CPU clock.
 - **cpu_core.mps3_board.telnetterminal0.start_telnet=0** disables the Telnet connectivity.
 - **cpu_core.mps3_board.uart0.out_file=-** UART output is send to stdout.
 - **cpu_core.mps3_board.visualisation.disable-visualisation=1** disables the graphical user interface of the FVP.
