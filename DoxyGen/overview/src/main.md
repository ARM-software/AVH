\mainpage Introduction

**\prj_name** provides simulation models, software tooling, and infrastructure that can be integrated into [**CI/CD**](https://en.wikipedia.org/wiki/CI/CD) and [**MLOps**](https://en.wikipedia.org/wiki/MLOps) development flows. **\prj_name** supports the software development cycle of embedded, IoT, and ML applications and provides essential components for effective test and validation environments. **\prj_name** is flexible and can run any [**RTOS**](https://en.wikipedia.org/wiki/Real-time_operating_system) that is designed for Cortex-M or bare metal code that interacts with the processor. **\prj_name** offers a comprehensive tool integration along with resources for software developers and can therefore run complex applications and software integration tests. A potential workload could be a [**sensor-fusion**](https://en.wikipedia.org/wiki/Sensor_fusion) Machine Learning (ML) application that connects to the Internet via an IoT operating system.

**\prj_name** consists of the following components:

  - **\prj_name Targets (VHT)** are precise [**simulation models**](https://en.wikipedia.org/wiki/Simulation) of Cortex-M device sub-systems and are designed for complex software verification and testing. It allows [**simulation-based test automation**](https://en.wikipedia.org/wiki/Test_automation) of various software workloads, including unit tests, integration tests, and fault injection. 

  - **\prj_name Services** provide a cloud-native infra-structure for software test and validation. These \prj_name services can be integrated into various **CI/CD** and **MLOps** environments that range from GitHub to on-premise IT infrastructure. The Arm VHT services will be available via the AWS Marketplace (and later also via other Cloud Service providers).
 
  - **\prj_name Developer Resources** gives you access to interface drivers that map to virtual targets and physical hardware along with Python scripts for I/O simulation. The documentation explains how to integrate Arm VHT into typical **CI/CD** environments. Usage examples show typical usage cases and range from audio processing, ML algorithm testing, up to IoT applications that interface to Cloud Service providers.
  
  - **Software Development Environments** with Arm VHT integration are also available. \prj_name is an integral part of the Keil MDK Professional Edition that is a comprehensive software tool suite for creating Cortex-M-based applications and related validation and test processes. In future, the next-generation Keil Studio will also integrate \prj_name.

\image html "vht_overview.png" "\prj_name - Components"


# Documentation Structure {#Sections}

Section                                                    | Description
:----------------------------------------------------------|:--------------------
[**Overview**](index.html)                                 | Introduces **\prj_name** along with the top-level structure.
[**Simulation**](../../simulation/html/index.html)         | Explains the **\prj_name** Targets along with the simulation technology and the virtual interfaces.
[**Infrastructure**](../../infrastructure/html/index.html) | Describes how to setup development work flows with **\prj_name**.
[**Examples**](../../examples/html/index.html)             | Guides you through the examples demonstrating how to use **\prj_name**.


# User Benefits {#User_Benefits}

## Test without Hardware {#No_Hardware}

**\prj_name** allows to verify your code without the need for physical hardware which provides a robust test environment that enables:
 - Early software development for faster time-to-market
 - Select optimal target device once the software workload is analysed
 - Re-target applications to production hardware with driver abstractions

## Verify Correctness {#Verify}

**\prj_name Targets** are based on Arm simulation models that are validated with the same process as the IP. Specially it allows you to:
 - Algorithm testing with identical logical behaviour of the target device
 - Precisely repeat complex input patterns in CI/CD test environments
 - Analyse software behaviour with event annotations

## Evaluate Performance {#Evaluate}

Software algorithms for Digital Signal Processing (DSP) or Machine Learning (ML) frequently require significant CPU resources and need to be optimized for the target hardware. Comparing performance of such "load heavy" algorithms requires that they can be automatically executed with different configurations parameters but using identical input. 

**\prj_name Services** allows users to test their programs at scale with reproducible input patterns and so validate and optimize application performance which allows you to:
 - Compare speed of different implementations of an algorithm
 - Identify timing issues during system integration
 - Optimize resources (i.e. data buffers) towards application requirements

## Continuous Testing {#CI}

Applying continuous integration work flows for embedded applications can be complicated by the specifics of development environments and the need of executing the program on target hardware. So the development teams are often reluctant to spend initial effort setting up the continuous integration (CI) workflow even though the long-term benefits are undisputed as shown on the Figure below

\image html "effort_comparison.png" "Comparison of test efforts in CI and no CI workflows"

**\prj_name** simplifies the setup and use of CI workflows in embedded projects. 

For unit and integration tests virtual targets offer additional advantages over hardware, including:
 - **Speed** - no overhead for flashing the application on physical hardware. This saves time on small and fast unit tests. 
 - **Scale** - virtual platforms can scale to run many tests in parallel. This makes virtual platforms more cost-effective than a farm of physical hardware. 
 - **Maintenance** – unlike physical hardware, virtual platforms do not overheat, wear out from overuse, break from misuse, or use physical space and resources. 
 - **Upgrades** – virtual platforms can be adapted and re-configured to match corresponding changes to the underlying hardware platform that is under development. These types of changes can be costly or impossible with physical hardware.


