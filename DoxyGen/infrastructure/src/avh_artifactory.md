# AVH FVPs in Arm Tools Artifactory {#avh_fvp_artifactory}

The AVH FVP models can be universally obtained from [Arm Tools Artifactory](https://www.keil.arm.com/artifacts/) that also contains other useful develepment tools, such as Arm Compiler, GCC toolchain, CMSIS-Toolbox.

You can either download the AVH FVPs \ref avh_fvp_download "directly" or rely on the environment setup via the \ref avh_fvp_vcpkg "vcpkg configuration" in the project. Additionally a user-based license needs to be \ref avh_fvp_lic_act "activated".

Note that AVH FVPs integrations in \ref avh_gh_actions "GitHub Actions" or \ref avh_desktop "desktop IDEs" may provide own built-in mechanisms for environment setup and vcpkg configuration support. Refer to corresponding documentation sections for details.

## Direct download {#avh_fvp_download}

You can download individual tool artifacts from Arm Tools Artifactory directly using URLs. The AVH FVPs can be found at [https://artifacts.tools.arm.com/avh/](https://artifacts.tools.arm.com/avh/), are organized by release version and packaged for supported host operating systems such as Linux on Arm (AArch64), Windows on x86, and Linux on x86.

For example to download AVH FVP v11.27.31 for use on Linux with Arm-based CPUs, run the following commands:

```
wget https://artifacts.tools.arm.com/avh/11.27.31/avh-linux-aarch64_11.27_31_Linux64_armv8l.tgz
tar zxvf avh-linux-aarch64_11.27_31_Linux64_armv8l.tgz
```

In this example, the avh-fvp artifact is downloaded and the extracted models are available locally in `./avh-linux-aarch64/bin/models/` directory.

## Download with vcpkg {#avh_fvp_vcpkg}

vcpkg is a package management utility that can be used to easily configure and recreate your development environment.

Learning path article [Install tools on the command line using vcpkg
](https://learn.arm.com/learning-paths/microcontrollers/vcpkg-tool-installation/) provides detailed information on how to install vcpkg on your machine and use it to retrieve specific tool artifacts.

The package management via vcpkg is natively integrated into Keil Studio for VS Code and is configured in many Arm references examples. It is also simplified for use in GitHub CI/CD workflows as explained in \ref avh_gh_actions.

For AVH FVPs the `vcpkg_configuration.json` file shall contain `"arm:models/arm/avh-fvp"` entry to ensure the download of the models. For example:

```
{
  "registries": [
    {
      "kind": "artifact",
      "location": "https://artifacts.tools.arm.com/vcpkg-registry"
      "name": "arm"
    }
  ],
  "requires": {
    "arm:models/arm/avh-fvp": "^11.27.31"
  }
}
```

## License management {#avh_fvp_lic_act}

AVH FVPs as well as other Arm Tools provided in the Arm Tools Artifactory require an active [Arm user-based license (UBL)](https://developer.arm.com/Tools%20and%20Software/User-based%20Licensing) for their operation.

Arm tools artifacts include the license management utility armlm that shall be used to [activate and deactivate](https://developer.arm.com/documentation/102516/1-3/Activate-and-deactivate-your-product-license) a UBL license in your environment.

For evaluation and non-commercial use you can activate an [MDK-Community Edition](https://www.keil.arm.com/keil-mdk/#mdk-v6-editions) that also enables AVH FVPs. Use the following command for that:

```
armlm activate -product KEMDK-COM0 -server https://mdk-preview.keil.arm.com
```

For commercial use you need to obtain a license for [MDK-Professional edition](https://www.keil.arm.com/keil-mdk/#mdk-v6-editions) or [Arm Success Kit](https://www.arm.com/products/development-tools/success-kits).

> **Note**
> Your use of an Arm tool is subject to your acceptance of the End User License Agreement for Arm Software Development Tools, located within the 'license_terms' folder of the downloaded archive. By installing and using the Arm tool, you agree to be bound by the terms and conditions of the end user license agreement.
