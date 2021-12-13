# Run with MDK-Professional {#run_mdk_pro}

This section explains how Virtual Hardware Targets can be used with [Keil MDK](https://developer.arm.com/tools-and-software/embedded/keil-mdk) tools for developing and debugging your embedded application on a local computer.

\note
  - [**ON ROADMAP**](../../overview/html/index.html#Roadmap): The **\prj_name Targets** for Keil MDK are in development an will become available soon.

## Tools Installation {#mdk_vht_install}

 - Download and install Keil MDK on your Windows PC, if not present yet.
 - [MDK-Professional Edition](https://developer.arm.com/tools-and-software/embedded/keil-mdk/buy) is required for using VHTs. If it is not available, you can [request evaluation license](https://www.keil.com/support/man/docs/license/license_eval.htm).
 - Install the MDK_AddOn_VHT with the VHT models. It is recommended to use Keil MDK installation folder for it (for example `C:/Keil_v5/`), because some example projects use this path by default.
 - Enable Telnet Client on Windows 10. This will allow to observe UART output from the VHT during debug.
   - Open _Start_ > _Settings_.
   - In the search box, type _Turn Windows features on or off_ and click on the suggested item. The _Windows Features_ dialog opens.
   - Select the _Telnet Client_ check box and click _OK_. The installation might take several minutes to
complete.
   .
   ![Enable Windows Telnet Client](images/windows_telnet_enable.png)

## Project Configuration {#mdk_project_config}

 - Open the target project in uVision IDE:
  - either double-click on existing *uvprojx* project file,
  - or [import a .cprj project](https://www.keil.com/support/man/docs/uv4/uv4_ui_import.htm) from uVision menu.
 - Agree to install missing software packs when requested.
   - In some cases, to proceed with the installation you need to accept license agreement displayed in a separate dialog.
 - Return to the project window and accept to reload packs.

**Target configuration**
 - todo: explain how VHT target is selected.

**VHT debug configuration**
 - Open _Options for Target..._ dialog from the toolbar and navigate to the  _Debug_ tab.
 - Verify that the _Models Debugger_ is selected in _Use:_ drop-down menu. For example for Corstone-3300:<br>
   ![Models ARMv8-M Debugger](images/uv4_model_debug.png)
 - Click on the _Settings_ button. This opens corresponding _Models Target Driver Setup_ dialog. Configuration from the VHT Basic example is shown below:
    ![VHT model configuration in VHT Basic example](images/vht_uv4_setup_basic.png)
    - _Command_ line contains the path to the model executable.`$K` is a [key sequence](https://www.keil.com/support/man/docs/uv4/uv4_ut_keysequence.htm) shortening the Keil MDK installation path (for example `C:\Keil_v5\`). Change the value in this field if the VHT is installed in a different location.
    - _Arguments_ field specifies optional [FVP command-line options](https://developer.arm.com/documentation/100966/1116/Getting-Started-with-Fixed-Virtual-Platforms/FVP-command-line-options) to be used with the model execution. In many examples it contains an option for starting a Telnet client for displaying the redirected output during debug session.
    - _Target_ field shall contain `cpu0` when using VHT.
    - _Configuration File_ points to the file with model configuration parameters (passed to the model executable with `-f` option).
    .
  [Fast Models Debug Driver Configuration](https://www.keil.com/support/man/docs/fstmdls/fstmdls_debug_cfg.htm) explains the configuration dialog in details.

## Program Build and Debug {#mdk_program_run}

Project build and debug on VHT can be done in the similar way as any other Keil MDK project:

 - Press _Rebuild_ button in uVision toolbar (or use `F7` hotkey).
 - Start the debug session from uVision toolbar (or with `Ctrl-F5`). The model executable window should pop up ( with `C:\WINDOWS\system32\cmd.exe`) but it will stay empty during the session.
 - A Telnet client will start if configured accordingly in the project. Program output should be expected there.
 - Debug the project as usual with available uVision functionality. Refer to [uVision User's Guide](https://www.keil.com/support/man/docs/uv4/) for details about user interface and debug capabilities.

## Project Export {#mdk_cprj_export}

Universal [.cprj format](https://arm-software.github.io/CMSIS_5/Build/html/cprjFormat_pg.html) is required for building the program in AVH cloud environment. So it is important to keep the MDK project files and the _cprj_ file synchronized. For that after saving modifications in the MDK project go to the uVision menu [_Project_ - _Export_](https://www.keil.com/support/man/docs/uv4/uv4_ui_export.htm) and select _Save project to CPRJ format_.
