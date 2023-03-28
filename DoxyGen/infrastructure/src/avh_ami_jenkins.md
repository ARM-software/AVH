# Run AMI with Jenkins {#run_ami_jenkins}

Use of Arm Virtual Hardware (AVH) AMI can be integrated into [Jenkins pipelines](https://www.jenkins.io/) for automating software builds and tests.

Two approaches can be followed to create and control instances of the AVH AMIs with Jenkins:
- \ref avh_jenkins_node : a classic approach with a Jenkins node created in AWS.
- \ref avh_module_jenkins : a simplified way with Jenkins as a thin wrapper on top of AVH Client python module.

Example implementations of both approaches are provided in [GetStarted example](https://github.com/ARM-software/AVH-GetStarted/) and explained in this chapter.

\note
   Refer to \ref mainpage "Infrastructure" for others ways to use the Arm Virtual Hardware.

## Using AVH AMI as a Jenkins node {#avh_jenkins_node}
This is a common way to implement Jenkins pipelines on AWS.

A Jenkins Controller uses Amazon EC2 plugin to create an EC2 instance as a Jenkins node from an AVH AMI. Then the Jenkins node gets connected by SSH to the Jenkins Controller and the Jenkins commands are executed directly on the EC2 instance.

### Implementation example
The example implementation is available in [.jenkins/AVH-as-Jenkins-Node/](https://github.com/ARM-software/AVH-GetStarted/tree/main/.jenkins/AVH-as-Jenkins-Node/) and consists of the following items:

- `configuration-as-code/` provides an example of Amazon EC2 plugin code.
- `jobDSL/`  contains Jenkins configuration as code to create the AVH Jenkins Job.
- `pipeline/`  implements an example pipeline for running AVH AMI as Jenkins Node.

### Dependencies
#### AWS Account

Following resources are required on the AWS side:

- \ref Subscribe "Subscription" to Arm Virtual Hardware AMI.
- IAM User with Access Keys for the AWS Account. IAM setup can be found at [plugins.jenkins.io/ec2/\#plugin-content-iam-setup](https://plugins.jenkins.io/ec2/#plugin-content-iam-setup).
- EC2 Security Group with Ingress SSH port allowed.
- SSH Keys to communicate with the EC2 instance as Jenkins Node.
- Subnet Id needs to be informed with EC2 instance.

An AWS Cloudformation template file can be used to create most of the required AWS Resources for AVH AMI, please refer to [./infrastructure/cloudformation/](https://github.com/ARM-software/AVH-GetStarted/tree/main/infrastructure/cloudformation) folder in the GetStarted example.

#### Jenkins plugins
Following Jenkins plugins are used by the example implementation:

- [Amazon EC2](https://plugins.jenkins.io/ec2/) - Tested on v1.57
- [JobDSL - needed if the JobDSL code is used](https://plugins.jenkins.io/job-dsl/) - Tested on v1.77

#### Jenkins credentials
Following Jenkins credentials need to be configured:
- AWS Credential for IAM User (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`)
- AWS SSH Private Key to be associated with the EC2 instance.

## Using AVH Client {#avh_module_jenkins}
In this approach, a python module [*avhclient*](https://github.com/ARM-software/avhclient) drives the communication with the AVH AMI. The Jenkins pipeline is just a light-weight front end that uses the AVH Client module, and the actual work is done by an EC2 instance created and controlled with the commands from the avhclient built on top of AWS SDK.

This approach is simpler to implement but the capabilities are limited by the functionality of the avhclient.

### Implementation example
The example implementation using Jenkins with avhclient is available in [.jenkins/Using-AVH-Module/](https://github.com/ARM-software/AVH-GetStarted/tree/main/.jenkins/Using-AVH-Module) and consists of the following items:

- `jobDSL/`  contains Jenkins configuration as code to create the AVH Jenkins Job.
- `pipeline/`  implements an example pipeline for running AVH AMI using avhclient Python Module.

### Dependencies
#### AWS Account

Following resources are required on the AWS side:

- \ref Subscribe "Subscription" to Arm Virtual Hardware AMI.
- IAM User with Access Keys for the AWS Account.
- IAM Instance Profile to be associated with the AVH EC2 instances.
- S3 Bucket to store temporary files.
- EC2 Security Group with Ingress SSH port allowed.
- [*Optional*] SSH Key if you would like to debug on EC2.
- Subnet Id needs to be informed with EC2 instance.

An AWS CloudFormation template file can be used to create the required AWS resources for AVH AMI. Refer to   [./infrastructure/cloudformation/](https://github.com/ARM-software/AVH-GetStarted/tree/main/infrastructure/cloudformation) folder in the GetStarted example.

#### Jenkins plugins
Following Jenkins plugins are used by the example implementation:

- [CloudBees AWS Credentials](https://plugins.jenkins.io/aws-credentials/) - Tested on v1.29
- [Pyenv-pipeline](https://plugins.jenkins.io/pyenv-pipeline/) - Tested on v2.1.2
- [JobDSL - needed if the JobDSL code is used](https://plugins.jenkins.io/job-dsl/) - Tested on v1.77

#### Jenkins credentials
Following Jenkins credentials need to be configured:
- AWS Credential for IAM User (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`)
- [*Optional*] AWS SSH Private Key to be associated with the EC2 instance.