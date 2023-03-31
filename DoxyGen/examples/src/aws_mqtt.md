# AWS MQTT Example {#aws_mqtt}

[comment]:[TOC]

This example is based on [AWS coreMQTT mutual authentication demo](https://docs.aws.amazon.com/freertos/latest/userguide/mqtt-demo-ma.html) and demonstrates how to use cloud-connectivity on Arm Virtual Hardware (AVH) via [VSocket interface](../../simulation/html/group__arm__vsocket.html), and how to verify such communication with Continuous Integration (CI) workflows. The project is maintained in the GitHub repository [**github.com/ARM-software/AVH-AWS_MQTT_Demo**](https://github.com/ARM-software/AVH-AWS_MQTT_Demo) that also contains additional description of the example.

## Overview {#aws_mqtt_overview}

The AWS MQTT Example application connects to [AWS MQTT broker](https://docs.aws.amazon.com/en_en/iot/latest/developerguide/mqtt.html) using TLS with mutual authentication between the client and the server. As a network interface either Ethernet or WiFi can be used on hardware boards, or VSocket on Arm FVP models. The application subscribes to MQTT topics and publishes messages that can be observed in AWS IoT MQTT client.

Automated test execution is managed with GitHub Actions and gets triggered on
every code change in the repository. The program gets built and run on [Arm
Virtual Hardware](https://www.arm.com/products/development-tools/simulation/virtual-hardware) cloud infrastructure in AWS and the test results can
be then observed in repository's [GitHub Actions](https://github.com/ARM-software/AVH-GetStarted/actions).

## Prerequisites {#aws_mqtt_prerequisites}

Following is required to reproduce operation of the example project:

* a [GitHub](https://github.com/) account
* an [AWS](https://aws.amazon.com/) account with [subscribtion to Arm Virtual Hardware](../../infrastructure/html/AWS.html#Subscribe)

## Device commissioning

In order to communicate with the AWS IoT service the embedded application needs to be commissioned with proper connection and security parameters that match the configuration in the cloud service. \ref aws_iot_thing describes how to setup necessary endpoint in the AWS and \ref aws_iot_params explains how to apply the parameters in the embedded code.

### Create AWS IoT Thing {#aws_iot_thing}

The communication and security parameters can be obtained from [AWS IoT Core](https://aws.amazon.com/iot-core/) service. Steps below explain the process for this example and AWS tutorial [Create AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/create-iot-resources.html) provides general overview and additional references.

Create an AWS **IoT Thing** for your device as follows:

- From your AWS Management Console browse to the **AWS IoT Core** service.
- In the left navigation pane, choose **Manage**, and then choose **Things**.
- On the Things page click **Create things** button, choose **Create a single thing** and proceed further.
- In the thing properties provide a name for your thing (for example *MyThing*), keep other parameters at default and then choose **Next**. Later you will need to provision the same name to the embedded code.
- Choose to Auto-generate a certificate for your thing.
- When offered to attach policies to certificate, click **Create policy** to open corresponding page in a separate browser tab. There:
  - Enter a name for the policy (for example “MyThingPolicy”).
  - In the **Policy document** area add new statements, each with **Policy effect** set to **Allow** and following values in **Policy action** respectively:
    - **iot:Connect**
    - **iot:Publish**
    - **iot:Subscribe**
    - **iot:Receive**
  - In the **Policy resource** set * for all statements.
  - Click on **Create** and observe the new policy appeared in the list.
- Return to the browser tab where offered to attach policies to certifate and observe the created. There:
  - Select the policy to be attached to the certificate.
  - Click **Create thing**.
  - Download the certicate, public and private keys by choosing the **Download** links for each.
- Make a note of your Device data endpoint.
  - In the navigation pane of the AWS IoT console, choose **Settings** and there find the  **Device data endpoint** such as *a3xyzzyx.iot.us-east-2.amazonaws.com* to have it ready for later.

Now you have all information required for connecting your device to the AWS IoT Cloud.

### Commission parameters to device {#aws_iot_params}

In the example code the required commissioning parameters are defined in the following files:

- [`aws_clientcredential.h`](https://github.com/ARM-software/AVH-AWS_MQTT_Demo/blob/main/amazon-freertos/demos/include/aws_clientcredential.h)
- [`aws_clientcredential_keys.h`](https://github.com/ARM-software/AVH-AWS_MQTT_Demo/blob/main/amazon-freertos/demos/include/aws_clientcredential_keys.h)

Note: when the project is imported to uVision these files are present in the `demos_include` group.

Specifically following definitions need to be updated:
- `clientcredentialMQTT_BROKER_ENDPOINT`: Device data endpoint
  - Take the value in AWS IoT Console under **Settings**, it appears in format such as a3xyzzyx.iot.us-east-2.amazonaws.com.
- `clientcredentialIOT_THING_NAME`: Thing Name
  - Use the name specified in \ref aws_iot_thing
- `keyCLIENT_CERTIFICATE_PEM`: Client Security Certificate
  - Provide here the value from the device certificate file (*\*.perm.crt*) associated with the AWS Thing named above.
- `keyCLIENT_PRIVATE_KEY_PEM`: Client Private Key
  - Provide here the value from the private key file of the certificate associated with the AWS Thing named above.
- `clientcredentialWIFI_SSID`: WiFi Access Point SSID (when connecting via WiFi, can be empty otherwise).
- `clientcredentialWIFI_PASSWORD`: WiFi Access Point Password (when connecting via WiFi, can be empty otherwise).

Note that when running the example on Arm Virtual Hardware using GitHub Actions, corresponding definitions (non-WiFi) are automatically updated in the code with values stored in \ref aws_mqtt_gh_secrets.

## Setup of CI Test

To build and run this application program with a GitHub Actions workflow the following steps are required. For details refer to [Run AMI with GitHub Actions](https://arm-software.github.io/AVH/main/infrastructure/html/run_ami_github.html).

1. **Amazon Web Service (AWS) account** with:
    - Amazon EC2 (elastic cloud) access
    - Amazon S3 (storage) access
    - Registration to access AVH Amazon Machine Image [AVH AMI](https://aws.amazon.com/marketplace/search/results?searchTerms=Arm+Virtual+Hardware)
    - User role setup for scripted API access

2. **GitHub**:
    - Fork this repository with at least _Write_ access rights
    - Store the AWS account configuration (obtained in step 1) as values of \ref aws_mqtt_gh_secrets "AWS Access GitHub Secrets" in the forked repository.
    - Store the commissioning parameters (obtained in \ref aws_iot_thing) as values of \ref aws_mqtt_gh_secrets "IoT Cloud Access GitHub Secrets" in the forked repository.

### GitHub Secrets {#aws_mqtt_gh_secrets}

The following (secret) configuration values need to be added to the repositories as [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

Secret Name                    | Description
:------------------------------|:--------------------
**AWS Access**                 | **Settings and credentials required to acces AWS EC2 and S3 services**
`AWS_IAM_PROFILE`              | The [IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html) to be used for AWS access.
`AWS_ACCESS_KEY_ID`<br>`AWS_SECRET_ACCESS_KEY`      | [Access key pair](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for the AWS account (as IAM user) that shall be used by the CI workflow for AWS access.
`AWS_S3_BUCKET_NAME`           | The name of the S3 storage bucket to be used for data exchange between GitHub and AWS AMI.
`AWS_DEFAULT_REGION`           | The data center region the AVH AMI will be run on. For example `eu-west-1`.
`AWS_SECURITY_GROUP_ID`        | The id of the [VPC security group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) to add the EC2 instance to. Shall have format `sg-xxxxxxxx`.
`AWS_SUBNET_ID`                | The id of the [VPC subnet](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#view-subnet) to connect the EC2 instance to. Shall have format `subnet-xxxxxxxx`.
**IoT Cloud Access**           | **Settings and credentials required to connect an [AWS IoT Thing](https://github.com/MDK-Packs/Documentation/tree/master/AWS_Thing)**
`CLIENT_CERTIFICATE_PEM`       | Client (device) certificate
`CLIENT_PRIVATE_KEY_PEM`       | Client (device) private key
`IOT_THING_NAME`               | Client  (device) name
`MQTT_BROKER_ENDPOINT`         | MQTT broker host name
