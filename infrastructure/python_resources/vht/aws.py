import logging
import os
import sys
import time
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import WaiterError

class AWSClient():
    """
    VHT AWS Backend

    This backend runs in your Amazon account:
     * Creates/starts/setup a [new] VHT EC2 instance.
     * Run VHT-related commands.
     * Get the outputs
     * Terminates/Stops the VHT EC2 instance.

    The AWS credentials key is expected as envs. See _is_aws_credentials_present method.
    Some AWS-related info is expected as envs. See _setup.
    """
    def __init__(self):
        logging.info('aws:Creating EC2 client...')
        self.ec2_client = boto3.client('ec2')

        logging.info('aws:Creating SSM client...')
        self.ssm_client = boto3.client('ssm')

        logging.info('aws:Creating S3 client...')
        self.s3_client = boto3.client('s3')

        logging.info('aws:Creating S3 resource...')
        self.s3_resource = boto3.resource('s3')

        self._is_aws_credentials_present()
        self._setup()

    def __repr__(self):
        return (
            f"ami_id={self.ami_id},"
            f"ami_version={self.ami_version},"
            f"gh_workspace={self.gh_workspace},"
            f"iam_profile={self.iam_profile},"
            f"instance_id={self.instance_id},"
            f"instance_type={self.instance_type},"
            f"key_name={self.key_name},"
            f"s3_bucket_name={self.s3_bucket_name},"
            f"security_group_id={self.security_group_id},"
            f"subnet_id={self.subnet_id},"
            f"vht_in_filename={self.vht_in_filename},"
            f"vht_out_filename={self.vht_out_filename},"
            f"terminate_ec2_instance={self.terminate_ec2_instance}"
        )

    def _is_aws_credentials_present(self):
        """
            Verifies presence of AWS Credentias as Environment Variables.
            AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are mandatory
            AWS_SESSION_TOKEN is optional for IAM User credentials.
        """
        if os.environ.get('AWS_ACCESS_KEY_ID') is None:
            logging.info("aws:AWS_ACCESS_KEY_ID environment variable not present!")
            sys.exit(1)
        else:
            logging.debug('aws:AWS_ACCESS_KEY_ID present!')

        if os.environ.get('AWS_SECRET_ACCESS_KEY') is None:
            logging.info("aws:AWS_SECRET_ACCESS_KEY environment variable not present!")
            sys.exit(1)
        else:
            logging.debug('aws:AWS_SECRET_ACCESS_KEY present!')

        if os.environ.get('AWS_SESSION_TOKEN') is None:
            logging.debug('aws:AWS_SESSION_TOKEN environment variable not present!')
            logging.debug('aws:It is expected for an IAM User')
        else:
            logging.debug('aws:AWS_SESSION_TOKEN present!')

    def _setup(self):
        """
            Setup AWS object by collecting env vars & preparing AWS instance
        """
        # Initializing None all VHT related variables
        logging.info("aws:setting up aws backend")
        self.ami_id = None
        self.ami_version = None
        self.gh_workspace = None
        self.iam_profile = None
        self.instance_id = None
        self.instance_type = None
        self.key_name = None
        self.s3_bucket_name = None
        self.security_group_id = None
        self.subnet_id = None
        self.terminate_ec2_instance = None
        self.vht_in_filename = 'vht.tar'
        self.vht_out_filename = 'out.tar'

        # instance_id
        self.instance_id = None if os.environ.get('instance_id') in (None, '') else os.environ.get('instance_id')
        # ami_id & ami_version

        # EC2-related info is not needed if an instance is already created
        if self.instance_id is None:
            self.ami_id = os.environ.get('ami_id')
            self.ami_version = os.environ.get('ami_version')
            if not self.ami_id and not self.ami_version:
                logging.error("Either `ami_id` or `ami_version` should be presented as env var!")
                sys.exit(-1)
            if not self.ami_id:
                self.ami_id = self.get_image_id()
            if self.ami_id == '':
                logging.error('AMI ID should not be blank. You should inform either vht_ami_id or vht_ami_version')
                sys.exit(-1)

            # Optional: key_name
            self.key_name = os.environ.get('key_name')

            envs = [
                'iam_profile',
                'instance_type',
                'security_group_id',
                'subnet_id',
                'terminate_ec2_instance'
            ]
            for env_ in envs:
                if os.environ.get(env_) in (None, ''):
                    logging.error(f"aws:environment variable `{env_}` needs to be present!")
                    sys.exit(-1)
            self.iam_profile = os.environ.get('iam_profile')
            self.instance_type = os.environ.get('instance_type')
            self.security_group_id = os.environ.get('security_group_id')
            self.subnet_id = os.environ.get('subnet_id')
            self.terminate_ec2_instance = os.environ.get('terminate_ec2_instance')
            if self.terminate_ec2_instance.lower() == 'true':
                self.terminate_ec2_instance = True
            else:
                self.terminate_ec2_instance = False

        # s3_keyprefix
        self.s3_keyprefix = 'ssm' if os.environ.get('s3_keyprefix') in (None, '') else os.environ.get('s3_keyprefix')

        # check mandatory env vars
        envs = [
            'gh_workspace',
            's3_bucket_name',
        ]
        for env_ in envs:
            if os.environ.get(env_) in (None, ''):
                logging.error(f"vht_github_action:environment variable `{env_}` needs to be present!")
                sys.exit(-1)

        self.gh_workspace = os.environ.get('gh_workspace')
        self.s3_bucket_name = os.environ.get('s3_bucket_name')
        self.vht_in = f"{self.gh_workspace}/{self.vht_in_filename}"
        self.vht_out = f"{self.gh_workspace}/{self.vht_out_filename}"

        logging.info(f"aws:aws__repr__:{self.__repr__()}")

    def create_instance(self):
        """
            Create an EC2 Instance. It is a wrapper for create_ec2_instance.
            If key_name is present, it creates a instance with the selected private key.

            This is a mandatory VHT backend method.
        """
        if self.key_name is None or self.key_name == '':
            self.instance_id = self.create_ec2_instance(
                ImageId=self.ami_id,
                InstanceType=self.instance_type,
                MaxCount=1,
                MinCount=1,
                SecurityGroupIds=[self.security_group_id],
                SubnetId=self.subnet_id,
                TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'VHT_CLI','Value': 'true',}]}],
                IamInstanceProfile={'Name': self.iam_profile}
            )
        else:
            self.instance_id = self.create_ec2_instance(
                ImageId=self.ami_id,
                InstanceType=self.instance_type,
                MaxCount=1,
                MinCount=1,
                KeyName=self.key_name,
                SecurityGroupIds=[self.security_group_id],
                SubnetId=self.subnet_id,
                TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'VHT_CLI','Value': 'true',}]}],
                IamInstanceProfile={'Name': self.iam_profile}
            )

        return self.instance_id

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
        logging.debug('aws:DryRun=True to test for permission check')
        logging.debug(f"aws:create_ec2_instance:kwargs:{kwargs}")

        try:
            self.ec2_client.run_instances(**kwargs, DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        logging.info('aws:Creating EC2 instance...')
        logging.debug(f"aws:kwargs={kwargs}")
        response = self.ec2_client.run_instances(**kwargs)
        logging.debug(response)

        self.instance_id = response['Instances'][0]['InstanceId']
        assert isinstance(self.instance_id, str)
        self.wait_ec2_running()
        self.wait_ec2_status_ok()

        return self.instance_id

    def delete_file_from_cloud(self, key):
        """
        Delete S3 Object

        Parameters
        ----------
        String
            key (s3 path)

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object

        This is a mandatory VHT backend method.
        """

        logging.info(f"aws:Delete S3 Object from S3 Bucket {self.s3_bucket_name}, Key {key}")
        response = self.s3_client.delete_object(
            Bucket=self.s3_bucket_name,
            Key=key
        )
        logging.debug(response)

    def download_file_from_cloud(self, filename, key):
        """
        Download S3 File

        Parameters
        ----------
        String
            filename (destination local path)
            key (s3 path)

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file

        This is a mandatory VHT backend method.
        """

        logging.info("aws:Download S3 File")
        try:
            logging.info(f"Downloading S3 file from bucket `{self.s3_bucket_name}`, key `{key}`, filename `{filename}`")
            self.s3_client.download_file(self.s3_bucket_name, key, filename)
        except ClientError as e:
            if 'HeadObject operation: Not Found' in str(e):
                print(f"Key '{key}' not found on S3 Bucket Name = '{self.s3_bucket_name}'")
            else:
                print(f"The error {e} happens for Key={key} and S3_bucket_name={self.s3_bucket_name}")
            exit(-1)

    def get_image_id(self):
        """
        Get the VHT AMI ID for the region
        The VHT AMI ID changes for each AWS region

        Return
        ----------
        String
            VHT AMI ID

        More
        ----
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images

        This is a mandatory VHT backend method.
        """
        assert self.ami_version is not None, \
            "The variable `ami_version` is not present"
        response = self.ec2_client.describe_images(
            Filters=[
                {
                    'Name': 'name',
                    'Values': [
                        f"ArmVirtualHardware-{self.ami_version}*"
                    ]
                },
            ]
        )

        logging.debug(f"aws:get_vht_ami_id_by_version:{response}")
        self.ami_id = response['Images'][0]['ImageId']
        return self.ami_id

    def get_instance_id(self):
        """
        Return EC2 Instance ID.
        This is a mandatory VHT backend method.
        """
        return self.instance_id

    def get_instance_state(self):
        """
        Get EC2 Instance State

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
                self.instance_id,
            ],
        )

        logging.debug(f"aws:get_instance_state: {response}")
        self.instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
        logging.info(f"aws:The EC2 instance state is {self.instance_state}...")
        return self.instance_state

    def get_s3_file_content(self, key):
        """
        Get S3 File Content

        Parameters
        ----------
        String
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
        content = ''
        try:
            content = self.s3_resource.Object(self.s3_bucket_name, key).get()['Body'].read().decode('utf-8')
        except self.s3_client.exceptions.NoSuchKey:
            logging.info(f"aws:Key '{key}' not found on S3 bucket '{self.s3_bucket_name}'")
            return ''

        return content

    def get_s3_ssm_command_id_key(self, command_id, output_type):
        """
        Get calculated S3 SSM Command ID Output Key

        Parameters
        ----------
        String
            command_id (Command ID)
            output_type (`stderr` or `stdout`)

        Return
        ----------
        String
            S3 SSM Command ID Key
        """
        return f"{self.s3_keyprefix}/{command_id}/{self.instance_id}/awsrunShellScript/0.awsrunShellScript/{output_type}"

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

        logging.debug(f"aws:get_ssm_command_id_status:{response}")
        command_id_status = response['Commands'][0]['Status']
        logging.info(f"aws:The command_id {command_id} status is {command_id_status}...")
        return command_id_status

    def get_ssm_command_id_status_details(self, command_id):
        """
        Get the Status details for a specific command ID and Instance ID.

        Parameters
        ----------
        String
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
            InstanceId=self.instance_id
        )
        logging.debug(f"aws:get_ssm_command_id_status_details:{response}")
        logging.info(f"aws:The command_id {command_id} status details is {response['StatusDetails']}...")
        return response['StatusDetails']

    def get_ssm_command_id_stdout_url(self, command_id):
        """
        Get the stdout output URL for a specific command ID and Instance ID.

        Parameters
        ----------
        String
            command_id (Command ID)

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
            InstanceId=self.instance_id
        )
        logging.debug(f"aws:get_ssm_command_id_stdout_url:{response}")
        return response['CommandInvocations'][0]['StandardOutputUrl']

    def get_ssm_command_id_stderr_url(self, command_id):
        """
        Get the stderr output URL for a specific command ID and Instance ID.

        Parameters
        ----------
        String
            command_id (Command ID)

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
            InstanceId=self.instance_id
        )
        logging.debug(f"aws:get_ssm_command_id_stderr_url:{response}")
        return response['CommandInvocations'][0]['StandardErrorUrl']

    def get_process_vht_commands(self):
        """
            VHT commands to be executed on a remote EC2 instance.

            This is a mandatory VHT backend method.
        """
        return [
            "runuser -l ubuntu -c 'cat ~/.bashrc | grep export > vars'",
            "rm -rf /home/ubuntu/vhtagent",
            "rm -rf /home/ubuntu/vhtwork",
            "runuser -l ubuntu -c 'mkdir vhtagent'",
            "runuser -l ubuntu -c 'mkdir vhtwork'",
            "runuser -l ubuntu -c 'mkdir -p /home/ubuntu/packs/.Web'",
            "runuser -l ubuntu -c 'cd /home/ubuntu/vhtagent && wget https://raw.githubusercontent.com/ARM-software/VHT-AMI/master/agent/process_vht.py'",
            "runuser -l ubuntu -c 'wget -N https://www.keil.com/pack/index.pidx -O /home/ubuntu/packs/.Web/index.pidx'",
            "apt update",
            "apt install awscli -y",
            f"runuser -l ubuntu -c 'aws s3 cp s3://{self.s3_bucket_name}/{self.vht_in_filename} /home/ubuntu/vhtwork/{self.vht_in_filename}'",
            "runuser -l ubuntu -c 'source vars && python3 /home/ubuntu/vhtagent/process_vht.py'",
            f"runuser -l ubuntu -c 'aws s3 cp /home/ubuntu/vhtwork/{self.vht_out_filename} s3://{self.s3_bucket_name}/{self.vht_out_filename}'"
        ]

    def run(self, delete_output_file_from_cloud=True):
        if self.instance_id in ('', None):
            self.create_instance()
        else:
            logging.info(f"aws:EC2 Instance {self.instance_id} provided!")
            self.start_instance()

        self.upload_file_to_cloud(self.vht_in, self.vht_in_filename)
        self.send_remote_command_batch(self.get_process_vht_commands(), working_dir='/home/ubuntu')

        logging.info("aws:Download S3 File to the GitHub Runner...")
        self.download_file_from_cloud(
            filename=self.vht_out,
            key=self.vht_out_filename
        )

        if delete_output_file_from_cloud:
            logging.info("aws:Delete S3 Out.tar object from the S3 Bucket...")
            self.delete_file_from_cloud(key=self.vht_out_filename)

        self.teardown()

    def upload_file_to_cloud(self, filename, key):
        """
        Upload a file to a S3 Bucket

        Parameters
        ----------
        String
            filename (Local Filename Path)
            Key (Filepath to be stored on S3 Bucket)

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file
        """

        logging.info(f"aws:Upload File {filename} to S3 Bucket {self.s3_bucket_name}, Key {key}")
        self.s3_resource.meta.client.upload_file(filename, self.s3_bucket_name, key)

    def send_remote_command(self, command_list, working_dir, fail_if_unsuccess = True):
        """
        Send a remote command to an EC2 Instance.

        Parameters
        ----------
        List
            command_list (List of commands)
        String
            working_dir (Directory where the remote command will be executed)
        Boolean
            fail_if_unsuccess (Fail the method in case the command failed)

        Return
        ------
            JSON data from send_ssm_shell_command method.

        This is a mandatory VHT backend method.
        """
        logging.info(f"vht: command_list = {command_list}")
        response = self.send_ssm_shell_command(
            command_list=command_list,
            working_dir=working_dir
        )

        for i in response.keys():
            logging.info(f"vht:{i} = {response[i].strip()}")
        if response['CommandIdStatus'] != 'Success' and fail_if_unsuccess:
            logging.error(f"Command {command_list} failed")
            logging.error("Tearing down the EC2 instance!")
            self.teardown()
            sys.exit(-1)

        return response

    def send_remote_command_batch(self, command_list, working_dir, fail_if_unsuccess = True):
        """
        Send batch of remote commands to an EC2 Instance.

        Parameters
        ----------
        List
            command_list (List of List of commands)
        String
            working_dir (Directory where the remote command will be executed)
        Boolean
            fail_if_unsuccess (Fail the method in case the command failed - Default: True)

        Return
        ------
            JSON data from send_ssm_shell_command method.

        This is a mandatory VHT backend method.
        """
        logging.info(f"vht: command_list = {command_list}")
        all_responses = []

        for command in command_list:
            all_responses.append(
                self.send_remote_command(
                    command_list=command,
                    working_dir=working_dir,
                    fail_if_unsuccess=fail_if_unsuccess
                )
            )
        logging.debug(f"vht: all_responses = {all_responses}")
        return all_responses

    def send_ssm_shell_command(self,
                               command_list,
                               working_dir='/',
                               return_type='all',
                               timeout_seconds=600):
        """
        Send SSM Shell Commands to a EC2 Instance

        Parameters
        ----------
        String
            command_list (List of commands to be executed on the instance_id)
            working_dir (Working directory - Default: '/')
            return_type (
                Method return types:
                    `all`: Return as a dict: 'CommandId', 'CommandIdStatus', 'CommandList', 'StdOut', 'StdErr' - Default
                    `command_id`: Return only the `command_id` as a String
            )
            timeout_seconds (Command Timeout in Seconds - Default: 600)

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
                    self.instance_id
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
                OutputS3BucketName=self.s3_bucket_name,
                OutputS3KeyPrefix=self.s3_keyprefix,
                TimeoutSeconds=timeout_seconds,
            )
        except ClientError as e:
            print(e)
            exit(-1)

        logging.debug(f"aws:send_ssm_shell_command:{response}")
        command_id = response['Command']['CommandId']
        logging.info(f"aws:command_id = {command_id}")

        # We need a little bit of time to wait for a command
        time.sleep(2)

        logging.info(f"aws:Waiting command id {command_id} to finish")
        self.wait_ssm_command_finished(command_id)

        logging.info(f"aws:Get command id {command_id} status")
        command_id_status = self.get_ssm_command_id_status(command_id)
        logging.info(f"aws:Command id status = {command_id_status}")

        stdout_key = self.get_s3_ssm_command_id_key(command_id, 'stdout')
        stdout_str = self.get_s3_file_content(stdout_key)

        if command_id_status != 'Success':
            stderr_key = self.get_s3_ssm_command_id_key(command_id, 'stderr')
            stderr_str = self.get_s3_file_content(stderr_key)

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
            raise AttributeError(f"Output type '{return_type}' invalid. See docs.")

    def start_instance(self):
        """
        Start an Instance and wait it to become running and status OK

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.start_instances

        This is a mandatory VHT backend method.
        """
        assert self.instance_id not in ('', None), "instance_id should be provided!"

        logging.info(f"aws:Starting EC2 instance {self.instance_id}")
        response = self.ec2_client.start_instances(
            InstanceIds=[
                self.instance_id,
            ]
        )
        logging.debug(f"aws:start_ec2_instance:{response}")
        self.wait_ec2_running()
        self.wait_ec2_status_ok()

        return self.instance_id

    def stop_instance(self):
        """
        Stop an Instance and wait it becomes stopped.

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.stop_instances

        This is a mandatory VHT backend method.
        """
        logging.info(f"aws:Stopping EC2 instance {self.instance_id}")
        response = self.ec2_client.stop_instances(
            InstanceIds=[
                self.instance_id
            ]
        )
        logging.debug(f"aws:stop_instance:{response}")
        self.wait_ec2_stopped()

        return self.instance_id

    def wait_ec2_status_ok(self):
        """
        Wait an EC2 instance to have a Status == OK.

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.InstanceStatusOk
        """
        logging.info(f"aws:Waiting until EC2 instance id {self.instance_id} Status Ok...")
        waiter = self.ec2_client.get_waiter('instance_status_ok')
        waiter.wait(
            InstanceIds=[
                self.instance_id
            ]
        )

    def wait_ec2_running(self):
        """
        Wait an EC2 instance to be running

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Waiter.InstanceRunning
        """
        logging.info(f"aws:Waiting until EC2 instance id {self.instance_id} is running...")
        waiter = self.ec2_client.get_waiter('instance_running')
        waiter.wait(
            InstanceIds=[
                self.instance_id
            ]
        )

    def wait_ec2_stopped(self):
        """
        Wait an EC2 instance to stop

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_stopped
        """
        logging.info(f"aws:Waiting until EC2 instance id {self.instance_id} is stopped...")
        instance = boto3.resource('ec2').Instance(self.instance_id)
        instance.wait_until_stopped()

    def wait_ec2_terminated(self):
        """
        Wait an EC2 instance to terminate

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.wait_until_terminated
        """
        logging.info(f"aws:Waiting until EC2 instance id {self.instance_id} is terminated...")
        instance = boto3.resource('ec2').Instance(self.instance_id)
        instance.wait_until_terminated()

    def wait_s3_object_exists(self, key, delay=5, max_attempts=120):
        """
        Wait an S3 Object to exists

        Parameters
        ----------
        String
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
            Bucket=self.s3_bucket_name,
            Key=key,
            WaiterConfig={
                'Delay': delay,
                'MaxAttempts': max_attempts
            }
        )

    def teardown(self):
        """
            Teardown
        """
        # if terminate_instance is True Terminate Otherwise Stop instance
        if self.terminate_ec2_instance:
            self.terminate_instance()
        else:
            self.stop_instance()

    def wait_ssm_command_finished(self, command_id, delay=5, max_attempts=120):
        """
        Wait the SSM command to reach a terminal status.
        Parameters
        ----------
        String
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
                InstanceId=self.instance_id,
                WaiterConfig={
                    'Delay': delay,
                    'MaxAttempts': max_attempts
                }
            )
        except WaiterError:
            if "Failed" in str(WaiterError):
                logging.info("aws:Failed status found while wainting for command id")

    def terminate_instance(self):
        """
        Terminate an Instance and wait it to terminated.

        More
        ----------
        API Definition
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.terminate_instances

        This is a mandatory VHT backend method.
        """
        logging.debug('aws:terminate_instance: DryRun=True to test for permission check')
        try:
            self.ec2_client.terminate_instances(
                InstanceIds=[
                    self.instance_id
                ],
                DryRun=True
            )
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        logging.info('aws:Terminating EC2 instance...')
        response = self.ec2_client.terminate_instances(
            InstanceIds=[
                self.instance_id
            ]
        )
        logging.debug(f"aws:terminate_instance:{response}")
        self.wait_ec2_terminated()
        return response
