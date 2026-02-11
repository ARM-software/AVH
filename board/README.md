# Board Support for Arm Virtual Hardware FVPs

This folder contains board support layers for various Arm Corstone FVP (Fixed Virtual Platform) targets. Each board layer provides hardware-specific configurations, drivers, and setup for running applications on FVP simulation models.

## Available Board Layers

The following Corstone FVP platforms are supported with pre-configured board layers:

| Board Layer | Description |
|:------------|:------------|
| [Corstone-300](Corstone-300/) | Board layer for Corstone-300 FVP with optional Ethos-U55/U65 |
| [Corstone-310](Corstone-310/) | Board layer for Corstone-310 FVP with optional Ethos-U55/U65 |
| [Corstone-315](Corstone-315/) | Board layer for Corstone-315 FVP with optional Ethos-U65 |
| [Corstone-320](Corstone-320/) | Board layer for Corstone-320 FVP with optional Ethos-U85 |

Each board folder contains a **README** with implementation details and multiple **CSolution layer files** (`*.clayer.yml`) that configure different hardware variants. The postfix in the `*.clayer.yml` filename determines the Ethos-U NPU configuration:

| Layer File | NPU Configuration | Description |
|:-----------|:------------------|:------------|
| `Board.clayer.yml` | None | Cortex-M system only, no Ethos-U NPU |
| `Board-U55.clayer.yml` | Ethos-U55 | Cortex-M system + Ethos-U55 NPU (256 MACs) |
| `Board-U65.clayer.yml` | Ethos-U65 | Cortex-M system + Ethos-U65 NPU |
| `Board-U85.clayer.yml` | Ethos-U85 | Cortex-M system + Ethos-U85 NPU |

The layer files define the hardware abstraction, including CMSIS components, drivers, and device initialization required for the specific configuration.

Refer to [CMSIS-Toolbox - CSolution Project Structure - Software Layers](https://open-cmsis-pack.github.io/cmsis-toolbox/build-overview/#software-layers) for more information.