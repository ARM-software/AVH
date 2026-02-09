# Use with Keil Studio {#run_mdk_vscode}

This section explains how Arm FVPs can be used with [Keil Studio](https://www.keil.arm.com) for developing and
debugging embedded applications on a local computer.

## Tools Installation {#mdk_vscode_install}

- Download and install [Visual Studio Code](https://code.visualstudio.com/) if not installed yet.
- Install [Arm Keil Studio Pack](https://developer.arm.com/documentation/109350/latest/Installation/Keil-Studio-installation)
  in Visual Studio Code.
- Ensure that a user-based license is
  [activated](https://developer.arm.com/documentation/108029/latest/Activate-your-license-to-use-Arm-tools). Either an
  [MDK-Community edition](https://www.keil.arm.com/mdk-community) (evaluation and non-commercial use) or an
  [MDK-Professional](https://www.keil.arm.com/keil-mdk/#mdk-v6-editions) (commercial use) is required for running Arm
  FVP models.

## Target selection {#mdk_vscode_fvp_targets}

Keil Studio natively supports the [Open-CMSIS-Pack format](https://www.open-cmsis-pack.org/) for device support and
management of software components. See [CMSIS-based projects for AVH FVPs](../../simulation/html/avh_fvp_cmsis.html)
for the list of the device family packs and BSP packs required for use with Arm FVPs.

- When opening an existing
  [csolution project](https://github.com/Open-CMSIS-Pack/cmsis-toolbox/blob/main/docs/YML-Input-Format.md) in Keil
  Studio, all necessary packs for the target will be automatically installed.
- When creating a new solution, you need to select a target device that corresponds to the Arm FVP model according to
  the table in [CMSIS-based projects for AVH FVPs](../../simulation/html/avh_fvp_cmsis.html).

You can view the device name defined for the target in the project `csolution.yml` file, or by clicking the
*Manage solution settings* button in the **CMSIS** view, as shown on the image below.
[Manage solutions](https://mdk-packs.github.io/vscode-cmsis-solution-docs/manage_settings.html) explains the concept in
details.

![CMSIS Manage solution settings](images/mdk_vscode_mng_solution.png)

## vcpkg configuration {#mdk_vscode_vcpkg}

Keil Studio relies on the
[Arm Tools Environment Manager](https://marketplace.visualstudio.com/items?itemName=Arm.environment-manager) extension
to setup the development environment from Arm Tools Artifactory using Microsoft vcpkg. The vcpkg manifest file
`vcpkg_configuration.json` must contain the requirement for Arm FVPs models, in the same way as explained in
\ref avh_fvp_vcpkg. For example:

```json
{
  "registries": [
    {
      "name": "arm"
      "kind": "artifact",
      "location": "https://artifacts.tools.arm.com/vcpkg-registry"
    }
  ],
  "requires": {
    "arm:models/arm/avh-fvp": "^11.30.29"
  }
}
```

> **Note**
> In Keil Studio other tools are usually also present for build and debug tasks such as CMSIS-Toolbox, a compiler
> toolchain, and others.

## Build {#mdk_vscode_build}

Follow the instructions provided in the [Build](https://mdk-packs.github.io/vscode-cmsis-solution-docs/build_run.html)
chapter in the Keil Studio User's Guide.

## Run {#mdk_vscode_program_run}

In Keil Studio, you can run a program on the target without using the debugger. See
[Arm FVPs](https://mdk-packs.github.io/vscode-cmsis-solution-docs/debug.html#arm-fvps) for steps how to
configure this.
