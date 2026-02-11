# CMSIS Support {#avh_fvp_cmsis}

Arm provides comprehensive CMSIS support for FVP targets in [Open-CMSIS-Pack format](https://www.open-cmsis-pack.org/), including device definitions, startup code, board support packages, and examples.

The following table lists available FVP models with their corresponding CMSIS-Packs and device names:

<table class="doxtable" style="width:115%">
<tr>
<th style="width:27%">Arm FVP Model Name   </th><th style="width:25%">CMSIS Packs with DFP/BSP<sup> (1)</sup>  </th><th style="width:17%">Device name</th><th>Description</th></tr>
<tr>
<td>FVP_Corstone_SSE-320</td><td>[ARM.SSE_320_BSP](https://www.keil.arm.com/packs/sse_320_bsp-arm)</td><td>[`SSE-320-FVP`](https://www.keil.arm.com/devices/arm-sse-320-fvp)</td><td>Corstone-320 subsystem</td></tr>
<tr>
<td>FVP_Corstone_SSE-315</td><td>[ARM.SSE_315_BSP](https://www.keil.arm.com/packs/sse_315_bsp-arm)</td><td>[`SSE-315-FVP`](https://www.keil.arm.com/devices/arm-sse-315-fvp)</td><td>Corstone-315 subsystem</td></tr>
<tr>
<td>FVP_Corstone_SSE-310<br/>FVP_Corstone_SSE-310_Ethos-U65</td><td>[ARM.V2M_MPS3_SSE_310_BSP](https://www.keil.arm.com/packs/v2m_mps3_sse_310_bsp-arm)</td><td>[`SSE-310-MPS3_FVP`](https://www.keil.arm.com/devices/arm-sse-310-mps3-fvp)</td><td>Corstone-310 subsystem</td></tr>
<tr>
<td>FVP_Corstone_SSE-300<br/>FVP_Corstone_SSE-300_Ethos-U55<br/>FVP_Corstone_SSE-300_Ethos-U65</td><td>[ARM.V2M_MPS3_SSE_300_BSP](https://www.keil.arm.com/packs/v2m_mps3_sse_300_bsp-arm)</td><td>[`SSE-300-MPS3`](https://www.keil.arm.com/devices/arm-sse-300-mps3)</td><td>Corstone-300 subsystem</td></tr>
<tr>
<td>FVP_MPS2_Cortex-M85</td><td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM85`](https://www.keil.arm.com/devices/arm-armcm85)</td><td>Generic Cortex-M85 device</td></tr>
<tr>
<td>FVP_MPS2_Cortex-M55   </td><td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM55`](https://www.keil.arm.com/devices/arm-armcm55)</td><td>Generic Cortex-M55 device</td></tr>
<tr>
<td>FVP_MPS2_Cortex-M52   </td><td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM52`](https://www.keil.arm.com/devices/arm-armcm52)</td><td>Generic Cortex-M52 device</td></tr>
<tr>
<td>FVP_MPS2_Cortex-M35P   </td><td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM35P`](https://www.keil.arm.com/devices/arm-armcm35p)</td><td>Generic Cortex-M35P device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M33   </td><td>[Keil.V2M-MPS2_IOTKit_BSP](https://www.keil.arm.com/packs/v2m-mps2_iotkit_bsp-keil/)</td><td>[`IOTKit_CM33_VHT`](https://www.keil.arm.com/devices/arm-iotkit-cm33-vht)<br/>[`IOTKit_CM33_FP_VHT`](https://www.keil.arm.com/devices/arm-iotkit-cm33-vht)</td><td>Cortex-M33 IoT Kit subsystem</td></tr>
<tr>                                       <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM33`](https://www.keil.arm.com/devices/arm-armcm33)</td><td>Generic Cortex-M33 device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M23   </td><td>[Keil.V2M-MPS2_IOTKit_BSP](https://www.keil.arm.com/packs/v2m-mps2_iotkit_bsp-keil/)</td><td>[`IOTKit_CM23_VHT`](https://www.keil.arm.com/devices/arm-iotkit-cm23-vht)</td><td>Cortex-M23 IoT Kit subsystem</td></tr>
<tr>                                       <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM23`](https://www.keil.arm.com/devices/arm-armcm23)</td><td>Generic Cortex-M23 device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M7   </td><td>[Keil.V2M-MPS2_CMx_BSP](https://www.keil.arm.com/packs/v2m-mps2_cmx_bsp-keil)</td><td>[`CMSDK_CM7_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm7-vht)<br/>[`CMSDK_CM7_SP_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm7-sp-vht)<br/>[`CMSDK_CM7_DP_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm7-dp-vht)</td><td>Cortex-M7 System Design Kit Device<br/>SP variant -  Single Precision FPU support<br/>DP variant - Dual Precision FPU support</td></tr>
<tr>                                      <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)</td><td>[`ARMCM7`](https://www.keil.arm.com/devices/arm-armcm7)</td><td>Generic Cortex-M7 device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M4   </td><td>[Keil.V2M-MPS2_CMx_BSP](https://www.keil.arm.com/packs/v2m-mps2_cmx_bsp-keil)</td><td>[`CMSDK_CM4_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm4-vht)<br/>[`CMSDK_CM4_FP_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm4-fp-vht)</td><td>Cortex-M3 System Design Kit Device<br/>FP variant - with Floating Point Unit (FPU) support</td></tr>
<tr>                                      <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)              </td><td>[`ARMCM4`](https://www.keil.arm.com/devices/arm-armcm4)</td><td>Generic Cortex-M4 device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M3   </td><td>[Keil.V2M-MPS2_CMx_BSP](https://www.keil.arm.com/packs/v2m-mps2_cmx_bsp-keil)</td><td>[`CMSDK_CM3_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm3-vht)</td><td>Cortex-M3 System Design Kit Device</td></tr>
<tr>                                      <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)              </td><td>[`ARMCM3`](https://www.keil.arm.com/devices/arm-armcm3)</td><td>Generic Cortex-M3 device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M0plus</td><td>[Keil.V2M-MPS2_CMx_BSP](https://www.keil.arm.com/packs/v2m-mps2_cmx_bsp-keil)</td><td>[`CMSDK_CM0plus_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm0plus-vht)</td><td>Cortex-M0+ System Design Kit Device</td></tr>
<tr>                                       <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)       </td><td>[`ARMCM0plus`](https://www.keil.arm.com/devices/arm-armcm0plus)</td><td>Generic Cortex-M0+ device</td></tr>
<tr>
<td rowspan="2">FVP_MPS2_Cortex-M0 </td><td>[Keil.V2M-MPS2_CMx_BSP](https://www.keil.arm.com/packs/v2m-mps2_cmx_bsp-keil)</td><td>[`CMSDK_CM0_VHT`](https://www.keil.arm.com/devices/arm-cmsdk-cm0-vht)</td><td>Cortex-M0 System Design Kit Device</td></tr>
<tr>                                    <td>[ARM.Cortex_DFP](https://www.keil.arm.com/packs/cortex_dfp-arm)              </td><td>[`ARMCM0`](https://www.keil.arm.com/devices/arm-armcm0)      </td><td>Generic Cortex-M0 device</td></tr>

</table>

**Note:** <sup>(1)</sup> BSP packs (suffixed with "_BSP") include both board support and device definitions, eliminating the need for a separate Device Family Pack (DFP).

## Software Layers

The AVH_FVP pack provides board support layers for Corstone FVP platforms in the `board/` folder. Each board layer includes hardware-specific configurations, drivers, and setup for running applications on FVP simulation models.

| Folder                 | Description |
|:-----------------------|:------------|
| `./board/Corstone-300` | Board layer for Corstone-300 FVP with optional Ethos-U55/U65 |
| `./board/Corstone-310` | Board layer for Corstone-310 FVP with optional Ethos-U55/U65 |
| `./board/Corstone-315` | Board layer for Corstone-315 FVP with optional Ethos-U65 |
| `./board/Corstone-320` | Board layer for Corstone-320 FVP with optional Ethos-U85 |

Each folder contains a **README** with implementation details and multiple **CSolution layer files** (`*.clayer.yml`) that configure different hardware variants. The postfix in the `*.clayer.yml` filename determines the Ethos-U NPU configuration:

| Layer File | NPU Configuration | Description |
|:-----------|:------------------|:------------|
| `Board.clayer.yml` | None | Cortex-M system only, no Ethos-U NPU |
| `Board-U55.clayer.yml` | Ethos-U55 | Cortex-M system + Ethos-U55 NPU (256 MACs) |
| `Board-U65.clayer.yml` | Ethos-U65 | Cortex-M system + Ethos-U65 NPU |
| `Board-U85.clayer.yml` | Ethos-U85 | Cortex-M system + Ethos-U85 NPU |

Refer to [CMSIS-Toolbox - Software Layers](https://open-cmsis-pack.github.io/cmsis-toolbox/build-overview/#software-layers) for more information on using layers in projects.
