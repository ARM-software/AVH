# Infrastructure {#mainpage}

The [**\prj_name Targets**](../../simulation/html/index.html) can be accessed via:

  - \ref AWS 
  - \ref Local

## AWS Marketplace {#AWS}

Arm provides on **AWS Marketplace** a ready-to-use [**Amazon Machine Image (AMI)**](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) with **\prj_name Targets**, various compilers, other tools, and resources. The tools are executed in a Linux Virtual Machine and allows you to use the \prj_name environment in various different environments.

The following AWS tutorials help you to get started:

  - [How do I create and activate a new AWS account?](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
  - [Tutorial: Get started with Amazon EC2 Linux instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)

### Subscribe \prj_name {#Subscribe}

Before you can use the **AMI with \prj_name Targets** you should have a AWS account.  The following steps describe how to subscribe to the AWS Service for \prj_name:
  - Open [AWS Marketplace](https://aws.amazon.com/marketplace) and search for **\prj_name**. 
  - Click on **\prj_name** to open the product page.
  - Click on **Continue to Subscribe** to active the product.
  - Click on **Configure this software** and select the parameters. Note that this page gives you access to the **Ami Id**.
  - Click on **Continue to Launch** to active the **\prj_name**.  You have various ways to use the AMI as described in the next section.  


### Use AMI 

The **AMI** provides a lot of flexibility and gives you the option to integrate **\prj_name** various CI/CD DevOps environments that range from on-premise IT to Cloud-native infrastructure. The following sections give you some flavors of possible integrations:

  - \subpage run_ami_local allows to use the AMI from a local computer.
  - \subpage run_ami_github explains how to integrate the **\prj_name AWS AMI ** in GitHub action workflows.

  
## Local Tool Installation {#Local}

Arm provides [**\prj_name Targets**](../../simulation/html/index.html) also as part of [**Keil MDK-Professional edition**](https://developer.arm.com/mdk). This local tool installation allows to setup and create test cases and to analyze/debug test case failures.

  - \subpage run_mdk_pro explains how to use **\prj_name Targets** with Keil MDK.

\note
  - [**ON ROADMAP**](../../overview/html/index.html#Roadmap): This feature is in development an will become available in the next few weeks.  

