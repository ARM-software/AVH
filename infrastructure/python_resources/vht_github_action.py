from vht import vht_core
from vht import vht_utils

import logging
import os
import sys

# Logging
verbosity = 'INFO'
level = { "DEBUG": 10, "INFO": 20, "WARNING" : 30, "ERROR" : 40 }
logging.basicConfig(format='[%(levelname)s]\t%(message)s', level = verbosity)
logging.debug("Verbosity level is set to " + verbosity)

# Instances
core_instance = vht_core.VhtCore()
utils_instance = vht_utils.VhtUtils()

## Get environments
# ami_id
ami_id = core_instance.get_ami_id("1.0.0") if (os.environ.get('ami_id') is None) else os.environ.get('ami_id')

# iam_profile
if os.environ.get('iam_profile') is None:
    logging.error("vht_github_action:environment variable `iam_profile` needs to be present!")
    sys.exit(-1)
else:
    iam_profile = os.environ.get('iam_profile')

# instance_id
instance_id = '' if os.environ.get('instance_id') is None else os.environ.get('instance_id')

# instance_type
if os.environ.get('instance_type') is None:
    logging.error("vht_github_action:environment variable `instance_type` needs to be present!")
    sys.exit(-1)
else:
    instance_type = os.environ.get('instance_type')

# key_name
key_name = os.environ.get('key_name')

# s3_bucket_name
if os.environ.get('s3_bucket_name') is None:
    logging.error("vht_github_action:environment variable `s3_bucket_name` needs to be present!")
    sys.exit(-1)
else:
    s3_bucket_name = os.environ.get('s3_bucket_name')

# s3_keyprefix
s3_keyprefix = 'ssm' if os.environ.get('s3_keyprefix') is None else os.environ.get('s3_keyprefix')

# security_group_id
if os.environ.get('security_group_id') is None:
    logging.error("vht_github_action:environment variable `security_group_id` needs to be present!")
    sys.exit(-1)
else:
    security_group_id = os.environ.get('security_group_id')

# subnet_id
if os.environ.get('subnet_id') is None:
    logging.error("vht_github_action:environment variable `subnet_id` needs to be present!")
    sys.exit(-1)
else:
    subnet_id = os.environ.get('subnet_id')

# gh_workspace
if os.environ.get('gh_workspace') is None:
    logging.error("vht_github_action:environment variable `gh_workspace` needs to be present!")
    sys.exit(-1)
else:
    gh_workspace = os.environ.get('gh_workspace')
    vht_in = gh_workspace + "/vht.tar"
    vht_out = gh_workspace + "/out.tar"

# terminate_ec2_instance
if os.environ.get('terminate_ec2_instance') is None:
    logging.error("vht_github_action:environment variable `terminate_ec2_instance` needs to be present!")
    sys.exit(-1)
else:
    terminate_ec2_instance = os.environ.get('terminate_ec2_instance')
    if terminate_ec2_instance == 'true':
        terminate_ec2_instance = True
    else:
        terminate_ec2_instance = False

if (instance_id == ''):
    if key_name is None:
        instance_id = core_instance.create_ec2_instance(
            ImageId=ami_id,
            InstanceType=instance_type,
            MaxCount=1,
            MinCount=1,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'VHT_CLI','Value': 'true',}]}],
            IamInstanceProfile={'Name': iam_profile}
        )
    else:
        instance_id = core_instance.create_ec2_instance(
            ImageId=ami_id,
            InstanceType=instance_type,
            MaxCount=1,
            MinCount=1,
            SecurityGroupIds=[security_group_id],
            SubnetId=subnet_id,
            KeyName='common',
            TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'VHT_CLI','Value': 'true',}]}],
            IamInstanceProfile={'Name': iam_profile}
        )
else:
    instance_state = core_instance.get_ec2_instance_state(instance_id)
    if (instance_state != 'running'):
        core_instance.start_ec2_instance(instance_id)


core_instance.upload_s3_file(s3_bucket_name, vht_in, 'vht.tar')
try:
    command_list = [
        "runuser -l ubuntu -c 'cat ~/.bashrc | grep export > vars'",
        "rm -rf vhtagent",
        "rm -rf vhtwork",
        "runuser -l ubuntu -c 'mkdir vhtagent'",
        "runuser -l ubuntu -c 'mkdir vhtwork'",
        "runuser -l ubuntu -c 'mkdir -p /home/ubuntu/packs/.Web'",
        "runuser -l ubuntu -c 'cd /home/ubuntu/vhtagent && wget https://raw.githubusercontent.com/ARM-software/VHT-AMI/master/agent/process_vht.py'",
        "runuser -l ubuntu -c 'wget -N https://www.keil.com/pack/index.pidx -O /home/ubuntu/packs/.Web/index.pidx'",
        "apt update",
        "apt install awscli -y",
        "aws s3 cp s3://" + s3_bucket_name + "/vht.tar /home/ubuntu/vhtwork/vht.tar",
        "runuser -l ubuntu -c 'source vars && python3 /home/ubuntu/vhtagent/process_vht.py'",
        "aws s3 cp /home/ubuntu/vhtwork/out.tar s3://" + s3_bucket_name + "/out.tar"
    ]

    for command in command_list:
        logging.info("vht_github_action: command = {}".format(command))
        ssm_response = core_instance.send_ssm_shell_command(
            instance_id=instance_id,
            command_list=command,
            s3_bucket_name=s3_bucket_name,
            s3_keyprefix=s3_keyprefix,
            working_dir='/home/ubuntu'
        )
        for i in ssm_response.keys():
            logging.info("vht_github_action:{} = {}".format(i, ssm_response[i].strip()))
        if ssm_response['CommandIdStatus'] != 'Success':
            raise Exception("CommandIdStatus not successful")
        logging.info("vht_github_action:-------------------------------------------")
except:
    logging.info("vht_github_action:erros happened -- see logs above")
    utils_instance.teardown(core_instance, instance_id, terminate_ec2_instance)
    sys.exit(-1)

logging.info("vht_github_action:Download S3 File to the GitHub Runner...")
core_instance.download_s3_file(
    s3_bucket_name=s3_bucket_name,
    key='out.tar',
    filename=vht_out
)

logging.info("vht_github_action:Delete S3 Out.tar object from the S3 Bucket...")
core_instance.delete_s3_object(
    s3_bucket_name=s3_bucket_name,
    key='out.tar'
)

utils_instance.teardown(core_instance, instance_id, terminate_ec2_instance)
