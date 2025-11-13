[![License](https://img.shields.io/github/license/Arm-Software/AVH?label)](https://github.com/Arm-Software/AVH/blob/main/LICENSE)
[![GH-Pages](https://img.shields.io/github/actions/workflow/status/Arm-Software/AVH/gh-pages.yaml?logo=arm&logoColor=0091bd&label=Deploy%20content)](./.github/workflows/gh-pages.yaml)


# AVH FVPs: Developer Resources

This repository explains the use of [Arm Virtual Hardware on Fixed Virtual Platforms (AVH FVP)](https://arm-software.github.io/AVH/main/simulation/html/index.html).

The [documentation](https://arm-software.github.io/AVH/main/overview/html/index.html) describes how to integrate AVH FVPs into typical [CI/CD](https://developer.arm.com/servers-and-cloud-computing/cicd-on-arm) workflows as well as desktop development environments. Additional interface drivers are provided that map to virtual targets and physical hardware along with Python scripts for I/O simulation.


## Examples

The table below lists some of the example projects that demonstrate the usage of [AVH FVPs](https://arm-software.github.io/AVH/main/simulation/html/index.html). Also see [AVH FVP Example Projects](https://arm-software.github.io/AVH/main/examples/html/index.html) in the documentation.

| Examples       | Description            |
|---             |---                     |
| [AVH-Hello](https://github.com/Arm-Examples/AVH-Hello)   | Hello world example for [AVH FVPs](https://arm-software.github.io/AVH/main/simulation/html/index.html). The [GitHub workflow](https://github.com/Arm-Examples/AVH-Hello/blob/main/.github/workflows/hello-ci.yml) supports build and run actions for different [targets](https://github.com/Arm-Examples/AVH-Hello/blob/main/.github/workflows/hello-ci.yml#L22). |
| [AVH_CI_Template](https://github.com/Arm-Examples/AVH_CI_Template)   | Simple example for unit test automation that uses [GitHub Actions](https://github.com/features/actions) on a [GitHub-hosted runner](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners). |
| [AVH-VSI Examples](https://github.com/Arm-Examples/AVH-VSI)   | Demonstrates how to use the [Virtual Streaming Interface (VSI)](https://arm-software.github.io/AVH/main/simulation/html/group__arm__vsi.html) for feeding sensor or video data to an application running on an [AVH FVP Model](https://arm-software.github.io/AVH/main/overview/html/index.html). |
| [AVH-MLOps](https://github.com/ARM-software/AVH-MLOps)   | A set of tools, software components, and examples showcasing MLOps systems with [AVH FVPs](https://arm-software.github.io/AVH/main/simulation/html/index.html). |
| [CMSIS-Core Validation](https://github.com/ARM-software/CMSIS_6/tree/main/CMSIS/CoreValidation)   | Test suite to verify the correct operation of the [CMSIS-Core](https://arm-software.github.io/CMSIS_6/latest/Core/index.html) functionality on various Cortex-M cores by using different toolchains and [AVH FVPs](https://arm-software.github.io/AVH/main/simulation/html/index.html). |
| [CMSIS-RTOS2 Validation](https://github.com/Arm-Software/CMSIS-RTOS2_Validation)   | Test suite for validating [CMSIS-RTOS2](https://arm-software.github.io/CMSIS_6/latest/RTOS2/index.html) implementations on various Cortex-M cores by using different toolchains and [AVH FVPs](https://arm-software.github.io/AVH/main/simulation/html/index.html). |


## Directory Structure

The content of this repository:

| Directory      | Description |
|---             |--- |
| [interface](https://github.com/ARM-software/AVH/tree/main/interface)                 | [Virtual Interface APIs](https://arm-software.github.io/AVH/main/simulation/html/group__arm__cmvp.html) with drivers and Python scripts. |
| [DoxyGen](https://github.com/ARM-software/AVH/tree/main/DoxyGen)                     | Doxygen sources for Arm Virtual Hardware FVP documentation. |
| [Documentation](https://github.com/ARM-software/AVH/tree/main/Documentation)         | Temporary output directory for the [documentation](https://arm-software.github.io/AVH/main/overview/html/index.html). |
| [.github/workflows](https://github.com/ARM-software/AVH/tree/main/.github/workflows) | GitHub action for publishing. |

## Issues

Please feel free to raise an [issue on GitHub](https://github.com/ARM-software/AVH/issues)
to report misbehavior (i.e. bugs) or start discussions about enhancements. This
is your best way to interact directly with the maintenance team and the community.

Copyright (C) 2021-2025, Arm Ltd.
