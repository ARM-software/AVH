\mainpage Introduction

Arm **\prj_name** (VHT) provide simulation models, software tooling, and infrastructure that can be integrated into [**CI/CD**](https://en.wikipedia.org/wiki/CI/CD) and [**MLOps**](https://en.wikipedia.org/wiki/MLOps) development flows. Arm VHT supports the software development cycle of embedded, IoT, and ML applications and provides essential components for effective test and validation environments. Arm VHT is flexible and can run any [**RTOS**](https://en.wikipedia.org/wiki/Real-time_operating_system) that is designed for Cortex-M or bare metal code that interacts with the processor. Arm VHT offers a comprehensive tool integration along with resources for software developers and can therefore run complex applications and software integration tests. A potential workload could be a [**sensor-fusion**](https://en.wikipedia.org/wiki/Sensor_fusion) Machine Learning (ML) application that connects to the Internet via an IoT operating system.


Arm VHT consists of the following components:

  - **Arm VHT Systems** are precise [**simulation models**](https://en.wikipedia.org/wiki/Simulation) of Cortex-M device sub-systems and are designed for complex software verification and testing. It allows [**simulation-based test automation**](https://en.wikipedia.org/wiki/Test_automation) of various software workloads, including unit tests, integration tests, and fault injection. 

  - **Arm VHT Services** provide a cloud-native infra-structure for software test and validation. These Arm VHT services can be integrated into various **CI/CD** and **MLOps** environments that range from GitHub to on-premise IT infrastructure. The Arm VHT services will be available via the AWS Marketplace (and later also via other Cloud Service providers).
 
  - **Arm VHT Developer Resources** gives you access to interface drivers that map to virtual targets and physical hardware along with Python scripts for I/O simulation. The documentation explains how to integrate Arm VHT into typical **CI/CD** environments. Usage examples show typical usage cases and range form audio processing, ML algorithm testing, up to IoT applications that interface to Cloud Service providers.
  
  - **Software Development Environments** with Arm VHT integration are also available. Arm VHT Systems are integral part of the Keil MDK Professional Edition that is a comprehensive software tool suite for creating Cortex-M-based applications and related validation and test processes. In future, the next-generation Keil Studio will also integrate the VHT Systems and Services.

\image html "vht_overview.png" "Arm \prj_name - Components"


# Documentation {#overview_doc}

This documentation describes the Arm **\prj_name** and the examples that show integration into CI/CD and MLOps development flows. The table below explains the documentation structure.


Section                                                    | Description
:----------------------------------------------------------|:--------------------
[**Overview**](index.html)                                 | Introduces Arm **\prj_name** along with the top-level structure.
[**Simulation**](../../simulation/html/index.html)         | Explains the Arm VHT system simulation technology and the virtual interfaces.
[**Infrastructure**](../../infrastructure/html/index.html) | Describes how to setup development work flows with Arm VHT.
[**Examples**](../../examples/html/index.html)             | Guides through the examples demonstrating how to use Arm VHT.
</table>

# Motivation {#motivation}

\todo facts missing
The simulation-based Arm VHT framework integrates with the cloud-native CI/CD and MLOps workflows as explained in the subsections below.

## Cloud-based Continuous Testing {#overview_motiv_test}

Applying continuous integration work flow for embedded applications can be complicated by the specifics of development environments and the need of executing the program on target hardware. So the development teams are often reluctant to spend initial effort setting up the continuous integration (CI) workflow even though the long-term benefits are undisputed as shown on the Figure below

\image html "effort_comparison.png" "Comparison of test efforts in CI and no CI workflows"

VHT simplifies the setup and use of CI workflows in embedded projects. 

For unit and integration tests virtual targets offer additional advantages over hardware, including:
 - \b Speed - no overhead for flashing the application on physical hardware. This saves time on small and fast unit tests. 
 - \b Scale - virtual platforms can scale to run many tests in parallel. This makes virtual platforms more cost-effective than a farm of physical hardware. 
 - \b Maintenance – unlike physical hardware, virtual platforms do not overheat, wear out from overuse, break from misuse, or use physical space and resources. 
 - \b Upgrades – virtual platforms can be adapted and re-configured to match corresponding changes to the underlying hardware platform that is under development. These types of changes can be costly or impossible with physical hardware.

## Performance comparisons {#overview_motiv_perf}

Software algorithms for such operations as digital signal processing (DSP) or machine learning (ML) frequently require significant CPU resources and need to be optimized for the target hardware. Comparing performance of such "load heavy" algorithms requires that they can be automatically executed with different configurations parameters but using identical input. 

Arm VHT Services allows users to test their programs at scale with reproducible input patterns and so validate and optimize application performance.
