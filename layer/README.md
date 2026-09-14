# Board Support for Arm Virtual Hardware FVPs

This folder contains board support layers for Arm Corstone FVP (Fixed Virtual
Platform) targets. Each board layer provides the hardware-specific
configuration, drivers, and initialization required to run applications on an
FVP.

## Layer Types

Two alternative layer sets are provided:

| Layer set           | Description                                                                        |
|:--------------------|:-----------------------------------------------------------------------------------|
| [Base](base/)       | Standard board support with USART, VIO, STDIO, and optional Ethos-U configuration. |
| [vStream](vStream/) | Base layer + with CMSIS-Driver vStream interfaces using the FVP VSI peripherals.   |

Select one board layer from either `base` or `vStream`.

## Available Board Layers

| Platform     | Base layer                 | vStream layer                    | NPU variants         |
|:-------------|:---------------------------|:---------------------------------|:---------------------|
| Corstone-300 | [Base](base/Corstone-300/) | [vStream](vStream/Corstone-300/) | Ethos-U55, Ethos-U65 |
| Corstone-310 | [Base](base/Corstone-310/) | [vStream](vStream/Corstone-310/) | Ethos-U55, Ethos-U65 |
| Corstone-315 | [Base](base/Corstone-315/) | [vStream](vStream/Corstone-315/) | Ethos-U65            |
| Corstone-320 | [Base](base/Corstone-320/) | [vStream](vStream/Corstone-320/) | Ethos-U85            |

Each board folder contains a **README** with implementation details and multiple **CSolution layer files** (`*.clayer.yml`) that configure different hardware variants. The postfix in the `*.clayer.yml` filename determines the Ethos-U NPU configuration:

| Layer File             | NPU Configuration | Description                                |
|:-----------------------|:------------------|:-------------------------------------------|
| `Board.clayer.yml`     | None              | Cortex-M system only, no Ethos-U NPU       |
| `Board-U55.clayer.yml` | Ethos-U55         | Cortex-M system + Ethos-U55 NPU (256 MACs) |
| `Board-U65.clayer.yml` | Ethos-U65         | Cortex-M system + Ethos-U65 NPU            |
| `Board-U85.clayer.yml` | Ethos-U85         | Cortex-M system + Ethos-U85 NPU            |

The layer files define the hardware abstraction, including CMSIS components,
drivers, and device initialization required for the selected configuration.

Refer to [CMSIS-Toolbox - CSolution Project Structure - Software Layers](https://open-cmsis-pack.github.io/cmsis-toolbox/build-overview/#software-layers) for more information.
