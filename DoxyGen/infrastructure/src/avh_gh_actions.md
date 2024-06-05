# AVH FVPs with GitHub Actions {#avh_gh_actions}

GitHub Actions allow you to automate build, test, and deployment pipelines for GitHub-based projects.

A GitHub Actions workflow executes your commands on a Virtual Machine (GitHub Runner) that is hosted either directly by GitHub or can be self-hosted. It is event-driven, meaning that you can run a series of commands after a specified event such as push of a new commit or creation of a pull request. Refer to [Introduction to GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions) for information about the components of GitHub Actions.

This section explains how to setup your GitHub Runner environment for executing programs on AVH FVPs.

## Setup with CMSIS-Actions {#arm_cmsis_actions}

Arm provides several GitHub Actions that simplify installation and use of AVH FVPs and other Arm Tools within your own GitHub CI workflows. Following actions are maintained in the [github.com/ARM-software/cmsis-actions](https://github.com/ARM-software/cmsis-actions) repository:

 - **vcpkg action**  performs environment setup from Arm Tools Artifactory based on vcpkg configuration.<br/>This follows the concept explained in \ref avh_fvp_vcpkg.<br/>
 Following step can be added to the workflow to execute this action:
 ```
 - name: Setup vcpkg environment
   uses: ARM-software/cmsis-actions/vcpkg@v1
   with:
     config: "./vcpkg-configuration.json"
     vcpkg-downloads: "${{ github.workspace }}/.vcpkg/downloads"
     cache: "-"
 ```
.

- **armlm action** activates an Arm user based license (UBL) on GitHub Runner.<br/>
 For example add the following step to your workflow to activate a Keil-MDK Community license that allows evaluation and open-source usage of Arm Tools:
 ```yml
 - name: Activate Arm license
   uses: ARM-software/cmsis-actions/armlm@v1
 ```
 The activated environment is preserved into `$GITHUB_PATH` and `$GITHUB_ENV` so that it can be used by subsequent steps.


## Program Execution {#avh_gh_run}

After AVH FVPs and other tools are installed and activated on the GitHub Runner (see \ref arm_cmsis_actions) you can use the command line interface for building your project (e.g with cbuild utility) and run the firmware on the AVH FVP target (see [Running User Applications in CLI](../../simulation/html/using.html#Execution)).

For example, the code snippet below adds to a GitHub Actions workflow a step with program execution on Cortex-M3 FVP target:

```yml
name: Execute
        run: |
          echo "Running get started example ..."
          FVP_MPS2_Cortex-M3 --simlimit 10 -f fvp_config.txt -a Project.axf | tee Project.avh.log
```

## Example Template {#avh_ci_template}

[AVH_CI_Template](https://github.com/Arm-Examples/AVH_CI_Template) provides an example that uses \ref arm_cmsis_actions "CMSIS-Actions" for environment setup and subsequently performs project build with Arm Compiler and program execution on an AVH FVP target. See its Readme for detailed description and [.github/workflows/basic.yml](https://github.com/Arm-Examples/AVH_CI_Template/blob/main/.github/workflows/basic.yml) for the GitHub workflow implementation.
