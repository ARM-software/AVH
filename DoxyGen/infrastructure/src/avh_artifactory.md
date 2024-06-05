# AVH FVPs in Arm Tools Artifactory {#avh_fvp_artifactory}

The AVH FVP models can be universally obtained from [Arm Tools Artifactory](https://www.keil.arm.com/artifacts/) that also contains other useful develepment tools, such as Arm Compiler, GCC toolchain, CMSIS-Toolbox.

You can either download the AVH FVPs directly or rely on the environment setup via the vcpkg configuration in the project. Additionally a user-based license needs to be activated.

Note that AVH FVPs integrations in \ref avh_gh_actions "GitHub Actions" or \ref avh_desktop "desktop IDEs" may provide own built-in mechanisms for environment setup and vcpkg configuration support. Refer to corresponding documentation sections for details.

## Direct Download {#avh_fvp_download}

You can download individual tool artifacts from Arm Tools Artifactory directly using URLs. The AVH FVPs can be found at [https://artifacts.tools.arm.com/avh/](https://artifacts.tools.arm.com/avh/), are organized by release version and packaged for supported host operating systems.

For example to download AVH FVP v11.24.24 for use on Linux with Arm-based CPUs, run the following commands:

```
wget https://artifacts.tools.arm.com/avh/11.24.24/avh-linux-aarch64_11.24_24_Linux64_armv8l.tgz
tar zxvf avh-linux-aarch64_11.24_24_Linux64_armv8l.tgz
```

In this example, the avh-fvp artifact is downloaded and the extracted models are available locally in `./avh-linux-aarch64/bin/models/` directory.

## Download with vcpkg {#avh_fvp_vcpkg}

vcpkg is a package management utility that can be used to easily configure and recreate your development environment.

Learning path article [Install tools on the command line using vcpkg
](https://learn.arm.com/learning-paths/microcontrollers/vcpkg-tool-installation/) provides detailed information on how to install vcpkg on your machine and use it to retrieve specific tool artifacts.

The package management via vcpkg is natively integrated into Keil Studio for VsCode and is configured in many Arm references examples. It is also simplified for use in GitHub CI/CD workflows as explained in \ref avh_gh_actions.

For AVH FVPs the vcpkg_configuration.json file shall contain `"arm:models/arm/avh-fvp"` entry to ensure the download of the models. For example:

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
    "arm:models/arm/avh-fvp": "^11.24.24"
  }
}
```

## License management {#avh_fvp_lic_act}

AVH FVPs as well as other Arm Tools obtained from the Arm Tools Artifactory require an active Arm user-based license for their operation.

Your use of an Arm tool is subject to your acceptance of the End User License Agreement for Arm Software Development Tools, located within the 'license_terms' folder of the downloaded archive. By installing and using the Arm tool, you agree to be bound by the terms and conditions of the end user license agreement.
