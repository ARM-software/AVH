#/bin/bash -ex

# CONTS
VERBOSITY=INFO
VHT_IMAGE_VERSION=1.0.0
IAM_INSTANCE_PROFILE=Proj-s3-orta-vht-role
INSTANCE_TYPE=t2.micro
S3_BUCKET_NAME=gh-orta-vht
S3_KEYPREFIX=ssm
SECURITY_GROUP_ID=sg-04022e04e91197ce3
SUBNET_ID=subnet-00455495b268076f0

ami_id=$(vht_cli -v $VERBOSITY --get-ami-id $VHT_IMAGE_VERSION)
echo "VHT AMI ID = $ami_id"

instance_id=$(vht_cli -v $VERBOSITY --create-ec2-instance \
    ImageId="$ami_id" \
    InstanceType="$INSTANCE_TYPE" \
    MaxCount=1 \
    MinCount=1 \
    SecurityGroupIds=["${SECURITY_GROUP_ID}"] \
    SubnetId="$SUBNET_ID"  \
    IamInstanceProfile="{'Name': '$IAM_INSTANCE_PROFILE'}")
echo "Instance ID = $instance_id"

command_id=$(vht_cli -v $VERBOSITY --send-ssm-shell-command \
    InstanceId=$instance_id \
    commandList='ls -la' \
    s3BucketName=$S3_BUCKET_NAME \
    s3KeyPrefix=$S3_KEYPREFIX)
echo "Command ID = $command_id"

command_id_status=$(vht_cli -v $VERBOSITY --get-ssm-command-id-status $command_id)
echo "Command ID status = $command_id_status"

command_id_status_details=$(vht_cli -v $VERBOSITY --get-ssm-command-id-status-details \
    CommandId=$command_id \
    InstanceId=$instance_id)
echo "Command ID status Details = $command_id_status_details"

command_id_stdout_url=$(vht_cli -v $VERBOSITY --get-ssm-command-id-stdout-url \
    CommandId=$command_id \
    InstanceId=$instance_id)
echo "Command ID Stdout URL = $command_id_stdout_url"

command_id_stderr_url=$(vht_cli -v $VERBOSITY --get-ssm-command-id-stderr-url \
    CommandId=$command_id \
    InstanceId=$instance_id)
echo "Command ID Stderr URL = $command_id_stderr_url"

stdout_s3_key=$(vht_cli -v $VERBOSITY --get-s3-ssm-command-id-key \
    InstanceId=$instance_id \
    CommandId=$command_id \
    s3KeyPrefix=$S3_KEYPREFIX \
    OutputType=stdout)
echo "Stdout S3 Key Location = $stdout_s3_key"

stderr_s3_key=$(vht_cli -v $VERBOSITY --get-s3-ssm-command-id-key \
    InstanceId=$instance_id \
    CommandId=$command_id \
    s3KeyPrefix=$S3_KEYPREFIX \
    OutputType=stderr)
echo "Stderr S3 Key Location = $stderr_s3_key"

vht_cli -v $VERBOSITY --download-s3-file \
    s3BucketName=$S3_BUCKET_NAME \
    key=$stdout_s3_key \
    filename=stdout

vht_cli -v $VERBOSITY --download-s3-file \
    s3BucketName=$S3_BUCKET_NAME \
    key=$stderr_s3_key \
    filename=stderr

vht_cli -v $VERBOSITY --get-s3-file-content \
    s3BucketName=$S3_BUCKET_NAME \
    key=$stdout_s3_key

vht_cli -v $VERBOSITY --get-s3-file-content \
    s3BucketName=$S3_BUCKET_NAME \
    key=$stderr_s3_key

instance_state=$(vht_cli -v $VERBOSITY --get-ec2-instance-state $instance_id)
echo "Instance State = $instance_state"

vht_cli -v $VERBOSITY --stop-ec2-instance $instance_id
vht_cli -v $VERBOSITY --start-ec2-instance $instance_id
vht_cli -v $VERBOSITY --terminate-ec2-instance $instance_id
