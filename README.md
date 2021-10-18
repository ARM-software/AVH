# Arm Virtual Hardware - Developer Resources

This repository gives you access to interface drivers that map to virtual targets and physical hardware along with Python scripts for I/O simulation. The [documentation](https://arm-software.github.io/VHT/main/overview/html/index.html) explains how to integrate Arm Virtual Hardware Targets (VHT) into typical CI/CD environments. Usage examples show typical usage cases and range from audio processing, ML algorithm testing, up to IoT applications that interface to Cloud Service providers.

**Arm Virtual Hardware** is now in public beta phase, is currently provided free of charge, and may be used only for evaluation. You may, for example, evaluate the development processes in CI/CD, MLOps and DevOps workflows which require automated testing.


## Resources

Resource       | Description
:--------------|:--------------------------------------------------
[Marketing Overview](https://www.arm.com/virtual-hardware)                                            | Gives you a top-level marketing message.
[Documentation](https://arm-software.github.io/VHT/main/overview/html/index.html)                     | Is a comprehensive documentation about **Arm Virtual Hardware**.
[AWS Marketplace](https://aws.amazon.com/marketplace/search/results?searchTerms=Arm+Virtual+Hardware) | **Arm Virtual Hardware** is available via a Cloud Service
[Product Roadmap](https://arm-software.github.io/VHT/main/overview/html/index.html#Roadmap)           | Lists the features that we will deploy in the next 6 months.
[Support Forum](https://community.arm.com/support-forums/f/arm-virtual-hardware-targets-forum)        | **Arm Virtual Hardware** is supported via a forum. Your feedback will influence future roadmap.
[TFL Micro Speech](https://github.com/arm-software/VHT-TFLmicrospeech)             | This example project shows the [**Arm VHT VSI interface**](https://arm-software.github.io/VHT/main/simulation/html/group__arm__vsi.html) with Audio input.


## Directory Structure

The content of this repository are the Developer Resources for **Arm Virtual Hardware**. 

Directory      | Description
:--------------|:--------------------------------------------------
[interface](https://github.com/ARM-software/VHT/tree/main/interface)      | [Virtual Interface APIs](https://arm-software.github.io/VHT/main/simulation/html/group__arm__cmvp.html) with drivers and Python scripts.
[infrastructure](https://github.com/ARM-software/VHT/tree/main/infrastructure)      | Scripts that help to integrate the [infrastructure services](https://arm-software.github.io/VHT/main/infrastructure/html/index.html) into workflows.
Doxygen        | Doxygen [documentation](https://arm-software.github.io/VHT/main/overview/html/index.html) of **Arm Virtual Hardware**. 
Documentation  | Temporary output directory for the [documentation](https://arm-software.github.io/VHT/main/overview/html/index.html).

Copyright (C) 2021, Arm Ltd.
