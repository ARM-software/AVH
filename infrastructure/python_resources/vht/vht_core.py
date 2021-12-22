from botocore.exceptions import ClientError
from botocore.exceptions import WaiterError
from vht import vht_utils

import boto3
import os
import logging
import sys
import time

class VhtCore():
    def __init__(self):
        self.vht_utils = vht_utils.VhtUtils()
        self.vht_utils.is_aws_credentials_present()

        logging.info('vht_core:Creating EC2 client...')
        self.ec2_client = boto3.client('ec2')

        logging.info('vht_core:Creating SSM client...')
        self.ssm_client = boto3.client('ssm')

        logging.info('vht_core:Creating S3 client...')
        self.s3_client = boto3.client('s3')

    def create_ec2_instance(self, **kwargs):
        """
        Create a new EC2 Instance

        Parameters
        ----------
        **kwargs: Keyword args associated with run-instances API doc e.g.:
            --create-ec2-instance
                ImageId=ami-0c5eeabe11f3a2685 \
                InstanceType=t2.micro \
                MaxCount=1 \
                MinCount=1 \
                SecurityGroupIds=['sg-04022e04e91197ce3'] \
                SubnetId=subnet-00455495b268076f0  \
                IamInstanceProfile="{'Name': 'Proj-s3-orta-vht-role'}"

        Returns
        -------
        string
            Instance ID

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.run_instances
        """
        instance_id = ''

        logging.debug('vht_core:DryRun=True to test for permission check')
        logging.debug('vht_core:create_ec2_instance:kwargs:{}'.format(kwargs))

        try:
            self.ec2_client.run_instances(**kwargs, DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        logging.info('vht_core:Creating EC2 instance...')
        logging.debug('vht_core:kwargs = {}'.format(kwargs))
        response = self.ec2_client.run_instances(**kwargs)
        logging.debug(response)

        instance_id = response['Instances'][0]['InstanceId']
        assert isinstance(instance_id, str)
        self.wait_ec2_running(instance_id)
        self.wait_ec2_status_ok(instance_id)

        return instance_id

    def delete_s3_object(self, s3_bucket_name, key):
        """
        Delete S3 Object

        Parameters
        ----------
        String
            s3_bucket_name
            key (s3 path)

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
        """

        logging.info("vht_core:Delete S3 Object from S3 Bucket {}, Key {}".format(s3_bucket_name, key))
        response = self.s3_client.delete_object(
            Bucket=s3_bucket_name,
            Key=key
        )
        logging.debug(response)

    def download_s3_file(self, s3_bucket_name, key, filename):
        """
        Download S3 File

        Parameters
        ----------
        String
            s3_bucket_name
            key (s3 path)
            filename (destination local path)

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file
        """

        logging.info("vht_core:Download S3 File")
        s3 = boto3.resource('s3')
        try:
            s3.meta.client.download_file(s3_bucket_name, key, filename)
        except ClientError as e:
            if 'HeadObject operation: Not Found' in str(e):
                print("Key '{}' not found on S3 Bucket Name = '{}'".format(key, s3_bucket_name))
            else:
                print("The error {} happens for Key={} and S3_bucket_name={}".format(e, key, s3_bucket_name))
            exit(-1)


    def get_ami_id(self, vht_version):
        """
        Get the VHT AMI ID for the region
        The VHT AMI ID changes for each AWS region

        Parameters
        ----------
        String
            vht_version (VHT AMI Version)

        Return
        ----------
        String
            VHT AMI ID

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

        """
        response = self.ec2_client.describe_images(
            Filters=[
                {
                    'Name': 'name',
                    'Values': [
                        'ArmVirtualHardware-{}*'.format(vht_version),
                    ]
                },
            ]
        )

        logging.debug("vht_core:get_vht_ami_id_by_version:{}".format(response))
        ami_id = response['Images'][0]['ImageId']
        return ami_id

    def get_ec2_instance_state(self, instance_id):
        """
        Get EC2 Instance State

        Parameters
        ----------
        String
            instance_id (e.g. i-02d395a021e6d9d17)

        Return
        ----------
        String
            EC2 Instance State ('pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped')

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
        """
        response = self.ec2_client.describe_instances(
            InstanceIds=[
                instance_id,
            ],
        )

        logging.debug("vht_core:get_ec2_instance_state: {}".format(response))
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
        logging.info("vht_core:The EC2 instance state is {}...".format(instance_state))
        return instance_state

    def get_s3_file_content(self, s3_bucket_name, key):
        """
        Get S3 File Content

        Parameters
        ----------
        String
            s3_bucket_name
            key (s3 path)

        Return
        ----------
        String
            S3 File Content

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
        """
        s3 = boto3.resource('s3')
        content = ''
        try:
            obj = s3.Object(s3_bucket_name, key)
            content = obj.get()['Body'].read().decode('utf-8')
        except self.s3_client.exceptions.NoSuchKey:
            logging.info("vht_core:Key '{}' not found on S3 bucket '{}'".format(key, s3_bucket_name))
            return ''

        return content

    def get_s3_ssm_command_id_key(self, instance_id, command_id, s3_keyprefix, output_type):
        """
        Get calculated S3 SSM Command ID Output Key

        Parameters
        ----------
        String
            instance_id (Instance ID)
            command_id (Command ID)
            s3_keyprefix (S3 Key Prefix used)
            output_type (`stderr` or `stdout`)

        Return
        ----------
        String
            S3 SSM Command ID Key
        """
        return "{}/{}/{}/awsrunShellScript/0.awsrunShellScript/{}".format(
            s3_keyprefix,
            command_id,
            instance_id,
            output_type
        )

    def get_ssm_command_id_status(self, command_id):
        """
        Get the Status for a specific command ID and Instance ID.

        Parameters
        ----------
        String
            command_id (Command ID)

        Return
        ----------
        String
            Command ID Status

        More
        ----------
        API Definition:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_commands
        """
        response = self.ssm_client.list_commands(
            CommandId=command_id
        )

        logging.debug("vht_core:get_ssm_command_id_status:" + str(response))
        command_id_status = response['Commands'][0]['Status']
        logging.info("vht_core:The command_id {} status is {}...".format(command_id, command_id_status))
        return command_id_status

    def get_ssm_command_id_status_details(self, instance_id, command_id):
        """
        Get the Status details for a specific command ID and Instance ID.

        Parameters
        ----------
        String
            instance_id (Instance ID)
            command_id (Command ID)

        Return
        ----------
        String
            Command ID Status Details

        More
        ----------
        API Definition:
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_command_invocation
        """

        response = self.ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id
        )
        return response['StatusDetails']

    def get_ssm_command_id_stdout_url(self, command_id, instance_id):
        """
        Get the stdout output URL for a specific command ID and Instance ID.

        Parameters
        ----------
        String
            command_id (Command ID)
            instance_id (Instance ID)

        Return
        ----------
        String
            Command ID Stdout URL

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_command_invocations
        """
        response = self.ssm_client.list_command_invocations(
            CommandId=command_id,
            InstanceId=instance_id
        )
        return response['CommandInvocations'][0]['StandardOutputUrl']

    def get_ssm_command_id_stderr_url(self, command_id, instance_id):
        """
        Get the stderr output URL for a specific command ID and Instance ID.

        Parameters
        ----------
        String
            command_id (Command ID)
            instance_id (Instance ID)

        Return
        ----------
        String
            Command ID Stderr URL

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.list_command_invocations
        """
        response = self.ssm_client.list_command_invocations(
            CommandId=command_id,
            InstanceId=instance_id
        )
        return response['CommandInvocations'][0]['StandardErrorUrl']

    def upload_s3_file(self, s3_bucket_name, filename, key):
        """
        Upload a file to a S3 Bucket

        Parameters
        ----------
        String
            s3_bucket_name (S3 Bucket Name)
            filename (Local Filename Path)
            Key (Filepath to be stored on S3 Bucket)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
        """

        logging.info("vht_core:Upload File {} to S3 Bucket {}, Key {}".format(filename, s3_bucket_name, key))
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(filename, s3_bucket_name, key)

    def send_ssm_shell_command(self,
                               instance_id,
                               command_list,
                               s3_bucket_name,
                               s3_keyprefix='',
                               working_dir='/',
                               return_type='all',
                               timeoutSeconds=600):
        """
        Send SSM Shell Commands to a EC2 Instance

        Parameters
        ----------
        String
            instance_id (Instance ID)
            command_list (List of commands to be executed on the instance_id)
            s3_bucket_name (S3 Bucket where the stdout and stderr logs will be stored)
            s3_keyprefix (Desided prefix location for the logs - Default: '')
            working_dir (Working directory - Default: '/')
            return_type (
                Method return types:
                    `all`: Return as a dict: 'CommandId', 'CommandIdStatus', 'CommandList', 'StdOut', 'StdErr' - Default
                    `command_id`: Return only the `command_id` as a String
            )
            timeoutSeconds (Command Timeout in Seconds - Default: 600)

        Return
        ----------
        Dict
            if return_type == `all` (Default):
                'CommandId', 'CommandIdStatus', 'CommandList', 'StdOut', 'StdErr'
        String
            if return_type == `command_id`:
                command_id

        More
        ----------
        TODO: Use **kwargs

        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.send_command
            https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-plugins.html#aws-runShellScript
        """

        command_id = ''
        command_id_status = ''
        stdout_key = ''
        stdout_str = ''
        stderr_key = ''
        stderr_str = ''

        try:
            response = self.ssm_client.send_command(
                InstanceIds=[
                    instance_id,
                ],
                DocumentName='AWS-RunShellScript',
                Parameters={
                    'workingDirectory': [
                        working_dir,
                    ],
                    'commands': [
                        command_list,
                    ]
                },
                OutputS3BucketName=s3_bucket_name,
                OutputS3KeyPrefix=s3_keyprefix,
                TimeoutSeconds=timeoutSeconds,
            )
        except ClientError as e:
            print(e)
            exit(-1)

        command_id = response['Command']['CommandId']
        logging.info("vht_core:command_id = {}".format(command_id))

        # We need a little bit of time to wait for a command
        time.sleep(2)

        logging.info("vht_core:Waiting command id {} to finish".format(command_id))
        self.wait_ssm_command_finished(
            instance_id,
            command_id
        )

        logging.info("vht_core:Get command id {} status".format(command_id))
        command_id_status = self.get_ssm_command_id_status(
            command_id
        )
        logging.info("vht_core:Command id status = {}".format(command_id_status))

        stdout_key = self.get_s3_ssm_command_id_key(
            instance_id,
            command_id,
            s3_keyprefix,
            'stdout'
        )
        stdout_str = self.get_s3_file_content(
            s3_bucket_name,
            stdout_key
        )

        if (command_id_status != 'Success'):
            stderr_key = self.get_s3_ssm_command_id_key(
                instance_id,
                command_id,
                s3_keyprefix,
                'stderr'
            )
            stderr_str = self.get_s3_file_content(
                s3_bucket_name,
                stderr_key
            )

        if return_type == 'all':
            return {
                'CommandId' : command_id,
                'CommandIdStatus' : command_id_status,
                'CommandList' : command_list,
                'StdOut' : stdout_str,
                'StdErr': stderr_str
            }
        elif return_type == 'command_id':
            return command_id
        else:
            raise AttributeError("Output type '{}' invalid. See docs.".format(return_type))

    def start_ec2_instance(self, instance_id):
        """
        Start an Instance and wait it to become running and status OK

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances
        """
        logging.info("vht_core:Starting EC2 instance {}".format(instance_id))
        response = self.ec2_client.start_instances(
            InstanceIds=[
                instance_id,
            ]
        )
        self.wait_ec2_running(instance_id)
        self.wait_ec2_status_ok(instance_id)

    def stop_ec2_instance(self, instance_id):
        """
        Stop an Instance and wait it becomes stopped.

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances
        """
        logging.info("vht_core:Stopping EC2 instance {}".format(instance_id))
        response = self.ec2_client.stop_instances(
            InstanceIds=[
                instance_id,
            ]
        )
        self.wait_ec2_stopped(instance_id)

    def wait_ec2_status_ok(self, instance_id):
        """
        Wait an EC2 instance to have a Status == OK.

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.InstanceStatusOk
        """
        logging.info("vht_core:Waiting until EC2 instance id {} Status Ok...".format(instance_id))
        waiter = self.ec2_client.get_waiter('instance_status_ok')
        waiter.wait(
            InstanceIds=[
                instance_id,
            ]
        )

    def wait_ec2_running(self, instance_id):
        """
        Wait an EC2 instance to be running

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.InstanceRunning
        """
        logging.info("vht_core:Waiting until EC2 instance id {} is running...".format(instance_id))
        waiter = self.ec2_client.get_waiter('instance_running')
        waiter.wait(
            InstanceIds=[
                instance_id,
            ]
        )

    def wait_ec2_stopped(self, instance_id):
        """
        Wait an EC2 instance to stop

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_stopped
        """
        logging.info("vht_core:Waiting until EC2 instance id {} is stopped...".format(instance_id))
        instance = boto3.resource('ec2').Instance(instance_id)
        instance.wait_until_stopped()

    def wait_ec2_terminated(self, instance_id):
        """
        Wait an EC2 instance to terminate

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_terminated
        """
        logging.info("vht_core:Waiting until EC2 instance id {} is terminated...".format(instance_id))
        instance = boto3.resource('ec2').Instance(instance_id)
        instance.wait_until_terminated()

    def wait_s3_object_exists(self, s3_bucket_name, key, delay=5, max_attempts=120):
        """
        Wait an S3 Object to exists

        Parameters
        ----------
        String
            s3_bucket_name (S3 Bucket Name)
            key (S3 Keypath)
            delay (Retry delay in seconds - Default: 5)
            max_attemps (Max retry - Default: 120)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Waiter.ObjectExists
        """
        waiter = self.s3_client.get_waiter('object_exists')
        waiter.wait(
            Bucket=s3_bucket_name,
            Key=key,
            WaiterConfig={
                'Delay': delay,
                'MaxAttempts': max_attempts
            }
        )

    def wait_ssm_command_finished(self, instance_id, command_id, delay=5, max_attempts=120):
        """
        Wait the SSM command to reach a terminal status.
        Parameters
        ----------
        String
            instance_id (Instance ID)
            command_id (Command ID)
            delay (Retry delay in seconds - Default: 5)
            max_attemps (Max retry - Default: 120)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Waiter.CommandExecuted
        """
        waiter = self.ssm_client.get_waiter('command_executed')
        try:
            waiter.wait(
                CommandId=command_id,
                InstanceId=instance_id,
                WaiterConfig={
                    'Delay': delay,
                    'MaxAttempts': max_attempts
                }
            )
        except WaiterError:
            if "Failed" in str(WaiterError):
                logging.info("vht_core:Failed status found while wainting for command id")

    def terminate_ec2_instance(self, instance_id):
        """
        Terminate an Instance and wait it to terminated.

        Parameters
        ----------
        String
            instance_id (Instance ID)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.terminate_instances
        """
        logging.debug('vht_core:terminate_ec2_instance: DryRun=True to test for permission check')
        try:
            self.ec2_client.terminate_instances(
                InstanceIds=[
                    instance_id,
                ],
                DryRun=True
            )
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        logging.info('vht_core:Terminating EC2 instance...')
        response = self.ec2_client.terminate_instances(
            InstanceIds=[
                instance_id
            ]
        )
        self.wait_ec2_terminated(instance_id)
        return response
