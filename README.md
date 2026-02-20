[![License](https://img.shields.io/github/license/ARM-software/AVH?label)](https://github.com/ARM-software/AVH/blob/main/LICENSE)
[![Build pack](https://img.shields.io/github/actions/workflow/status/ARM-software/AVH/pack.yml?logo=arm&logoColor=0091bd&label=Build%20pack)](./.github/workflows/pack.yml)
[![Publish documentation](https://img.shields.io/github/actions/workflow/status/ARM-software/AVH/gh-pages.yml?logo=arm&logoColor=0091bd&label=Publish%20documentation)](./.github/workflows/gh-pages.yml)
[![Build_Run_FVP_Audio](https://img.shields.io/github/actions/workflow/status/ARM-software/AVH/Build_Run_FVP_Audio.yml?logo=arm&logoColor=0091bd&label=Build_Run_FVP_Audio)](./.github/workflows/Build_Run_FVP_Audio.yml)
[![Build_Run_FVP_Hello](https://img.shields.io/github/actions/workflow/status/ARM-software/AVH/Build_Run_FVP_Hello.yml?logo=arm&logoColor=0091bd&label=Build_Run_FVP_Hello)](./.github/workflows/Build_Run_FVP_Hello.yml)
[![Build_Run_FVP_Video](https://img.shields.io/github/actions/workflow/status/ARM-software/AVH/Build_Run_FVP_Video.yml?logo=arm&logoColor=0091bd&label=Build_Run_FVP_Video)](./.github/workflows/Build_Run_FVP_Video.yml)

# Arm Virtual Hardware FVPs: Developer Resources

The repository contains developer resources, examples, and reference implementations for [Arm Fixed Virtual Platforms (FVP)](https://www.arm.com/products/development-tools/simulation/fixed-virtual-platforms) with **Virtual Interfaces**.

FVP simulation models of [Arm Cortex-M reference platforms](https://arm-software.github.io/AVH/main/simulation/html/index.html) run directly on your host system (Windows or Linux), providing accurate virtual hardware targets for firmware validation. FVP simulation models are included in [Keil MDK](https://www.keil.arm.com/) and integrate seamlessly with Keil Studio, command-line environments, and [CI/CD workflows](https://github.com/Arm-Examples/.github/blob/main/profile/CICD.md).

## Related

- The content of this repository is available as `ARM::AVH_FVP` Pack on [keil.arm.com/packs](https://www.keil.arm.com/packs)
- [Keil Studio](https://www.keil.arm.com/)
- [AVH FVP Documentation](https://arm-software.github.io/AVH/main/overview/html/index.html)
- More [Arm-Examples that use FVP simulation](https://github.com/search?q=topic%3Afvp+org%3AArm-Examples+fork%3Atrue&type=repositories)

## Files and Directories

This is a list of the relevant files and directories.

Directory                       | Description
:-------------------------------|:------------
[overview](./Overview)          | Overview of AVH_FVP content.
[example](./example)            | [Example projects](https://arm-software.github.io/AVH/main/examples/html/index.html) that show usage of FVP simulation models.
[board](./board)                | Board support layers for various Arm Corstone FVP (Fixed Virtual Platform) targets.
[interface](./interface)        | [Virtual Interface APIs](https://arm-software.github.io/AVH/main/simulation/html/group__arm__cmvp.html) with drivers and Python scripts.
[DoxyGen](./DoxyGen)            | Doxygen sources for documentation.
[.github/workflows](./.github/workflows) | GitHub action for publishing and validation.

## Issues

Please feel free to raise an [issue on GitHub](https://github.com/ARM-software/AVH/issues)
to report misbehavior (i.e. bugs) or start discussions about enhancements. This
is your best way to interact directly with the maintenance team and the community.

Copyright (C) 2021-2026, Arm Ltd.
