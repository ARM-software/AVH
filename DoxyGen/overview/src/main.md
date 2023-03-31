\mainpage Introduction

[comment]:[TOC]

**Arm Virtual Hardware (AVH)** provides simulation models, software tooling, and infrastructure that can be integrated into [**CI/CD**](https://en.wikipedia.org/wiki/CI/CD) and [**MLOps**](https://en.wikipedia.org/wiki/MLOps) development flows. 

AVH supports the software development cycle of embedded, IoT, and ML applications and provides essential components for effective test and validation environments. Arm Virtual Hardware is flexible and can run any [**RTOS**](https://en.wikipedia.org/wiki/Real-time_operating_system) that is designed for Cortex-M or bare metal code that interacts with the processor. 

Arm Virtual Hardware offers a comprehensive tool integration along with resources for software developers and can therefore run complex applications and software integration tests. A potential workload could be a [**sensor-fusion**](https://en.wikipedia.org/wiki/Sensor_fusion) Machine Learning (ML) application that connects to the Internet via an IoT operating system.

**Arm Virtual Hardware** consists of the following components:

  - **Arm Fixed Virtual Platforms (FVPs)** are precise [**simulation models**](https://en.wikipedia.org/wiki/Simulation) of Cortex-M device sub-systems and are designed for complex software verification and testing. This allows [**simulation-based test automation**](https://en.wikipedia.org/wiki/Test_automation) of various software workloads, including unit tests, integration tests, and fault injection.

  - **Arm Virtual Hardware Services** provide a cloud-native infrastructure for software test and validation. These services can be integrated into various **CI/CD** and **MLOps** environments that range from GitHub to on-premise IT infrastructure.
 
  - **Arm Virtual Hardware Developer Resources** gives you access to interface drivers that map to virtual targets and physical hardware along with Python scripts for I/O simulation. The documentation explains how to integrate Arm Virtual Hardware into typical **CI/CD** environments. Usage examples show typical usage cases and range from audio processing, ML algorithm testing, up to IoT applications that interface to Cloud Service providers.
  
  - **Software Development Environments** can be used with Arm Virtual Hardware. So, Arm Fixed Virtual Platforms are an integral part of the Keil MDK Professional Edition that is a comprehensive software tool suite for creating Cortex-M-based applications and related validation and test processes. Other IDEs and debuggers can be used as well. 

![Arm Virtual Hardware - Components](./images/vht_overview.png)


# Documentation Structure {#Sections}

Section                                                    | Description
:----------------------------------------------------------|:--------------------
[**Overview**](index.html)                                 | Introduces **Arm Virtual Hardware** along with the top-level structure.
[**Simulation**](../../simulation/html/index.html)         | Explains the simulation technology and the virtual interfaces.
[**Infrastructure**](../../infrastructure/html/index.html) | Describes how to setup development workflows with **Arm Virtual Hardware**, locally and in the cloud.
[**Examples**](../../examples/html/index.html)             | Guides through the examples that demonstrate how to use **Arm Virtual Hardware**.

# User Benefits {#User_Benefits}

## Test without Hardware {#No_Hardware}

AVH allows to verify your code without the need for physical hardware which provides a robust test environment that enables:
 - Early software development for faster time-to-market
 - Select optimal target device once the software workload is analysed
 - Re-target applications to production hardware with driver abstractions

## Verify Correctness {#Verify}

**Arm Fixed Virtual Platforms (FVPs)** are Arm simulation models validated with the same process as the CPU IP. Specially it allows you to:
 - Perform algorithm testing with identical logical behaviour of the target device
 - Precisely repeat complex input patterns in CI/CD test environments
 - Analyse software behaviour with event annotations

## Evaluate Performance {#Evaluate}

Software algorithms for Digital Signal Processing (DSP) or Machine Learning (ML) frequently require significant CPU resources and need to be optimized for the target hardware. Comparing performance of such "load heavy" algorithms requires that they can be automatically executed with different configurations parameters but using identical input. 

**Arm Virtual Hardware Services** allows users to test their programs at scale with reproducible input patterns and so validate and optimize application performance which allows you to:
 - Compare speed of different implementations of an algorithm
 - Identify timing issues during system integration
 - Optimize resources (i.e. data buffers) towards application requirements

## Continuous Testing {#CI}

Applying continuous integration work flows for embedded applications can be complicated by the specifics of development environments and the need of executing the program on target hardware. So the development teams are often reluctant to spend initial effort setting up the continuous integration (CI) workflow even though the long-term benefits are undisputed as shown on the Figure below

![Comparison of test efforts in CI and no CI workflows](./images/effort_comparison.png)

**Arm Virtual Hardware** simplifies the setup and use of CI workflows in embedded projects.

For unit and integration tests virtual targets offer additional advantages over hardware, including:
 - **Speed** - no overhead for flashing the application on physical hardware. This saves time on small and fast unit tests. 
 - **Scale** - virtual platforms can scale to run many tests in parallel. This makes virtual platforms more cost-effective than a farm of physical hardware. 
 - **Maintenance** – unlike physical hardware, virtual platforms do not overheat, wear out from overuse, break from misuse, or use physical space and resources. 
 - **Upgrades** – virtual platforms can be adapted and re-configured to match corresponding changes to the underlying hardware platform that is under development. These types of changes can be costly or impossible with physical hardware.

# Release History {#History}

For details of the AVH AMI content see [AMI Inventory](../../infrastructure/html/ami_inventory.html).

<table>
<tr>
<th>Version</th>
<th>Changes</th>
</tr>
<tr>
<td>1.3.1-beta (Jan 26, 2023)</td>
<td>
 - License validity period for installed Arm tools is extended.
 - EULA for AVH AMI is updated on AWS marketplace.
</td>
</tr>
<tr>
<td>1.3.0-beta (Sept 22, 2022)</td>
<td>
 - Arm Corstone SSE-300 model is supported with [**Keil Studio Cloud**](https://www.keil.arm.com/boards/arm-v2m-mps3-sse-300-fvp-610bb98/).
 - Provided [**eventlist utility**](https://github.com/ARM-software/CMSIS-View/tree/main/tools/eventlist) to process Event Recorder logs obtained with Arm FVP targets.
 - Added new FVP model - VHT_Corstone_SSE-310_Ethos-U65 to the AMI, see [Using Arm Fixed Virtual Platforms](../../simulation/html/Using.html).
 - Added installation of [**CMSIS-Toolbox v1.0.0**](https://github.com/Open-CMSIS-Pack/CMSIS-Toolbox) to the AMI, that also includes CMSIS-Build for command-line project builds.
 - Updated [**examples**](../../examples/html/index.html) to use dynamic credentials (IAM Role) in the GitHub CI workflow, removing the need for storing AWS credentials in GitHub Secrets.
 - Removed preinstalled Bootloader and OpenSuSE software for Corstone-1000.
 - Removed preinstalled CMSIS Packs.
</td>
</tr>
<tr>
<td>1.2.3-beta (July 9, 2022)</td>
<td>
 - Enabled timing annotations in FVPs by default ([FASTSIM_DISABLE_TA](https://developer.arm.com/documentation/100965/1117/Timing-Annotation/Enabling-and-disabling-timing-annotation) is set to 0).<br/>If disabled (FASTSIM_DISABLE_TA set to 1), VSI streams data too quickly and prevents normal execution of [ATS-Keyword Example] (https://github.com/ARM-software/open-iot-sdk/tree/main/examples/ats-keyword).
</td>
</tr>
<tr>
<td>1.2.2-beta (May 10, 2022)</td>
<td>
 - New versioning scheme to match the AMI version (see [AMI Inventory](../../infrastructure/html/ami_inventory.html)).
 - [**CMSIS-RTOS2 Validation**](https://github.com/ARM-software/CMSIS-RTOS2_Validation): Advanced test suite for validating CMSIS-RTOS2 implementations on supported Cortex-M cores runs using AVH.
 - Corstone-310 model fixes: NPU access fix as well as a parameter for the flash region size allowing it to be a maximum of 64MB.
</td>
</tr>
<tr>
<td>0.3-beta (Apr 2022)</td>
<td>Added features:
 - [**Corstone-310 and Corstone-1000**](../../simulation/html/Using.html): added new simulation models.
 - [**Integration with Jenkins**](../../infrastructure/html/run_ami_jenkins.html): example of AVH AMI usage in Jenkins CI pipelines.
 - [**Event Recorder Semihosting Support**](https://www.keil.com/pack/doc/compiler/EventRecorder/html/er_use.html#er_semihosting): allows to generate Event Recorder logs in AVH AMI environment.
 - [**AWS MQTT Example**](../../examples/html/aws_mqtt.html): IoT application with MQTT connectivity to AWS cloud service.
 - [**ATS-Keyword Example**](https://github.com/ARM-software/open-iot-sdk/tree/main/examples/ats-keyword): keyword detection application based on [Arm Total Solutions for IoT](https://github.com/ARM-software/ATS-Keyword/).
</td>
</tr>
<tr>
<td>0.2-beta (Feb 2022)</td>
<td>Added features:
 - [**Extended Target support**](../../simulation/html/Using.html): additional Cortex-M processors are supported: Cortex-M0/M0+/M3/M4/M7/M23/M33.
 - [**Support in MDK-Professional**](../../infrastructure/html/run_mdk_pro.html): enables desktop development in classic tooling.
 - [**VIO Interface**](../../simulation/html/group__arm__vio.html): simple interface to control I/O such as switches and LEDs via Python scripts.
 - [**VSocket Interface**](../../simulation/html/group__arm__vsocket.html): BSD socket interface that connects the application under test to networks, including public Internet.
 - [**Get-Started example**](../../examples/html/GetStarted.html): added simple example demonstrating how to setup a Continuous Integration (CI) workflow using Arm Virtual Hardware.
</td>
</tr>
<tr>
<td>0.1-beta (Nov 2021)</td>
<td>Initial release</td>
</tr>
</table>

# Known Limitations {#Issues}

The current beta version of of Arm Virtual Hardware has the following known issues:

[**Virtual Interfaces**](../../simulation/html/group__arm__cmvp.html):
  - After processor reset virtual interfaces may not work correctly. So it is required to restart the debug/run session.

# Feedback and Support {#Support}

Arm Virtual Hardware is supported during public beta via this [Arm forum](https://community.arm.com/support-forums/f/arm-virtual-hardware-forum). Your feedback will influence our future roadmap and we try to help you promptly with your questions.
