# AVH Client {#avhclient}

**Arm Virtual Hardware Client (avhclient)** is a python module for deploying projects on Arm Virtual Hardware from a command-line interface (CLI). The implementation is maintained by Arm in the GitHub repository [github.com/ARM-software/avhclient](https://github.com/ARM-software/avhclient).

When using avhclient you can have uniform implementation for CI operations in various environments including local execution. Reference examples are provided for the following use cases:

- \ref run_ami_jenkins "Jenkins CI pipelines"
- \ref run_ami_github "GitHub-Actions workflows"

## Installation {#avhclient_install}

You can install AVH Client development snapshot directly from its main branch on GitHub:

```
pip install git+https://github.com/ARM-software/avhclient.git@main
```

## Supported backends {#avhclient_backends}

AVH Client can control different backends with Arm FVP models. The backend shall be specified with `-b` option preceding the actual AVH Client command. Following options are currently available:

- `aws`(default) - interacts with \ref AWS "Arm Virtual Hardware instance on AWS".
  - avhclient can create/start AVH EC2 instances from AVH AMIs, prepare the instance, upload files to the instance, execute commands and run the program, download the results back and cleanup the instance.
- `local` - operates with FVP targets installed locally.

## AWS backend setup {#avhclient_setup_aws}

AVH Client accesses AWS services via [Boto3 AWS SDK](https://github.com/boto/boto3) and for that requires a set of parameters which can be provided in different ways:
- Added as options in the command line when executing avhclient.
- Defined as environmental parameters where avhclient is running.
- Specified in the \ref avhclient_yml as aws backend property.


| Enviromental Parameter| aws backend property | Description<sup>1</sup>
|:----------------------|:---------------------|:------------------------------
| **AWS Credentials**<sup>2</sup>  | &emsp;    | **It is necessary to expose avhclient with the AWS user credentials** (IAM User is recommended, see \ref avhclient_setup_iam)
| AWS_ACCESS_KEY_ID     | -                    | (M) Key Id of the [access key pair](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for the AWS account (as IAM user) that shall be used for AWS access.
| AWS_SECRET_ACCESS_KEY | -                    | (M) Key value of the [access key pair](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for the AWS account (as IAM user) that shall be used for AWS access.
| AWS_SESSION_TOKEN     | -                    | Session token, if applicable.
|                       |&emsp;                |&emsp;
|**AWS Parameters**     |&emsp;                |&emsp;
| AWS_AMI_ID            | `ami-id`             | (O) The id of already available \ref AWS "EC2 instance with AVH AMI" that shall be used. If not specified then a new AVH EC2 instance will be created. Default is ''.
| AWS_AMI_VERSION       | `ami-version`        | (O) Version of AVH AMI to use for new EC2 instance. If not specified the latest available version will be used.
| AWS_IAM_PROFILE       | `iam-profile`        | (M) The [IAM Instance Profile](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) associated with the AVH EC2 instance granting it access to required AWS resources. Default is ''.
| AWS_DEFAULT_REGION    | `default-region`     | (O) The data center region for running new AVH AMI. Default is `eu-west-1`.
| AWS_INSTANCE_NAME     | `instance-name`      | (O) The name for the EC2 instance that will be created with AVH AMI.
| AWS_INSTANCE_TYPE     | `instance-name`      | (O) The EC2 instance type to be used when creating the EC2 instance with AVH AMI. Default is `c5.large`. See \ref Requirements.
| AWS_SECURITY_GROUP_ID | `security-group-id ` | (N) The id of the [VPC security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) that the AVH AMI instance shall be added to. Shall have format `sg-xxxxxxxx`.
| AWS_SUBNET_ID         | `subnet-id`          | (N) The id of the [VPC subnet](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html#subnet-basics) that the AVH AMI instance shall use. Shall have format `subnet-xxxxxxxx`.
| AWS_S3_BUCKET_NAME    | `s3-bucket-name`     | (N) The name of the [S3 storage bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html) to be used for temporary data storage by Arm Virtual Hardware. Not used for long-term data.
| AWS_KEEP_EC2_INSTANCES| `keep-ec2-instance`  | (O) If set to `False`, then EC2 instance will be terminated after avhclient completes its execution. If `True`, the instance will only be stopped. Default is `False`.
| AWS_KEY_NAME          | `key-name`           | (O) The name of a [security key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) to be used for SSH access to the new AVH EC2 instance. If provided, corresponding key pair shall be available in AWS. If not provided, then no SSH connection will be possible. Default is ''.
| AWS_INSTANCE_ID       | `instance-id`        | (N) The id of an EC2 instance that shall be used for running AVH AMI. If defined, then AWS_AMI_ID is ignored. Default is ''.
| AWS_EFS_DNS_NAME      | `efs-dns-name`       | (O) If set, the avhclient will try to mount Elastic File System (EFS) during the cloud-init phase. The only scenario supported for now is using Packs. Default is ''.
| AWS_EFS_PACKS_DIR     | `efs-packs-dir`      | (O) Sets the mount path relative to /home/ubuntu folder. Default folder is `packs` and if it exists locally it will be then replaced by the EFS mount. Only used when AWS_EFS_DNS_NAME is set.

> <sup>1</sup> Following abbreviations indicate if a parameter is mandatory or optional:<br/>
> &emsp;(M) Mandatory parameter. Execution will fail if not provided.<br/>
> &emsp;(O) Optional parameter. Execution could proceed with default value as well.<br/>
> &emsp;(N) Mandatory parameter when creating a new AMI instance (AWS_AMI_ID and AWS_INSTANCE_ID aren't set) <br/>

> <sup>2</sup>You can either export your AWS credentials in the enviroment  or create an AWS credential file on ~/.aws/credentials (Linux & Mac) or %USERPROFILE%.awscredentials (Windows):
> 
> ```
> [default]
> aws_access_key_id=YOUR_AWS_ACCESS_KEY_ID
> aws_secret_access_key=YOUR_AWS_SECRET_ACCESS_KEY
> aws_session_token=YOUR_AWS_SESSION_TOKEN
> ```
> More info [AWS CLI config and credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

**Example**

When creating and running a new AVH AMI instance:

Mandatory info:
```
export AWS_IAM_PROFILE='YOUR_IAM_PROFILE'
export AWS_SECURITY_GROUP_ID='YOUR_AWS_SECURITY_GROUP_ID'
export AWS_SUBNET_ID='YOUR_SECURITY_GROUP_ID'
export AWS_S3_BUCKET_NAME='YOUR_B3_BUCKET_NAME'
```
Optional info (examples):

```
export AWS_AMI_ID=DESIRED_AVH_AMI_ID
export AWS_AMI_VERSION=1.1.2
export AWS_EFS_DNS_NAME=fs-066cf410af2428e2f.efs.eu-west-1.amazonaws.com
export AWS_EFS_PACKS_DIR=packs
export AWS_KEEP_EC2_INSTANCES=true
export AWS_KEY_NAME=YOUR_AWS_KEYPAIR_NAME
export AWS_INSTANCE_TYPE=t2.micro
export AWS_INSTANCE_NAME=MY_AVH_INSTANCE
```

### CloudFormation template {#avhclient_setup_cloudformation}

AWS CloudFormation can be used to create the AWS resources required for avhclient operation with AWS backend. 

Follow the descriptions provided with [AVH CloudFormation Template](https://github.com/ARM-software/AVH-GetStarted/tree/main/infrastructure/cloudformation) to create necessary AWS resources and obtain the values required for \ref avhclient_setup_aws.

### IAM Requirements {#avhclient_setup_iam}

avhclient operation with AWS backend requires certain Identity and Access Management (IAM) configurations as explained below.

**IAM User**

The IAM User that is used by avhclient for AWS access (see *AWS credentials* in \ref avhclient_setup_aws) shall have following [IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_id-based):

- AVHPassRole,- a customer-managed policy that you need to create in your AWS account specifically for using avhclient:
```json
AVHPassrole:
  Type: 'AWS::IAM::Policy'
  Properties:
    PolicyName: AVHPassRole
    PolicyDocument: |
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
- AmazonEC2FullAccess (AWS managed policy)
- AmazonS3FullAccess (AWS managed policy)
- AmazonSSMFullAccess (AWS managed policy)

You also need to add the following *Permission boundary*:
- PowerUserAccess

More information on the AWS documentation:
- [Create IAM Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html)
- [Create IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)
- [Permissions boundaries for IAM entities](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)

**IAM Profile for EC2**

An IAM Role needs to be attached to the EC2 Instances. This role gives EC2 Instances access to S3 buckets and SSM services.
For this role, you have to add the following `policies`:
- AmazonS3FullAccess
- AmazonSSMFullAccess

You also need to add the following `Permission boundary`:
- PowerUserAccess

More information on the AWS documentation: [Create IAM Role For Service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html)

## AVH YML file {#avhclient_yml}

avhclient `execute` command requires a file in [YML format](https://yaml.org/spec/) that describes details of individual steps to be executed on Arm FVP models. The fields available in the file syntax are explained below:

| Field            |  Description
|:-----------------|:---------------------------------------------------
| `name:`          | *[optional]* The name of the workload.
| `workdir:`       | *[optional]* The local directory to use as the workspace. Default is the folder with the yml file.
| `backend:`       | *[optional]* Backend specific parameters.<br/>&emsp;`aws:`&emsp;*[optional]* AWS backend specific parameters (see backend help)<br/>&emsp;`local:` *[optional]* local backend specific parameters (see backend help)
| `upload:`        | *[optional]* List of files (relative to `workdir`) to be sent to the AVH backend (see glob format below).
| `steps:`         | *[mandatory]* List of steps to be executed on the AVH backend.<br/>&emsp;`run:` string written into a bash script and executed on the AVH backend inside the workspace directory.
| `download:`      | *[optional]* List of files (relative to `workdir`) to be retrieved back from the AVH backend (see glob format below).

**Glob format:**

The list of glob patterns is evaluated in order.
 - Wildcard '*' matches all files but no directory except hidden files (starting with '.').
 - Wildcard '**' matches all files and directories except hidden files/directories (starting with '.').
 - Inclusive matches (no prefix) are added to the file list.
 - Exclusive (prefixed with '-:') matches are removed from current file list.

A JSON schema for automatic checks and auto-completion is available in [ARM-software/avhclient/schema/avh.schema.json](https://github.com/ARM-software/avhclient/blob/main/schema/avh.schema.json).

**Example**

```yml
# yaml-language-server: $schema=https://raw.githubusercontent.com/ARM-software/avhclient/main/schema/avh.schema.json

name: "AVH GetStarted Example"
workdir: ./
backend:
  aws:
    ami-version: ~=1.1
    instance-type: t2.micro
upload:
  - RTE/**/*
  - -:RTE/**/RTE_Components.h
  - basic.debug.cprj
  - build.py
  - main.c
  - requirements.txt
  - retarget_stdio.c
  - fvp_config.txt
  - README.md
steps:
  - run: |
      pip install -r requirements.txt
      python build.py --verbose build run
download:
  - RTE/**/RTE_Components.h
  - Objects/basic.axf
  - Objects/basic.axf.map
  - basic-*.xunit
  - basic-*.zip
```
