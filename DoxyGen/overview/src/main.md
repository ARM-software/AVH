\mainpage Introduction

[comment]:[TOC]

[Arm Virtual Hardware (AVH)](https://www.arm.com/products/development-tools/simulation/virtual-hardware) covers various solutions for software development on Arm-based processors using virtual targets. This includes virtual simulation models, their cloud-native deployments and integrations with development tools.

AVH supports the software development cycle of embedded, IoT, and ML applications and provides essential components for effective integration into Continuous Integration/Continuous Delivery ([CI/CD](https://en.wikipedia.org/wiki/CI/CD)) and [MLOps](https://en.wikipedia.org/wiki/MLOps) development flows.

![Arm Virtual Hardware - Overview](./images/avh_overview.png)

# AVH Models {#avh_models}

AVH simulation models enable execution of software programs on virtual targets. Two different AVH modelling technologies are available:

  <h2>AVH Fixed Virtual Platforms (FVPs)</h2>

  - Precise simulation models of Arm Cortex-M based reference platforms, such as Corstone-315/310/300. Learn more at [Simulation](../../simulation/html/index.html).
  - Available for cloud-native and desktop environments. See [Infrastructure](../../infrastructure/html/index.html) for details.

  <h2>AVH Corellium models</h2>

   - Functionally accurate virtual representations of popular IoT development boards and selected Arm reference platforms:
     - Cortex-A based systems with Linux OS support, such as Raspberry Pi and NXP i.MX.
     - Selected Cortex-M based kits.
   - Software binary-compatible with the hardware targets.
   - Available via [app.avh.arm.com](https://app.avh.arm.com/) cloud platform. Read more in [AVH Users's Guide](https://developer.arm.com/docs/107660).

# AVH Integrations {#avh_integrations}

Arm Virtual Hardware models integrate well in various tools and services for development, debug, testing as well as CI/CD and MLOps flows. AVH is already  supported within many Arm tools, as well as by third-party vendors.

The integration approach depends on the modelling technology:
- AVH FVP models are standalone programs that gets executed in the target environment. See [Infrastructure](../../infrastructure/html/index.html) for more details.
- AVH Corellium models are cloud-native and gets integrated via REST API and SSH connections. See [AVH Users's Guide](https://developer.arm.com/docs/107660)

# AVH Developer Resources {#avh_dev}

Various Resources explain how to integrate Arm Virtual Hardware into workflows common for generic embedded software development, CI testing and MLOps.

Usage examples show typical use cases and range from audio processing, ML algorithm testing, up to IoT applications that interface to Cloud Service providers and Over-the-Air Firware Updates (OTAU).

**This documentation** is dedicated to the **AVH FVPs** and has following sections that can be accessed as document tabs as well:

Section                                                    | Description
:----------------------------------------------------------|:--------------------
[**Overview**](index.html)                                 | Introduces **Arm Virtual Hardware** along with the top-level structure.
[**Simulation**](../../simulation/html/index.html)         | Explains the AVH FVP simulation technology and the virtual interfaces.
[**Infrastructure**](../../infrastructure/html/index.html) | Describes key integrations of AVH FVPs locally and in the cloud.
[**Examples**](../../examples/html/index.html)             | Guides through the examples that demonstrate how to use AVH FVPs.

For more details about AVH Corellium models refer to [AVH Users's Guide](https://developer.arm.com/docs/107660).

# Feedback and Support {#Support}

Arm Virtual Hardware is supported via this [Arm forum](https://community.arm.com/support-forums/f/arm-virtual-hardware-forum). Your feedback will influence our future roadmap and we try to help you promptly with your questions.
