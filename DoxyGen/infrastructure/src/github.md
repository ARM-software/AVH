
# Run AMI with GitHub Actions {#run_ami_github}

GitHub Actions help you automate tasks within your software development life cycle. GitHub Actions are event-driven, meaning that you can run a series of commands after a specified event has occurred.  For example, every time someone commits a push or creates a pull request for a repository, you can automatically run the Arm VHT Services that execute automated build or test scripts. Refer to [Introduction to GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions) for information about the components of GitHub Actions.

There are several different ways to execute GitHub Actions:
  - [**Self-hosted GitHub runners**](./#self_hosted) where the complete GitHub Action is executed on an AWS EC2 Linux instance.
  - [**GitHub-hosted runners**](./#GitHub_hosted) where only a part of the GitHub Action (for example testing) is executed on an AWS EC2 Linux instance.
  
The approach that you should choose depends on your CI/CD requirements.

# Self-hosted GitHub Runners {#self_hosted}

The following steps explain how to use **self-hosted GitHub runners** with [AWS Marketplace: \prj_name](https://aws.amazon.com/marketplace/search/results?searchTerms=Arm+Virtual+Hardware).

  1. [**Setup Github**](#self-hosted1) to obtain a control point for your runner.
  2. [**Setup AWS EC2 Instance**](#self-hosted2), install and connect the runner agent.
  3. [**Add github actions**](#self-hosted3) to your GitHub repository and configure it for your requirements.
  
  
## Setup Github {#self-hosted1}
From your github repository on github.com, go to Settings > Actions > Runners > New self-hosted runner. Make sure you have selected "Operating System: Linux x86" and follow the instructions of [Setup AWS EC2 Instance](#self-hosted2). 


## Setup AWS EC2 Instance {#self-hosted2}
Before you start with the following steps, make sure you created an EC2 instance on your AWS account. For instructions, see: [Launch through EC2](https://arm-software.github.io/VHT/main/infrastructure/html/run_ami_local.html#Launch_EC2).

  1. Open an SSH connection as described on: [Connect to the EC2 instance](https://arm-software.github.io/VHT/main/infrastructure/html/run_ami_local.html#connect)
  
  Follow these steps on SSH:

  1. Gain proper permissions: `sudo -u ubuntu bash && cd /home/ubuntu`
  2. Download the latest installer: `curl -o actions-runner-linux-x64-2.283.3.tar.gz -L https://github.com/actions/runner/releases/download/v2.283.3/actions-runner-linux-x64-2.283.3.tar.gz`
  3. Extract the installer: `tar xzf ./actions-runner-linux-x64-2.283.3.tar.gz`
  4. Create the runner instance with the personal token shown on github. Copy and paste the instruction from github. It will look similar to: `./config.sh --url https://github.com/myuser/myproject --token ABCDEFGHIJKLMNOP`
  5. Launch the runner: `./run.sh`


## Add GitHub Action {#self_hosted3}

Using the github runner is very simple. All jobs in the workflow file that should be executed on the EC2 instance via the runner, need to have the **runs-on** parameter added:

` runs-on: self-hosted `

This is a sample workflow for projects that run on an self-hosted runner:

``` yml
name: Arm Virtual Hardware example 

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

# To allow you to run this workflow manually from the GitHub Actions tab add
  workflow_dispatch:

jobs:
  ci_demonstration:
    runs-on: self-hosted
    env:
      working-directory: ${{ github.workspace }}/Platform_FVP_Corstone_SSE-300_Ethos-U55/
    steps:
      - name: Check out repository code
        uses: actions/checkout@v2

      - name: What has been cloned?
        run: echo "${{ github.repository }} has been cloned."

      - name: Get dependencies
        run: cp_install.sh packlist
        working-directory: ${{env.working-directory}}

      - name: Build the micro_speech example
        run: cbuild.sh microspeech.Example.cprj
        working-directory: ${{env.working-directory}}

      - name: Run the micro_speech example
        run: ./run_example.sh
        working-directory: ${{env.working-directory}}

```

Once this steps are completed, any commit or pull request to the repository should trigger the *CI* workflow that you have defined.
Make sure that the EC2 instance is up and in running state, for the github runner to be available to your actions.




# GitHub-hosted Runners {#GitHub_hosted}

The following steps explain how to use **GitHub-hosted runners** with [AWS Marketplace: \prj_name](https://aws.amazon.com/marketplace/pp/prodview-urbpq7yo5va7g).
The github-hosted runner will run the action on an github-hosted VM instance. A plugin is provided to provide remote execution on Arm Virtual Hardware. The plugin manages connection, upload and execution of a test suite on Amazon EC2 Linux instance that runs an \ref AWS "Arm VHT AMI". It also provides run-control of the EC2 instance itself, starting and stopping on demand.

![VHT GitHub action](./images/Github-GH-AWS.png "VHT GitHub action for AMI integration")

  1. [**Create user roles on AWS IAM**](#github_hosted1)
  2. [**Setup AWS EC2 Instance**](#github_hosted2), obtain the *access information*.
  3. [**Setup AWS S3 Instance**](#github_hosted3)
  4. [**Add GitHub Secrets**](#github_hosted4) with the *access information* to your GitHub repository with gives access to the AWS EC2 instance.
  5. [**Add GitHub Action**](#github_hosted5) to your GitHub repository and configure it for your requirements.


The VHT-AMI action receives a *.tar input file (vht_in) that contains the vht.yml control file. The vht.yml is the run control commands for the AMI and defines the execution of build scripts or test runs. Once the AMI run control commands are complete the results are returned as *.tar file to the GitHub runner.

The file [action.yml](https://github.com/ARM-software/VHT-AMI/blob/master/action.yml) defines the parameters for the GitHub action.



## Create user roles on AWS IAM {#github_hosted1}
The following AWS account requirements are needed to run VHT-AMI action.

1. ### Create Identity and Access Management (IAM) User
You have to create an IAM User to limit resource permission to your CI. In addition, the IAM User provides fixed `AWS Access Key Id` and `AWS Secret access key` values. 

**Make notes of the the users credentials as you will need them in futures steps of the setup.**

For this user, you have to add the following `policies`:
- vht-passrole (created before)
- AmazonEC2FullAccess (AWS managed policy --> It already exists in your account)
- AmazonS3FullAccess (AWS managed policy --> It already exists in your account)
- AmazonSSMFullAccess (AWS managed policy --> It already exists in your account)

You also need to add the following `Permission boundary`:
- PowerUserAccess

The user can be called `vht`.

More information on the AWS documentation: [Create IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)

2. ### Create PassRole policy for VHT-AMI
You need to create a PassRole IAM policy to be attached to our IAM User with the following content.
You can name it `vht-passrole`.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "*"
        }
    ]
}
```

More information on the AWS documentation: [Create IAM Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html)

3. ### Create an IAM Role For EC2 Services
You have to create IAM Role to be attached to the EC2 Instances. This role gives EC2 Instances access to S3 buckets and SSM services.
For this role, you have to add the following `policies`:
- AmazonS3FullAccess
- AmazonSSMFullAccess

You also need to add the following `Permission boundary`:
- PowerUserAccess

More information on the AWS documentation: [Create IAM Role For Service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)


## Setup AWS EC2 Instance {#github_hosted2}
Make sure you created an EC2 instance on your AWS account. For instructions, see: [Launch through EC2](https://arm-software.github.io/VHT/main/infrastructure/html/run_ami_local.html#Launch_EC2).
Once created you need to make notes of the Instance ID, for later reference. You can stop the machine once it has reached running state. The plugin will start the machine on demand.

## Setup AWS S3 Instance {#github_hosted3}

Use the AWS console to create an S3 storage with default options. Note the name to specify it the the parameters of the actions afterwards.

## Add Github Secrets {#github_hosted4}

Add the information from the last to steps to the secrets of your github repository. Secrets cannot be reviewed and are a secure way of providing the access credentials to the plugin. 

From your github repository on github.com, go to Settings > Secrets > Actions > New repository secret.

We recommend to add the Instance ID of the EC2 instance, and the IAM Access key pair into secrets with the following names:
AWS_INSTANCE_ID
AWS_ACCESS_KEY
AWS_ACCESS_KEY_SECRET

More information on github documentation: [Creating encrypted secrets for a repository](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) 



## Add Github Action {#github_hosted5}

The basic idea of creating a github-hosted CI flow is to run steps on the github VM instance - except build and execution of test cases. The testsuite contains of a collection of files that are required on the VHT instance on AWS and a yaml-based inventory file, that includes instructions. This file is called **vht.yml**. It will mark the root of a folder used to stage a testsuite on the Github VM. 

A complete example workflow is found in the example hosted on: https://github.com/ARM-software/VHT-TFLmicrospeech

### Prepare the testsuite

Steps before the actual execution should copy every file required to staging folder. It will then be passed in the vht_in parameter. File and path references in the vht.yml should be relative to the root of this folder, where also the vht.yml needs to be placed.

Refer to https://github.com/ARM-software/VHT-TFLmicrospeech/blob/main/.github/workflows/virtual_hardware_gh.yml for some detailed example.

### The vht.yml

vht.yml describes the content of the testsuite, assets, build and test run instructions. It is located in the root of the folder specified in vht_in. Its format is YAML (https://yaml.org/spec/)

### The YAML structure

``` yml
suite:
  name: <value>
  model: <value>
  configuration: <value>^
  pre: <value>
  post: <value>

  builds:
   - "<value>":
      shell: <value>
      pre: <value>
      post: <value>


  tests:
   - "<value>":
      executable: <value>
      arguments: <value>
      pre: <value>
      post: <value>
      timeout: <value>
```

#### **suite**

|  keyword      |  description                                       |
|---------------|----------------------------------------------------|
| suite         |  Starts the declaration of a testsuite             |
| name          |  Name of the testsuite                             |
| model         |  Executable name of the FVP used                   |
| configuration |  Configuration file for the FVP                    |
| pre           |  Execute command on shell before suite or test     |
| post          |  Execute command on shell after suite or test      |

#### **builds** (optional)

|  keyword      |  description                                       |
|---------------|----------------------------------------------------|
| builds        |  Starts a list of build declarations               |
| shell         |  Execute command on shell that builds executable   |
| pre           |  Execute command on shell before suite or test     |
| post          |  Execute command on shell after suite or test      |

#### **tests**

|  keyword      |  description                                       |
|---------------|----------------------------------------------------|
| tests         |  Starts a list of test declarations                |
| executable    |  ELF format executable file to be executed on test |
| arguments     |  Additional arguments passed to FVP                |
| timeout       |  Optional timeout for test                         |
| pre           |  Execute command on shell before suite or test     |
| post          |  Execute command on shell after suite or test      |

### Example

``` yml
suite:
  name: "Tensorflow lite micro examples"
  model: "/opt/arm_vsi/arm_vsi.x"
  configuration: ""
  pre: ""
  post: ""

  builds:
   - "microspeech example":
      shell: "cbuild.sh ./Platform_FVP_Corstone_SSE-300_Ethos-U55/microspeech.Example.cprj"
      post: "cp ./Platform_FVP_Corstone_SSE-300_Ethos-U55/Objects/microspeech.axf ./elf/" 

  tests:
   - "microspeech example":
      executable: "./elf/microspeech.axf"
      arguments: "-V ./VSI/audio/python -f fvp_config.txt -a Objects/microspeech.axf --stat $*"
      pre: ""
      post: ""
      timeout: 20
```

### Use Action

You can now consume the action by referencing the v1 branch...

```
uses: Arm-Software/VHT-AMI@v1
with:
  vht_in:
  instance_id: ${{ secrets.AWS_INSTANCE_ID }}
  access_key_id: ${{ secrets.AWS_INSTANCE_ID }}
  secret_key_id: ${{ secrets.AWS_ACCESS_KEY_SECRET }}
  aws_region: "eu-west-1"
  s3_bucket_name: my_bucket
```

**Where**

 - vht_in is the folder to the staged files, with vht.yml in root.

 - *secrets.AWS_INSTANCE_ID* is the instance ID of the AMI stored as GitHub secret.

 - *secrets.AWS_ACCESS_KEY_ID* is the access key to AMI stored as GitHub secret.

 - *secrets.AWS_SECRET_KEY* is the secret key to AMI stored as GitHub secret.

 - aws_region: name of the region your EC2 and S3 instances are located

 - s3_bucket_name: for temporary storage an S3 bucket is used

