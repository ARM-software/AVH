# AMI Inventory {#ami_inventory}

Sections below list the resources preinstalled on the corresponding version of Arm Virtual Hardware AMI. It is also possible to [obtain the current AMI Inventory](#inventory) on a running AMI instance.
 - [AMI v1.2.1](#ami_inventory_121)
 - [AMI v1.2.0](#ami_inventory_120)

## AMI v1.2.1 {#ami_inventory_121}

|  Item                                | Version<sup>1</sup>|
|--------------------------------------|-------------------|
|**HOST OS**                           |                   |
| &emsp;Ubuntu                         | x86_64 v20.04.1   |
|**COMPILERS**                         |                   |
| &emsp;Arm Compiler                   | 6.18              |
| &emsp;GCC Compiler                   | 11.2              |
| &emsp;Vela                           | 3.3.0             |
|**VIRTUAL HARDWARE TARGETS**          |                   |
| &emsp;VHT_MPS2_Cortex-M0             | 11.17.38          |
| &emsp;VHT_MPS2_Cortex-M0plus         | 11.17.38          |
| &emsp;VHT_MPS2_Cortex-M3             | 11.17.38          |
| &emsp;VHT_MPS2_Cortex-M4             | 11.17.38          |
| &emsp;VHT_MPS2_Cortex-M7             | 11.17.38          |
| &emsp;VHT_MPS2_Cortex-M23            | 11.17.38          |
| &emsp;VHT_MPS2_Cortex-M33            | 11.17.38          |
| &emsp;VHT_Corstone_SSE-300           | 11.17.38          |
| &emsp;VHT_Corstone_SSE-300_Ethos-U55 | 11.17.38          |
| &emsp;VHT_Corstone_SSE-300_Ethos-U65 | 11.17.38          |
| &emsp;VHT_Corstone_SSE-310           | 11.17.38          |
|**FIXED VIRTUAL PLATFORM (FVP)**      |                   |
| &emsp;FVP_Corstone-1000              | 11.17.35          |
|**CORSTONE 1000 SOFTWARE**            |                   |
| &emsp;Bootloader + TF                | CORSTONE1000-2022.04.07 |
| &emsp;OpenSuSE                       | Snapshot20220331  |
| **CMSIS PACKS**                      |                   |
| &emsp;ARM.CMSIS.pack                 | 5.9.0 (U)         |
| &emsp;ARM.V2M_MPS3_SSE_300_BSP.pack  | 1.2.0             |
| &emsp;Keil.ARM_Compiler.pack         | 1.7.2 (U)         |
| **OTHER**                            |                   |
| &emsp;CMSIS-Build                    | 0.10.6            |

>  <sup>1</sup> If an item is different from the previous AMI version this is indicated in parenthesis () as follows:<br/>
> <ul><li>(N): Item is newly introduced to this AMI.</li><br/>
> <li>(U): Item version is updated from the previous AMI version.</li></ul>

**Environment setup**

Following setup is additionally performed for the bash terminal session in the `.bash_rc` file:

```
`echo "==== Arm Virtual Hardware AMI ===="
export PATH=$PATH:/opt/armcompiler/bin
export PATH=$PATH:/opt/gcc-arm-11.2-2022.02-x86_64-arm-none-eabi/bin
alias FVP_Corstone-1000=/opt/FVP_Corstone_1000/models/Linux64_GCC-9.3/FVP_Corstone-1000
export CMSIS_PACK_ROOT=/home/ubuntu/packs
echo "CMSIS packs are installed at $CMSIS_PACK_ROOT"
export CMSIS_COMPILER_ROOT=/opt/cbuild/etc
export CMSIS_BUILD_ROOT=/opt/cbuild/bin
export PATH=/opt/cbuild/bin:$PATH
export ARMLMD_LICENSE_FILE=/opt/data.dat
export PATH=$PATH:/opt/VHT
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/VHT
export ARMCOMPILER6_CLANGOPT=-Wno-license-management
export ARMCOMPILER6_LINKOPT=--diag_suppress=9931
export ARMCOMPILER6_FROMELFOPT=--diag_suppress=9931
export ARMCOMPILER6_ASMOPT=--diag_suppress=9931
```

## AMI v1.2.0 {#ami_inventory_120}

|  Item                                | Version<sup>1</sup>|
|--------------------------------------|-------------------|
|**HOST OS**                           |                   |
| &emsp;Ubuntu                         | x86_64 v20.04.1   |
|**COMPILERS**                         |                   |
| &emsp;Arm Compiler                   | 6.18 (U)          |
| &emsp;GCC Compiler                   | 11.2              |
| &emsp;Vela                           | 3.3.0             |
|**VIRTUAL HARDWARE TARGETS**          |                   |
| &emsp;VHT_MPS2_Cortex-M0             | 11.17.38 (U)      |
| &emsp;VHT_MPS2_Cortex-M0plus         | 11.17.38 (U)      |
| &emsp;VHT_MPS2_Cortex-M3             | 11.17.38 (U)      |
| &emsp;VHT_MPS2_Cortex-M4             | 11.17.38 (U)      |
| &emsp;VHT_MPS2_Cortex-M7             | 11.17.38 (U)      |
| &emsp;VHT_MPS2_Cortex-M23            | 11.17.38 (U)      |
| &emsp;VHT_MPS2_Cortex-M33            | 11.17.38 (U)      |
| &emsp;VHT_Corstone_SSE-300           | 11.17.38 (U)      |
| &emsp;VHT_Corstone_SSE-300_Ethos-U55 | 11.17.38 (U)      |
| &emsp;VHT_Corstone_SSE-300_Ethos-U65 | 11.17.38 (U)      |
| &emsp;VHT_Corstone_SSE-310           | 11.17.38 (N)      |
|**FIXED VIRTUAL PLATFORM (FVP)**      |                   |
| &emsp;FVP_Corstone-1000              | 11.17.35 (N)      |
|**CORSTONE 1000 SOFTWARE**            |                   |
| &emsp;Bootloader + TF                | CORSTONE1000-2022.04.07 (N)|
| &emsp;OpenSuSE                       | Snapshot20220331 (N) |
| **CMSIS PACKS**                      |                   |
| &emsp;ARM.CMSIS.pack                 | 5.8.0             |
| &emsp;ARM.V2M_MPS3_SSE_300_BSP.pack  | 1.2.0             |
| &emsp;Keil.ARM_Compiler.pack         | 1.7.1 (U)         |
| **OTHER**                            |                   |
| &emsp;CMSIS-Build                    | 0.10.6 (U)        |

>  <sup>1</sup> If an item is different from the previous AMI version this is indicated in parentheses () as follows:<br/>
> <ul><li>(N): Item is newly introduced to this AMI.</li><br/>
> <li>(U): Item version is updated from the previous AMI version.</li></ul>

## Obtaining AMI Inventory {#inventory}

To obtain the list of tools installed in the AMI instance use:

```
$ ./tool-inventory.sh
```

Following output shall be expected by default on AMI v1.2.1:

```
ubuntu@ip-10-252-70-251:~$ ./tool-inventory.sh
Arm Compiler information:
Product: Arm Compiler for Embedded 6.18 Professional
Component: Arm Compiler for Embedded 6.18
Tool: armclang [5e4cc700]

Target: arm-arm-none-eabi

GNU Compiler information:
arm-none-eabi-gcc (GNU Toolchain for the Arm Architecture 11.2-2022.02 (arm-11.14)) 11.2.1 20220111
Copyright (C) 2021 Free Software Foundation, Inc.
This is free software; see the source for copying conditions. There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Corstone-1000 FVP information:

Fast Models [11.17.35 (Apr 8 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

Vela Compiler information:
3.3.0

CMSIS build information:
(cbuild.sh): Build Invocation 0.10.6 (C) 2021 ARM
error: missing required argument <project>.cprj
Usage:
cbuild.sh <ProjectFile>.cprj
[--toolchain=<Toolchain> --outdir=<OutDir> --intdir=<IntDir> <CMakeTarget>]

<ProjectFile>.cprj : CMSIS Project Description input file
--toolchain=<Toolchain> : select the toolchain
--intdir=<IntDir> : set intermediate directory
--outdir=<OutDir> : set output directory
--quiet : suppress output messages except build invocations
--clean : remove intermediate and output directories
--update=<CprjFile> : generate <CprjFile> for reproducing current build
--help : print usage
--log=<LogFile> : save output messages in a log file
--jobs=<N> : number of job slots for parallel execution
--cmake[=<BuildSystem>] : select build system, default <BuildSystem>=Ninja
<CMakeTarget> : optional CMake target name

Arm Virtual Hardware Targets information:
VHT_Corstone_SSE-300_Ethos-U55 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_Corstone_SSE-300_Ethos-U65 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_Corstone_SSE-310 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M0 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M0plus information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M23 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M3 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M33 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M4 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS2_Cortex-M7 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.

VHT_MPS3_Corstone_SSE-300 information:

Fast Models [11.17.38 (Apr 20 2022)]
Copyright 2000-2022 ARM Limited.
All Rights Reserved.

Info: /OSCI/SystemC: Simulation stopped by user.
```

For the list of locally installed CMSIS Packs use:

```
$ cp_list.sh
```

For example, default output on a new AMI instance would be:

```
ubuntu@ip-10-252-70-253:~$ cp_list.sh
Software packs are installed at: /home/ubuntu/packs

Currently installed software packs:

ARM.V2M_MPS2_SSE_300_BSP.1.2.0.pack
ARM.CMSIS.5.9.0.pack
Keil.ARM_Compiler.1.7.2.pack
```