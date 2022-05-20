# Arm Virtual Hardware - Developer Resources

This repository gives you access to interface drivers that map to virtual targets and physical hardware along with Python scripts for I/O simulation. The [documentation](https://arm-software.github.io/AVH/main/overview/html/index.html) explains how to integrate Arm Virtual Hardware Targets into typical CI/CD environments. Usage examples show typical usage cases and range from audio processing, ML algorithm testing, up to IoT applications that interface to Cloud Service providers.

**Arm Virtual Hardware (AVH)** is now in public beta phase, is currently provided free of charge, and may be used only for evaluation. You may, for example, evaluate the development processes in CI/CD, MLOps and DevOps workflows which require automated testing.


## Resources

Resource       | Description
:--------------|:--------------------------------------------------
[Marketing Overview](https://www.arm.com/virtual-hardware)                                            | Gives you a top-level marketing message.
[Documentation](https://arm-software.github.io/AVH/main/overview/html/index.html)                     | Is a comprehensive documentation about **Arm Virtual Hardware**.
[AWS Marketplace](https://aws.amazon.com/marketplace/search/results?searchTerms=Arm+Virtual+Hardware) | **Arm Virtual Hardware** is available via a Cloud Service
[Support Forum](https://community.arm.com/support-forums/f/arm-virtual-hardware-targets-forum)        | **Arm Virtual Hardware** is supported via a forum. Your feedback will influence future roadmap.
[AVH Client](https://github.com/ARM-software/avhclient)                                               | Python module for deploying **Arm Virtual Hardware**.
[Keil MDK Support](https://www.keil.com/pr/article/1298.htm)                                          | **Arm Virtual Hardware** is provided to users of the MDK-Professional edition at no extra cost.

The following example projects show the usage of **Arm Virtual Hardware**.

Examples       | Description
:--------------|:--------------------------------------------------
[GetStarted](https://github.com/ARM-software/AVH-GetStarted)                       | Example and project template for unit testing that shows CI and desktop development flows.
[TFL Micro Speech](https://github.com/arm-software/AVH-TFLmicrospeech)             | Example project that shows the [**Arm AVH VSI interface**](https://arm-software.github.io/AVH/main/simulation/html/group__arm__vsi.html) with Audio input.
[AWS MQTT Demo](https://github.com/ARM-software/AVH-AWS_MQTT_Demo)                 | Example project that utilizes [**IP connectivity via VSocket Interface**](https://arm-software.github.io/AVH/main/simulation/html/group__arm__vsocket.html) to connect to a cloud service.
[System Modeling](https://github.com/arm-software/AVH-SystemModeling)              | Example project that connects to a [**Modelica simulation**](https://modelica.org/) of a room acoustic. 
[RTOS Validation](https://github.com/ARM-software/CMSIS-RTOS2_Validation)          | CI test example that shows validation of CMSIS-RTOS2 compliant real-time operating systems.


## Directory Structure

The content of this repository are the Developer Resources for **Arm Virtual Hardware (AVH)**. 

Directory      | Description
:--------------|:--------------------------------------------------
[interface](https://github.com/ARM-software/AVH/tree/main/interface)      | [Virtual Interface APIs](https://arm-software.github.io/AVH/main/simulation/html/group__arm__cmvp.html) with drivers and Python scripts.
[infrastructure](https://github.com/ARM-software/AVH/tree/main/infrastructure)      | Scripts that help to integrate the [infrastructure services](https://arm-software.github.io/AVH/main/infrastructure/html/index.html) into workflows.
Doxygen        | Doxygen sources for  Arm Virtual Hardware documentation.
Documentation  | Temporary output directory for the [documentation](https://arm-software.github.io/AVH/main/overview/html/index.html).

Copyright (C) 2021, 2022, Arm Ltd.
