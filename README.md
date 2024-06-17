# AVH FVPs: Arm Virtual Hardware with Fixed Virtual Platforms

This repository explains the use of Arm Virtual Hardware on Fixed Virtual Platforms (AVH FVP).

The [documentation](https://arm-software.github.io/AVH/main/overview/html/index.html) describes how to integrate AVH FVPs into typical CI/CD workflows as well as desktop development environments. Additional interface drivers are provided that map to virtual targets and physical hardware along with Python scripts for I/O simulation.

## Resources

Resource       | Description
:--------------|:--------------------------------------------------
[Marketing Overview](https://www.arm.com/virtual-hardware)                                            | Gives you a top-level marketing message.
[Documentation](https://arm-software.github.io/AVH/main/overview/html/index.html)                     | Is a comprehensive documentation about AVH FVPs.
[Support Forum](https://community.arm.com/support-forums/f/arm-virtual-hardware-targets-forum)        | Arm Virtual Hardware is supported via a forum. Your feedback will influence future roadmap.


The table below lists some of the example projects that demonstrate the usage of AVH FVPs. Also see [Examples](https://arm-software.github.io/AVH/main/examples/html/index.html) in the documentation.

Examples       | Description
:--------------|:--------------------------------------------------
[GetStarted](https://github.com/ARM-software/AVH-GetStarted)                       | Example and project template for unit testing that shows CI and desktop development flows.
[TFL Micro Speech](https://github.com/arm-software/AVH-TFLmicrospeech)             | Example project that shows the [**Arm AVH VSI interface**](https://arm-software.github.io/AVH/main/simulation/html/group__arm__vsi.html) with Audio input.
[AWS MQTT Demo](https://github.com/ARM-software/AVH-AWS_MQTT_Demo)                 | Example project that utilizes [**IP connectivity via VSocket Interface**](https://arm-software.github.io/AVH/main/simulation/html/group__arm__vsocket.html) to connect to a cloud service.
[System Modeling](https://github.com/arm-software/AVH-SystemModeling)              | Example project that connects to a [**Modelica simulation**](https://modelica.org/) of a room acoustic.
[RTOS Validation](https://github.com/ARM-software/CMSIS-RTOS2_Validation)          | CI test example that shows validation of CMSIS-RTOS2 compliant real-time operating systems.

[VsCode Get Started](https://github.com/Open-CMSIS-Pack/vscode-get-started) | Hello world example for AVH FVPs with support of GitHub Actions for build and run
[AVH_CI_Template](https://github.com/Arm-Examples/AVH_CI_Template)          | Simple example with unit tests that shows the CI setup with AVH FVPs using GitHub Actions
[Hello VSI Examples](https://github.com/Arm-Examples/Hello_AVH)       | Simple examples that streams data from a file via Virtual Streaming Interface (VSI)
[AVH-MLOps](https://github.com/ARM-software/AVH-MLOps)               | A set of tools and software components and examples showcasing MLOps systems with AVH FVPs
[CMSIS-Core Validation](https://github.com/ARM-software/CMSIS_6/tree/main/CMSIS/CoreValidation)  | Test suite for validating CMSIS-Core implementations on Cortex-M cores using different toolchains and AVH FVPs
[CMSIS-RTOS2 Validation](https://github.com/Arm-Software/CMSIS-RTOS2_Validation)  | Test suite for validating CMSIS-RTOS2 implementations on Cortex-M cores using different toolchains and AVH FVPs

## Directory Structure

The content of this repository:

Directory      | Description
:--------------|:--------------------------------------------------
[interface](https://github.com/ARM-software/AVH/tree/main/interface)      | [Virtual Interface APIs](https://arm-software.github.io/AVH/main/simulation/html/group__arm__cmvp.html) with drivers and Python scripts.
[infrastructure](https://github.com/ARM-software/AVH/tree/main/infrastructure)      | Scripts that help to integrate the [infrastructure services](https://arm-software.github.io/AVH/main/infrastructure/html/index.html) into workflows.
Doxygen        | Doxygen sources for Arm Virtual Hardware FVP documentation.
Documentation  | Temporary output directory for the [documentation](https://arm-software.github.io/AVH/main/overview/html/index.html).

Copyright (C) 2021-2024, Arm Ltd.
