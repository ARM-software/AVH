# Release History {#History}

<table>
<tr>
<th>Version</th>
<th>Changes</th>
</tr>
<tr>
<td>2.1.0 (Oct 4, 2024)</td>
<td>
 - Added AVH FVP models:
   - FVP_Corstone_SSE-320
 - Updated the AVH FVP artifacts to version 11.27.31.
</td>
</tr>
<tr>
<td>2.0.0 (June 5, 2024)</td>
<td>
 - Removed beta status.
 - VIO/VSI python script path is moved into model configuration. See [Using AVH FVPs](../../simulation/html/using.html).
 - Added [Arm Tools Artifactory](../../infrastructure/html/avh_fvp_artifactory.html) support.
 - Added [Arm GitHub Actions](../../infrastructure/html/avh_gh_actions.html) support.
 - Added [Arm Keil Studio for VS Code](../../infrastructure/html/run_mdk_vscode.html) support.
 - Added AVH FVP models:
   - FVP_Corstone_SSE-315
   - FVP_MPS2_Cortex-M85
   - FVP_MPS2_Cortex-M55
   - FVP_MPS2_Cortex-M52
   - FVP_MPS2_Cortex-M35P
 - Reworked documentation
 - AWS AMI and custom GitHub Runner support are kept as [experimental](../../infrastructure/html/avh_beta.html).
</td>
</tr>
<tr>
<td>1.3.1-beta (Jan 26, 2023)</td>
<td>
 - License validity period for installed Arm tools is extended.
 - EULA for AVH AMI is updated on AWS marketplace.
</td>
</tr>
<tr>
<td>1.3.0-beta (Sept 22, 2022)</td>
<td>
 - Arm Corstone SSE-300 model is supported with [Keil Studio Cloud](https://www.keil.arm.com/boards/arm-v2m-mps3-sse-300-fvp-610bb98/).
 - Provided [eventlist utility](https://github.com/ARM-software/CMSIS-View/tree/main/tools/eventlist) to process Event Recorder logs obtained with Arm FVP targets.
 - Added new FVP model - VHT_Corstone_SSE-310_Ethos-U65 to the AMI, see [Using Arm Fixed Virtual Platforms](../../simulation/html/using.html).
 - Added installation of [CMSIS-Toolbox v1.0.0](https://github.com/Open-CMSIS-Pack/CMSIS-Toolbox) to the AMI, that also includes CMSIS-Build for command-line project builds.
 - Updated [examples](../../examples/html/index.html) to use dynamic credentials (IAM Role) in the GitHub CI workflow, removing the need for storing AWS credentials in GitHub Secrets.
 - Removed preinstalled Bootloader and OpenSuSE software for Corstone-1000.
 - Removed preinstalled CMSIS Packs.
</td>
</tr>
<tr>
<td>1.2.3-beta (July 9, 2022)</td>
<td>
 - Enabled timing annotations in FVPs by default ([FASTSIM_DISABLE_TA](https://developer.arm.com/documentation/100965/1117/Timing-Annotation/Enabling-and-disabling-timing-annotation) is set to 0).<br/>If disabled (FASTSIM_DISABLE_TA set to 1), VSI streams data too quickly and prevents normal execution of [ATS-Keyword Example] (https://github.com/ARM-software/open-iot-sdk/tree/main/examples/ats-keyword).
</td>
</tr>
<tr>
<td>1.2.2-beta (May 10, 2022)</td>
<td>
 - New versioning scheme to match the AMI version (see [AMI Inventory](../../infrastructure/html/ami_inventory.html)).
 - [CMSIS-RTOS2 Validation](https://github.com/ARM-software/CMSIS-RTOS2_Validation): Advanced test suite for validating CMSIS-RTOS2 implementations on supported Cortex-M cores runs using AVH.
 - Corstone-310 model fixes: NPU access fix as well as a parameter for the flash region size allowing it to be a maximum of 64MB.
</td>
</tr>
<tr>
<td>0.3-beta (Apr 2022)</td>
<td>Added features:
 - [Corstone-310 and Corstone-1000](../../simulation/html/using.html): added new simulation models.
 - [Integration with Jenkins](../../infrastructure/html/run_ami_jenkins.html): example of AVH AMI usage in Jenkins CI pipelines.
 - [Event Recorder Semihosting Support](https://www.keil.com/pack/doc/compiler/EventRecorder/html/er_use.html#er_semihosting): allows to generate Event Recorder logs in AVH AMI environment.
 - [AWS MQTT Example](../../examples/html/aws_mqtt.html): IoT application with MQTT connectivity to AWS cloud service.
 - [ATS-Keyword Example](https://github.com/ARM-software/open-iot-sdk/tree/main/examples/ats-keyword): keyword detection application based on [Arm Total Solutions for IoT](https://github.com/ARM-software/ATS-Keyword/).
</td>
</tr>
<tr>
<td>0.2-beta (Feb 2022)</td>
<td>Added features:
 - [Extended Target support](../../simulation/html/using.html): additional Cortex-M processors are supported: Cortex-M0/M0+/M3/M4/M7/M23/M33.
 - [Support in MDK-Professional](../../infrastructure/html/run_mdk_pro.html): enables desktop development in classic tooling.
 - [VIO Interface](../../simulation/html/group__arm__vio.html): simple interface to control I/O such as switches and LEDs via Python scripts.
 - [VSocket Interface](../../simulation/html/group__arm__vsocket.html): BSD socket interface that connects the application under test to networks, including public Internet.
 - [Get-Started example](../../examples/html/GetStarted.html): added simple example demonstrating how to setup a Continuous Integration (CI) workflow using Arm Virtual Hardware.
</td>
</tr>
<tr>
<td>0.1-beta (Nov 2021)</td>
<td>Initial release</td>
</tr>
</table>