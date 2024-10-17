# AVH FVPs with Arm GitHub Actions {#avh_gh_actions}

GitHub Actions allow you to automate build, test, and deployment pipelines for GitHub-based projects.

A GitHub Actions workflow executes your commands on a Virtual Machine (GitHub Runner) that is hosted either directly by GitHub or can be self-hosted. It is event-driven, meaning that you can run a series of commands on a specified event such as push of a new commit or creation of a pull request. Refer to [Introduction to GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions) for information about the components of GitHub Actions.

This section explains how to setup your GitHub Actions environment for executing programs on AVH FVPs.

## Setup with CMSIS-Actions {#arm_cmsis_actions}

Arm provides several GitHub Actions that simplify installation of AVH FVPs and other Arm Tools within your GitHub CI workflows. Following actions are maintained in the [github.com/ARM-software/cmsis-actions](https://github.com/ARM-software/cmsis-actions) repository:

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

 - **armlm action** activates an Arm user based license (UBL) for Arm Tools on your GitHub Runner.<br/>
 For example add the following step to your workflow to activate a Keil-MDK Community license that allows evaluation and open-source usage of Arm Tools:
 ```yml
 - name: Activate Arm license
   uses: ARM-software/cmsis-actions/armlm@v1
 ```
 The activated environment is preserved into `$GITHUB_PATH` and `$GITHUB_ENV` so that it can be used by subsequent steps.
.

The actions execute on the GitHub Runner operations for vcpkg-based tool download and license activation as explained in the \ref avh_fvp_artifactory.

## Program Execution {#avh_gh_run}

After AVH FVPs and other tools are installed and activated on the GitHub Runner (see \ref arm_cmsis_actions) you can use the command line interface for building your project (e.g with `cbuild` utility) and run the firmware on an AVH FVP target (see [Running User Applications in CLI](../../simulation/html/using.html#Execution)).

For example, the code snippet below adds to a GitHub Actions workflow a step with program execution on Corstone-320 FVP target:

```yml
name: Execute
        run: |
          echo "Running project example ..."
          FVP_Corstone_SSE-320 -f fvp_config.txt -a Project.axf | tee Project.avh.log
```

Also see [Execution in CI frameworks](../../simulation/html/hints.html#ci_frameworks) for useful hints about running FVPs in CI workflows.

## Running multiple configurations {#avh_gh_matrix}

Software often needs to be tested in multiple configurations, with different toolchains and on different platforms. To simplify job definition for such variations you can use [matrix strategy in GitHub Action](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs).

For example the code snapshot below defines a two-dimensional matrix for Corstone-320/315/310/300 targets with Arm Compiler 6, GCC and Clang:

```yml
matrix:
  target: [CS320, CS315, CS310, CS300]
  compiler: [AC6, GCC, Clang]
```

And then in your job descriptions you can use `${{ matrix.target }}` and  `${{ matrix.compiler }}` variables, that GitHub Actions will automatically iterate over for you.

See [AVH-Hello](https://github.com/Arm-Examples/AVH-Hello) as a simple example where such matrix strategy is implemented for building the program with different toolchains and for different AVH FVP targets.

Note that use of [csolution project format](https://github.com/Open-CMSIS-Pack/cmsis-toolbox/blob/main/docs/YML-Input-Format.md) greatly simplifies project definition and build for different target types and build configurations. It well integrates with the GitHub Actions matrix for CI jobs.

## Examples  {#avh_ci_template}

See chapter [Examples](../../examples/html/index.html) for reference implementations that use \ref arm_cmsis_actions "CMSIS-Actions" for environment setup and subsequently perform project build and program execution on AVH FVP targets. Refer to the project's `./github/workflows/` directory for the implemented GitHub Actions workflows.
