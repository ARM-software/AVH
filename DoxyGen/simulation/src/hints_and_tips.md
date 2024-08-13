# Useful Hints and Tips {#hints}

Below are some useful tips for using FVP models in common AVH scenarios:

 - \ref console
 - \ref ci_frameworks
 - \ref timing
 - \ref stop

## Terminal output and logging {#console}

Application can use following options for printing information to a console:
 - \ref uart
 - \ref semihosting

### UART I/O {#uart}

The application firmware can use UART channels available in the FVP model to print out information, with data being forwarded to a Telnet terminal on the PC via a local TCP/IP connection.

This approach is especially beneficial for full-stack applications that also run on real hardware with UART communication and so can keep uniform structure for virtual and real targets.

Below is useful information for using UART I/O on FVP targets:

 - **Concept**: [Using-a-terminal-with-an-FVP](https://developer.arm.com/documentation/100966/latest/Getting-Started-with-Fixed-Virtual-Platforms/Using-a-terminal-with-an-FVP) and [TelnetTerminal](https://developer.arm.com/documentation/100964/1126/Fast-Models-components/Peripheral-components/TelnetTerminal) explain the concept in details.
 - **UART Drivers**: CMSIS BSP packs listed in \ref avh_fvp_cmsis contain drivers for UART access on corresponding FVP targets.
 - **Retarget to UART**: [CMSIS-Compiler component](https://arm-software.github.io/CMSIS_6/latest/Compiler/index.html) implements retargeting of standard output functions, such as `printf()`.
 - **FVP parameters**: the default values of FVP configuration parameters related to UART and Telnet should already work correctly. Refer to the FVP and Fast Models documentation as well as reference examples for additional information.
 - **Windows setup** : On Windows you need to enable Telnet, as follows:
   - Open _Start_ > _Settings_.
   - In the search box, type _Turn Windows features on or off_ and click on the suggested item. The _Windows Features_ dialog opens.
   - Select the _Telnet Client_ check box and click _OK_. The installation might take several minutes to
complete.
 - **Linux setup** : on Linux both `xterm` and `telnet` must be installed and be specified in your PATH.
 - **Logging** : If a UART output needs to be saved as a log file (for example in CI tests), you can use FVP parameter `<board>.<uart>.out_file` to specify the log file. For example for UART0 on Corstone-315: `msp4_board.UART0.out_file=./log.txt`.
   - If displaying the ouput information in an output terminal is not required (for example in CI jobs) you can disable it with FVP configuration parameter `<board>.<telnetterminal>.start_telnet`. For example for Corsone-315 and UART0: `msp4_board.telnetterminal0.start_telnet=0`. In this case the output will not be displayed in any terminal, but will be stored into a log file if this is configured accordingly with the `out_file` parameter.
 - **Multiple channels**: in complex systems and applications it can be beneficial to separate output into different UART channels and hence terminals, to avoid cluttered messages in a single terminal.
 - **Example** : [AVH-Hello](https://github.com/Arm-Examples/AVH-Hello) provides a universal example with UART output, covering all AVH FVP targets.

### Semihosting I/O {#semihosting}

Application can also rely on the semihosting mechanism that enables the code running on an FVP model to direcly use the Input/Output facilities of the host computer. With semihosting we can enable standard C I/O functions, such as `printf()` and `scanf()`, to use the host terminal from where the model is started.

Semihosting approach can be useful to quickly enable terminal communication and bypass the complexity of using UART and I/O retargeting. It also helps to  achieve a simpler implementation for rather CPU-centric test suites  with unit testing, module testings and API testing that need to be run on various CPUs and with different compilers.

Below is useful information for using semihosting for terminal output on FVP targets:

 - **Concept**: [Using semihosting](https://developer.arm.com/documentation/101470/2024-0/Controlling-Target-Execution/Using-semihosting-to-access-resources-on-the-host-computer) gives a good overview and references about semihosting on Arm targets. It is a part of Arm Development Studio documenation, and contains additional details for that environment.
 - **FVP parameters**: by default semihosting is disabled in FVPs and needs to be enabled with `semihosting-enable` configuration parameter on the CPU instance. For example for FVP_Corstone_SSE-3xx as `cpu0.semihosting-enable=1` and for FVP_MPS2_Cortex-M4 as  `armcortexm4ct.semihosting-enable=1`.
 - **GCC support**: special considerations are required when using firmware built with GCC toolchain:
   - you need to set the spec strings file in Linker options as `--specs=rdimon.specs` to use the semihosted version of the syscalls.
   - when running a project built using GCC and CMSIS, the semihosting implementation can overwrite the memory configuration. To avoid this problem, configure the required values for stack and heap using model parameters, as described in this Knowledge Base Article [How do I Avoid Stack Pointer Corruption When Semihosting is Enabled on a GCC Toolchain?](https://developer.arm.com/documentation/ka005824/).
 - **Logging**: to store the semihosted output simply redirect the terminal output of the FVP execution to a log file, using standard mechanisms provided by corresponding console, such as `tee` in Linux or `>` in bash.
 - **Examples**:
   - [CMSIS-Core Validation](https://github.com/ARM-software/CMSIS_6/tree/main/CMSIS/CoreValidation) project implements tests suite for CMSIS-Core using semihosting-based print outs. FVP configuration file can be found in [/Layer/Target](https://github.com/ARM-software/CMSIS_6/tree/main/CMSIS/CoreValidation/Layer/Target) folder for respective target, as `model-config.txt`.
   - [CMSIS-FreeRTOS Examples](https://github.com/ARM-software/CMSIS-FreeRTOS/tree/main/CMSIS/RTOS2/FreeRTOS/Examples) contain simple "hello world" style applications that use semihosting for print-outs.

Semihosting is also required for the following use cases:

 - With [CMSIS-View](https://github.com/ARM-software/CMSIS-View) component to store the events and execution times into a log file on the host machine. See more in [Event Recorder semihosting](https://arm-software.github.io/CMSIS-View/main/er_use.html#er_semihosting).
 - With \ref arm_vsocket for using the internet connectivity of the host machine.


## Execution in CI frameworks {#ci_frameworks}

Chapter [Infrastructure](./../../infrastructure/html/index.html) explains how AVH FVPs and other related tools can be programatiically installed into various Continuous Integraion (CI) frameworks, such as GitHub. To execute your programs on AVH FVPs in such workflows following is important:

 - Disable GUI visualisation, as it often is not supported by a host and not needed in CI testing:
   - Set FVP configuration parameter `<board>.visualisation.disable-visualisation=1` for the board instance on the target FVP. For example for Corstone-315 FVP it should be `mps4_board.visualisation.disable-visualisation=1`.
   - For targets with HDLCD such as Corstone-315 FVP, additionally disable the visualisation for HDLCD as `vis_hdlcd.disable_visualisation=1`.
 - Redirect the console outputs to a log file as explained in \ref console.
 - Ensure the program execution is exited when required by the test. \ref stop explains options for such exit.
 - For simpler implementation a matrix-style job configuration configuration can be used. See for example [Running multiple configurations with GitHub Actions](./../../infrastructure/html/avh_gh_actions.html#avh_gh_matrix).


## Execution timing {#timing}

FVP simulation models are targeted to software development and functional testing, and are not  suitable for accurate performance comparisons on the CPU level. However, they can be well used to analyze timing on the program level, such as for scheduling RTOS tasks, detecting deadlocks, but also identifying overall performance trends.

Following mechanisms and settings can be used for timing control and measurements:

 - FVP model can be started with command-line option `--stat` to print the execution statistics on simulation exit. Here is an example of such statistics output:
   ```
   --- cpu_core statistics: ------------------------------------------------------
   Simulated time                          : 0.651964s
   User time                               : 0.843750s
   System time                             : 0.109375s
   Wall time                               : 1.503559s
   Performance index                       : 0.43
   cpu_core.cpu0                           :  68.40 MIPS (    65196784 Inst)
   -------------------------------------------------------------------------------
   ```

  Also see section [Displaying the total execution time](https://developer.arm.com/documentation/100965/latest/Timing-Annotation/Timing-annotation-tutorial/Setting-up-the-environment/Displaying-the-total-execution-time-of-the-simulation) in the Fast Models User Guide.

 - [CMSIS-View](https://github.com/ARM-software/CMSIS-View) utility can be used to measure and analyze timing between events in the program, including statistical data. To store the log files on FVPs, \ref semihosting "semihosting" shall be enabled. CMSIS-View annotations can also be reused for event analysis and time measurement on real hardware.
 - \ref Config parameters can be used to control and impact the execution timing:
   - With Cycle Per Instruction (CPI) settings `cpi_div` and `cpi_mul`.
   - With clock configurations such as Clock Rate Multiplier, for example `core_clk.mul` on Corstone-300.
   - With pipeline-impacting parameters such as for memory caches, Floating-Point-Unit (FPU) or M-Profile Vector Extensions (MVE), etc.
   .

Chapter [Timing Annotations](https://developer.arm.com/documentation/100965/latest/Timing-Annotation) in the Fast Models User Guide explains the performance estimation concept as implemented in the underlying FastModels technology. Note that the FVPs are built with Timing Annotations enabled (`FASTSIM_DISABLE_TA` set to 0).

For interaction with external world such as via \ref arm_vsi or \ref semihosting the timing differences need to be taken into account as explain in [Timing-considerations-for-FVPs](https://developer.arm.com/documentation/100966/1126/Getting-Started-with-Fixed-Virtual-Platforms/Timing-considerations-for-FVPs).

## Execution stop {#stop}

Embedded applications typically run with an infinite loop that ensures continuous program execution. But for executing regression tests as part of Continuous Integration (CI) workflows it is often required that program execution is stopped after a test is completed, so that the next test can be started.

FVP command line options `--cpulimit`, `--cyclelimit`, `--timelimit` and `--simlimit` can be used to stop execution after specified activity time, for example, for 20 wall-clock seconds, use `--timelimit 20`. See [FVP command line options](https://developer.arm.com/documentation/100966/latest/Getting-Started-with-Fixed-Virtual-Platforms/FVP-command-line-options) for more details.

FVP models have `shutdown_on_eot` parameter that enables simple implementation of program exit. The parameter should be set in the \ref Config, for example for FPV_Corstone_SSE-300:

```
mps3_board.uart0.shutdown_on_eot=1   # (bool, init-time) default = '0' : Shutdown simulation when a EOT (ASCII 4) char is transmitted (useful for regression tests when semihosting is not available)
```

And then to trigger the shutdown, a EOT (ASCII 4) symbol can be transmitted to the corresponding serial interface from the program. The code below demonstrates an example, where the execution is stopped after target execution count is achieved. In this implementation the STDIO is assumed to be retargeted to the UART0:

```c
  while (1)  {
    printf ("Hello World %d\r\n", count);
    if (count > 100) printf ("\x04");  // EOT (0x04) stops simulation
    count++;
    osDelay (1000);
  }
```
