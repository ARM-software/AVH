import datetime
import vht.vht_core
import vht.vht_utils
import unittest

from dateutil.tz import tzutc, tzlocal
from vht.vht_core import VhtCore
from unittest.mock import patch, Mock

# stubbers
# https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html#
# https://stackoverflow.com/questions/37143597/mocking-boto3-s3-client-method-python/37144161#37144161

class TestVhtCore(unittest.TestCase):
    """
        VHT Core Test Cases
    """
    def _get_vht_core_instance(self):
        with patch.object(vht.vht_core.vht_utils.VhtUtils, 'is_aws_credentials_present', return_value=True):
            return VhtCore()

    def test_create_ec2_instance(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ec2_client.run_instances = Mock()
        core_instance.wait_ec2_status_ok = Mock()
        core_instance.wait_ec2_running = Mock()

        # setting return values for the mocked methods
        core_instance.wait_ec2_status_ok.return_value = None
        core_instance.wait_ec2_running.return_value = None
        core_instance.ec2_client.run_instances.return_value = {
            'Groups': [],
            'Instances': [{
                'AmiLaunchIndex': 0,
                'ImageId': 'ami-0c5eeabe11f3a2685',
                'InstanceId': 'i-064a8d261aea65d9e',
                'InstanceType': 't2.micro',
                'LaunchTime': datetime.datetime(2022, 1, 3, 14, 48, 11, tzinfo=tzutc()),
                'Monitoring': {
                    'State': 'disabled'
                },
                'Placement': {
                    'AvailabilityZone': 'eu-west-1a',
                    'GroupName': '',
                    'Tenancy': 'default'
                },
                'PrivateDnsName': 'ip-10-252-70-151.eu-west-1.compute.internal',
                'PrivateIpAddress': '10.252.70.151',
                'ProductCodes': [],
                'PublicDnsName': '',
                'State': {
                    'Code': 0,
                    'Name': 'pending'
                },
                'StateTransitionReason': '',
                'SubnetId': 'subnet-00455495b268076f0',
                'VpcId': 'vpc-0dc320e47b6a8077f',
                'Architecture': 'x86_64',
                'BlockDeviceMappings': [],
                'ClientToken': 'ea10f8d4-857a-4130-9da4-39716dcef8e4',
                'EbsOptimized': False,
                'EnaSupport': True,
                'Hypervisor': 'xen',
                'IamInstanceProfile': {
                    'Arn': 'arn:aws:iam::720528183931:instance-profile/Proj-s3-orta-vht-role',
                    'Id': 'AIPA2PQWTSJ5SM4JWDFHG'
                },
                'NetworkInterfaces': [{
                    'Attachment': {
                        'AttachTime': datetime.datetime(2022, 1, 3, 14, 48, 11, tzinfo=tzutc()),
                        'AttachmentId': 'eni-attach-00db5f220383f42af',
                        'DeleteOnTermination': True,
                        'DeviceIndex': 0,
                        'Status': 'attaching',
                        'NetworkCardIndex': 0
                    },
                    'Description': '',
                    'Groups': [{
                        'GroupName': 'Arm Virtual Hardware-Initial release-AutogenByAWSMP-',
                        'GroupId': 'sg-04022e04e91197ce3'
                    }],
                    'Ipv6Addresses': [],
                    'MacAddress': '0a:38:3c:bb:2d:b1',
                    'NetworkInterfaceId': 'eni-0e292f48e4e254128',
                    'OwnerId': '720528183931',
                    'PrivateDnsName': 'ip-10-252-70-151.eu-west-1.compute.internal',
                    'PrivateIpAddress': '10.252.70.151',
                    'PrivateIpAddresses': [{
                        'Primary': True,
                        'PrivateDnsName': 'ip-10-252-70-151.eu-west-1.compute.internal',
                        'PrivateIpAddress': '10.252.70.151'
                    }],
                    'SourceDestCheck': True,
                    'Status': 'in-use',
                    'SubnetId': 'subnet-00455495b268076f0',
                    'VpcId': 'vpc-0dc320e47b6a8077f',
                    'InterfaceType': 'interface'
                }],
                'RootDeviceName': '/dev/sda1',
                'RootDeviceType': 'ebs',
                'SecurityGroups': [{
                    'GroupName': 'Arm Virtual Hardware-Initial release-AutogenByAWSMP-',
                    'GroupId': 'sg-04022e04e91197ce3'
                }],
                'SourceDestCheck': True,
                'StateReason': {
                    'Code': 'pending',
                    'Message': 'pending'
                },
                'VirtualizationType': 'hvm',
                'CpuOptions': {
                    'CoreCount': 1,
                    'ThreadsPerCore': 1
                },
                'CapacityReservationSpecification': {
                    'CapacityReservationPreference': 'open'
                },
                'MetadataOptions': {
                    'State': 'pending',
                    'HttpTokens': 'optional',
                    'HttpPutResponseHopLimit': 1,
                    'HttpEndpoint': 'enabled',
                    'HttpProtocolIpv6': 'disabled'
                },
                'EnclaveOptions': {
                    'Enabled': False
                },
                'PrivateDnsNameOptions': {
                    'HostnameType': 'ip-name',
                    'EnableResourceNameDnsARecord': False,
                    'EnableResourceNameDnsAAAARecord': False
                }
            }],
            'OwnerId': '720528183931',
            'ReservationId': 'r-01bb976ccb7d00dfd',
            'ResponseMetadata': {
                'RequestId': 'de98e48d-b2ee-4d30-aef8-7455a2c1a614',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': 'de98e48d-b2ee-4d30-aef8-7455a2c1a614',
                    'cache-control': 'no-cache, no-store',
                    'strict-transport-security': 'max-age=31536000; includeSubDomains',
                    'vary': 'accept-encoding',
                    'content-type': 'text/xml;charset=UTF-8',
                    'content-length': '5617',
                    'date': 'Mon, 03 Jan 2022 14:48:11 GMT',
                    'server': 'AmazonEC2'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        instance_id = core_instance.create_ec2_instance(
            ImageId='ami-0c5eeabe11f3a2685',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            SecurityGroupIds=['sg-04022e04e91197ce3'],
            SubnetId='subnet-00455495b268076f0',
            TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'VHT_CLI','Value': 'true',}]}],
            IamInstanceProfile={'Name': 'Proj-s3-orta-vht-role'}
        )

        # asserting values
        assert core_instance.ec2_client.run_instances.called
        assert core_instance.wait_ec2_status_ok.called
        assert core_instance.wait_ec2_running.called
        assert instance_id == 'i-064a8d261aea65d9e'

    def test_delete_s3_object(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.s3_client.delete_object = Mock()

        # setting return values for the mocked methods
        core_instance.s3_client.delete_object.return_value = None

        # running the actual method
        response = core_instance.delete_s3_object('s3_bucket_name', 'key')

        # asserting values
        assert core_instance.s3_client.delete_object.called
        assert response is None

    def test_download_s3_file(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.s3_client.download_file = Mock()

        # setting return values for the mocked methods
        core_instance.s3_client.download_file.return_value = None

        # running the actual method
        response = core_instance.download_s3_file('s3_bucket_name', 'key', 'filename')

        # asserting values
        assert core_instance.s3_client.download_file.called
        assert response is None

    def test_get_ami_id(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ec2_client.describe_images = Mock()

        # setting return values for the mocked methods
        core_instance.ec2_client.describe_images.return_value = {
            'Images': [{
                'Architecture': 'x86_64',
                'CreationDate': '2021-10-15T07:25:55.000Z',
                'ImageId': 'ami-0c5eeabe11f3a2685',
                'ImageLocation': 'aws-marketplace/ArmVirtualHardware-1.0.0-46c83f57-6612-4bba-9cab-901225d20134',
                'ImageType': 'machine',
                'Public': True,
                'OwnerId': '679593333241',
                'PlatformDetails': 'Linux/UNIX',
                'UsageOperation': 'RunInstances',
                'ProductCodes': [{
                    'ProductCodeId': '46uuys3r5s9869n32wjpldh6c',
                    'ProductCodeType': 'marketplace'
                }],
                'State': 'available',
                'BlockDeviceMappings': [{
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'SnapshotId': 'snap-0766f863beddee37c',
                        'VolumeSize': 24,
                        'VolumeType': 'gp2',
                        'Encrypted': False
                    }
                }],
                'EnaSupport': True,
                'Hypervisor': 'xen',
                'ImageOwnerAlias': 'aws-marketplace',
                'Name': 'ArmVirtualHardware-1.0.0-46c83f57-6612-4bba-9cab-901225d20134',
                'RootDeviceName': '/dev/sda1',
                'RootDeviceType': 'ebs',
                'SriovNetSupport': 'simple',
                'VirtualizationType': 'hvm'
            }],
            'ResponseMetadata': {
                'RequestId': 'b69537d6-e141-480a-a087-ce20d52ecd1d',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': 'b69537d6-e141-480a-a087-ce20d52ecd1d',
                    'cache-control': 'no-cache, no-store',
                    'strict-transport-security': 'max-age=31536000; includeSubDomains',
                    'content-type': 'text/xml;charset=UTF-8',
                    'content-length': '2044',
                    'date': 'Mon, 03 Jan 2022 14:48:08 GMT',
                    'server': 'AmazonEC2'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        response = core_instance.get_ami_id('1.0.0')

        # asserting values
        assert core_instance.ec2_client.describe_images.called
        assert response == 'ami-0c5eeabe11f3a2685'

    def test_get_ec2_instance_state(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ec2_client.describe_instances = Mock()

        # setting return values for the mocked methods
        core_instance.ec2_client.describe_instances.return_value = {
            'Reservations': [{
                'Groups': [],
                'Instances': [{
                    'AmiLaunchIndex': 0,
                    'ImageId': 'ami-0c5eeabe11f3a2685',
                    'InstanceId': 'i-064a8d261aea65d9e',
                    'InstanceType': 't2.micro',
                    'LaunchTime': datetime.datetime(2022, 1, 3, 14, 48, 11, tzinfo=tzutc()),
                    'Monitoring': {
                        'State': 'disabled'
                    },
                    'Placement': {
                        'AvailabilityZone': 'eu-west-1a',
                        'GroupName': '',
                        'Tenancy': 'default'
                    },
                    'PrivateDnsName': 'ip-10-252-70-151.eu-west-1.compute.internal',
                    'PrivateIpAddress': '10.252.70.151',
                    'ProductCodes': [{
                        'ProductCodeId': '46uuys3r5s9869n32wjpldh6c',
                        'ProductCodeType': 'marketplace'
                    }],
                    'PublicDnsName': '',
                    'State': {
                        'Code': 16,
                        'Name': 'running'
                    },
                    'StateTransitionReason': '',
                    'SubnetId': 'subnet-00455495b268076f0',
                    'VpcId': 'vpc-0dc320e47b6a8077f',
                    'Architecture': 'x86_64',
                    'BlockDeviceMappings': [{
                        'DeviceName': '/dev/sda1',
                        'Ebs': {
                            'AttachTime': datetime.datetime(2022, 1, 3, 14, 48, 12, tzinfo=tzutc()),
                            'DeleteOnTermination': True,
                            'Status': 'attached',
                            'VolumeId': 'vol-0174cd68348050d2d'
                        }
                    }],
                    'ClientToken': 'ea10f8d4-857a-4130-9da4-39716dcef8e4',
                    'EbsOptimized': False,
                    'EnaSupport': True,
                    'Hypervisor': 'xen',
                    'IamInstanceProfile': {
                        'Arn': 'arn:aws:iam::720528183931:instance-profile/Proj-s3-orta-vht-role',
                        'Id': 'AIPA2PQWTSJ5SM4JWDFHG'
                    },
                    'NetworkInterfaces': [{
                        'Attachment': {
                            'AttachTime': datetime.datetime(2022, 1, 3, 14, 48, 11, tzinfo=tzutc()),
                            'AttachmentId': 'eni-attach-00db5f220383f42af',
                            'DeleteOnTermination': True,
                            'DeviceIndex': 0,
                            'Status': 'attached',
                            'NetworkCardIndex': 0
                        },
                        'Description': '',
                        'Groups': [{
                            'GroupName': 'Arm Virtual Hardware-Initial release-AutogenByAWSMP-',
                            'GroupId': 'sg-04022e04e91197ce3'
                        }],
                        'Ipv6Addresses': [],
                        'MacAddress': '0a:38:3c:bb:2d:b1',
                        'NetworkInterfaceId': 'eni-0e292f48e4e254128',
                        'OwnerId': '720528183931',
                        'PrivateDnsName': 'ip-10-252-70-151.eu-west-1.compute.internal',
                        'PrivateIpAddress': '10.252.70.151',
                        'PrivateIpAddresses': [{
                            'Primary': True,
                            'PrivateDnsName': 'ip-10-252-70-151.eu-west-1.compute.internal',
                            'PrivateIpAddress': '10.252.70.151'
                        }],
                        'SourceDestCheck': True,
                        'Status': 'in-use',
                        'SubnetId': 'subnet-00455495b268076f0',
                        'VpcId': 'vpc-0dc320e47b6a8077f',
                        'InterfaceType': 'interface'
                    }],
                    'RootDeviceName': '/dev/sda1',
                    'RootDeviceType': 'ebs',
                    'SecurityGroups': [{
                        'GroupName': 'Arm Virtual Hardware-Initial release-AutogenByAWSMP-',
                        'GroupId': 'sg-04022e04e91197ce3'
                    }],
                    'SourceDestCheck': True,
                    'VirtualizationType': 'hvm',
                    'CpuOptions': {
                        'CoreCount': 1,
                        'ThreadsPerCore': 1
                    },
                    'CapacityReservationSpecification': {
                        'CapacityReservationPreference': 'open'
                    },
                    'HibernationOptions': {
                        'Configured': False
                    },
                    'MetadataOptions': {
                        'State': 'applied',
                        'HttpTokens': 'optional',
                        'HttpPutResponseHopLimit': 1,
                        'HttpEndpoint': 'enabled',
                        'HttpProtocolIpv6': 'disabled'
                    },
                    'EnclaveOptions': {
                        'Enabled': False
                    },
                    'PlatformDetails': 'Linux/UNIX',
                    'UsageOperation': 'RunInstances',
                    'UsageOperationUpdateTime': datetime.datetime(2022, 1, 3, 14, 48, 11, tzinfo=tzutc()),
                    'PrivateDnsNameOptions': {
                        'HostnameType': 'ip-name',
                        'EnableResourceNameDnsARecord': False,
                        'EnableResourceNameDnsAAAARecord': False
                    }
                }],
                'OwnerId': '720528183931',
                'ReservationId': 'r-01bb976ccb7d00dfd'
            }],
            'ResponseMetadata': {
                'RequestId': '2147b8e0-c2d8-4d2e-9913-c95487cfd767',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'x-amzn-requestid': '2147b8e0-c2d8-4d2e-9913-c95487cfd767',
                    'cache-control': 'no-cache, no-store',
                    'strict-transport-security': 'max-age=31536000; includeSubDomains',
                    'vary': 'accept-encoding',
                    'content-type': 'text/xml;charset=UTF-8',
                    'content-length': '7545',
                    'date': 'Mon, 03 Jan 2022 14:51:57 GMT',
                    'server': 'AmazonEC2'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        response = core_instance.get_ec2_instance_state('i-064a8d261aea65d9e')

        # asserting values
        assert core_instance.ec2_client.describe_instances.called
        assert response == 'running'

    @unittest.skip('Find out how to mock s3_resource.Object.get')
    def test_get_s3_file_content(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        # setting return values for the mocked methods
        core_instance.s3_resource.Object('s3_bucket_name', 'key').get = Mock(
            return_value="drwxr-xr-x  13 root root  4096 Apr 30  2021 var"
        )

        # running the actual method
        response = core_instance.get_s3_file_content('s3_bucket_name', 'key')

        # asserting values
        assert core_instance.s3_resource.Object.called
        assert response == "drwxr-xr-x  13 root root  4096 Apr 30  2021 var"

    def test_get_s3_ssm_command_id_key(self):
        core_instance = self._get_vht_core_instance()

        s3_keyprefix = 'some_prefix'
        command_id = '8f181e5d-8fec-45fa-9bfa-812e76df650c'
        instance_id = 'i-064a8d261aea65d9e'
        output_type = 'stdout'

        response = core_instance.get_s3_ssm_command_id_key(
            instance_id,
            command_id,
            s3_keyprefix,
            output_type
        )
        expected_response = "{}/{}/{}/awsrunShellScript/0.awsrunShellScript/{}".format(
            s3_keyprefix,
            command_id,
            instance_id,
            output_type
        )

        assert response == expected_response

    def test_get_ssm_command_id_status(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ssm_client.list_commands = Mock()

        # setting return values for the mocked methods
        core_instance.ssm_client.list_commands.return_value = {
            'Commands': [{
                'CommandId': '8f181e5d-8fec-45fa-9bfa-812e76df650c',
                'DocumentName': 'AWS-RunShellScript',
                'DocumentVersion': '$DEFAULT',
                'Comment': '',
                'ExpiresAfter': datetime.datetime(2022, 1, 3, 17, 1, 45, 663000, tzinfo=tzlocal()),
                'Parameters': {
                    'commands': ['ls -la'],
                    'workingDirectory': ['/']
                },
                'InstanceIds': ['i-064a8d261aea65d9e'],
                'Targets': [],
                'RequestedDateTime': datetime.datetime(2022, 1, 3, 15, 51, 45, 663000, tzinfo=tzlocal()),
                'Status': 'Success',
                'StatusDetails': 'Success',
                'OutputS3Region': 'eu-west-1',
                'OutputS3BucketName': 'gh-orta-vht',
                'OutputS3KeyPrefix': 'ssm',
                'MaxConcurrency': '50',
                'MaxErrors': '0',
                'TargetCount': 1,
                'CompletedCount': 1,
                'ErrorCount': 0,
                'DeliveryTimedOutCount': 0,
                'ServiceRole': '',
                'NotificationConfig': {
                    'NotificationArn': '',
                    'NotificationEvents': [],
                    'NotificationType': ''
                },
                'CloudWatchOutputConfig': {
                    'CloudWatchLogGroupName': '',
                    'CloudWatchOutputEnabled': False
                },
                'TimeoutSeconds': 600
            }],
            'ResponseMetadata': {
                'RequestId': '2d226bf9-efbd-461b-a381-225773ec85cd',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'server': 'Server',
                    'date': 'Mon, 03 Jan 2022 14:51:47 GMT',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '847',
                    'connection': 'keep-alive',
                    'x-amzn-requestid': '2d226bf9-efbd-461b-a381-225773ec85cd'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        response = core_instance.get_ssm_command_id_status(
            command_id='8f181e5d-8fec-45fa-9bfa-812e76df650c'
        )

        # asserting values
        assert core_instance.ssm_client.list_commands.called
        assert response == 'Success'

    def test_get_ssm_command_id_status_details(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ssm_client.get_command_invocation = Mock()

        # setting return values for the mocked methods
        core_instance.ssm_client.get_command_invocation.return_value = {
            'CommandId': 'da584039-585c-4fd7-b30f-fad58c42c881',
            'InstanceId': 'i-000f2435623398464',
            'Comment': '',
            'DocumentName': 'AWS-RunShellScript',
            'DocumentVersion': '$DEFAULT',
            'PluginName': 'aws:runShellScript',
            'ResponseCode': 0,
            'ExecutionStartDateTime': '2022-01-05T10:35:35.383Z',
            'ExecutionElapsedTime': 'PT0.198S',
            'ExecutionEndDateTime': '2022-01-05T10:35:35.383Z',
            'Status': 'Success',
            'StatusDetails': 'Success',
            'StandardOutputContent': 'total 80\ndrwxr-xr-x  19 root root  4096 Jan  5 10:33 .\ndrwxr-xr-x  19 root root  4096 Jan  5 10:33 ..\nlrwxrwxrwx   1 root root     7 Apr 30  2021 bin -> usr/bin\ndrwxr-xr-x   3 root root  4096 Oct 14 17:56 boot\ndrwxr-xr-x  17 root root  3200 Jan  5 10:34 dev\ndrwxr-xr-x 135 root root 12288 Jan  5 10:33 etc\ndrwxr-xr-x   3 root root  4096 Oct 14 17:53 home\nlrwxrwxrwx   1 root root     7 Apr 30  2021 lib -> usr/lib\nlrwxrwxrwx   1 root root     9 Apr 30  2021 lib32 -> usr/lib32\nlrwxrwxrwx   1 root root     9 Apr 30  2021 lib64 -> usr/lib64\nlrwxrwxrwx   1 root root    10 Apr 30  2021 libx32 -> usr/libx32\ndrwx------   2 root root 16384 Apr 30  2021 lost+found\ndrwxr-xr-x   2 root root  4096 Apr 30  2021 media\ndrwxr-xr-x   2 root root  4096 Apr 30  2021 mnt\ndrwxr-xr-x   8 root root  4096 Oct 14 18:00 opt\ndr-xr-xr-x 186 root root     0 Jan  5 10:33 proc\ndrwx------   6 root root  4096 Jan  5 10:33 root\ndrwxr-xr-x  27 root root   880 Jan  5 10:34 run\nlrwxrwxrwx   1 root root     8 Apr 30  2021 sbin -> usr/sbin\ndrwxr-xr-x   8 root root  4096 Jan  5 10:34 snap\ndrwxr-xr-x   2 root root  4096 Apr 30  2021 srv\ndr-xr-xr-x  13 root root     0 Jan  5 10:33 sys\ndrwxrwxrwt  18 root root  4096 Jan  5 10:35 tmp\ndrwxr-xr-x  15 root root  4096 Apr 30  2021 usr\ndrwxr-xr-x  13 root root  4096 Apr 30  2021 var\n',
            'StandardOutputUrl': 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stdout',
            'StandardErrorContent': '',
            'StandardErrorUrl': 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stderr',
            'CloudWatchOutputConfig': {
                'CloudWatchLogGroupName': '',
                'CloudWatchOutputEnabled': False
            },
            'ResponseMetadata': {
                'RequestId': '3eea5728-2539-427a-acf7-35cc93493e2d',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'server': 'Server',
                    'date': 'Wed, 05 Jan 2022 10:35:41 GMT',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '2214',
                    'connection': 'keep-alive',
                    'x-amzn-requestid': '3eea5728-2539-427a-acf7-35cc93493e2d'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        response = core_instance.get_ssm_command_id_status_details(
            instance_id='i-064a8d261aea65d9e',
            command_id='8f181e5d-8fec-45fa-9bfa-812e76df650c'
        )

        # asserting values
        assert core_instance.ssm_client.get_command_invocation.called
        assert response == 'Success'

    def test_get_ssm_command_id_stdout_url(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ssm_client.list_command_invocations = Mock()

        # setting return values for the mocked methods
        core_instance.ssm_client.list_command_invocations.return_value = {
            'CommandInvocations': [{
                'CommandId': 'da584039-585c-4fd7-b30f-fad58c42c881',
                'InstanceId': 'i-000f2435623398464',
                'InstanceName': 'ip-10-252-70-185.eu-west-1.compute.internal',
                'Comment': '',
                'DocumentName': 'AWS-RunShellScript',
                'DocumentVersion': '$DEFAULT',
                'RequestedDateTime': datetime.datetime(2022, 1, 5, 11, 35, 34, 581000, tzinfo=tzlocal()),
                'Status': 'Success',
                'StatusDetails': 'Success',
                'StandardOutputUrl': 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stdout',
                'StandardErrorUrl': 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stderr',
                'CommandPlugins': [],
                'ServiceRole': '',
                'NotificationConfig': {
                    'NotificationArn': '',
                    'NotificationEvents': [],
                    'NotificationType': ''
                },
                'CloudWatchOutputConfig': {
                    'CloudWatchLogGroupName': '',
                    'CloudWatchOutputEnabled': False
                }
            }],
            'ResponseMetadata': {
                'RequestId': '7b44dfb6-410a-473e-8d85-2b0f3d421d5b',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'server': 'Server',
                    'date': 'Wed, 05 Jan 2022 10:35:43 GMT',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '896',
                    'connection': 'keep-alive',
                    'x-amzn-requestid': '7b44dfb6-410a-473e-8d85-2b0f3d421d5b'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        response = core_instance.get_ssm_command_id_stdout_url(
            instance_id='i-000f2435623398464',
            command_id='da584039-585c-4fd7-b30f-fad58c42c881'
        )

        # asserting values
        assert core_instance.ssm_client.list_command_invocations.called
        assert response == 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stdout'

    def test_get_ssm_command_id_stderr_url(self):
        core_instance = self._get_vht_core_instance()

        # mocking methods
        core_instance.ssm_client.list_command_invocations = Mock()

        # setting return values for the mocked methods
        core_instance.ssm_client.list_command_invocations.return_value = {
            'CommandInvocations': [{
                'CommandId': 'da584039-585c-4fd7-b30f-fad58c42c881',
                'InstanceId': 'i-000f2435623398464',
                'InstanceName': 'ip-10-252-70-185.eu-west-1.compute.internal',
                'Comment': '',
                'DocumentName': 'AWS-RunShellScript',
                'DocumentVersion': '$DEFAULT',
                'RequestedDateTime': datetime.datetime(2022, 1, 5, 11, 35, 34, 581000, tzinfo=tzlocal()),
                'Status': 'Success',
                'StatusDetails': 'Success',
                'StandardOutputUrl': 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stdout',
                'StandardErrorUrl': 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stderr',
                'CommandPlugins': [],
                'ServiceRole': '',
                'NotificationConfig': {
                    'NotificationArn': '',
                    'NotificationEvents': [],
                    'NotificationType': ''
                },
                'CloudWatchOutputConfig': {
                    'CloudWatchLogGroupName': '',
                    'CloudWatchOutputEnabled': False
                }
            }],
            'ResponseMetadata': {
                'RequestId': '7b44dfb6-410a-473e-8d85-2b0f3d421d5b',
                'HTTPStatusCode': 200,
                'HTTPHeaders': {
                    'server': 'Server',
                    'date': 'Wed, 05 Jan 2022 10:35:43 GMT',
                    'content-type': 'application/x-amz-json-1.1',
                    'content-length': '896',
                    'connection': 'keep-alive',
                    'x-amzn-requestid': '7b44dfb6-410a-473e-8d85-2b0f3d421d5b'
                },
                'RetryAttempts': 0
            }
        }

        # running the actual method
        response = core_instance.get_ssm_command_id_stderr_url(
            instance_id='i-000f2435623398464',
            command_id='da584039-585c-4fd7-b30f-fad58c42c881'
        )

        # asserting values
        assert core_instance.ssm_client.list_command_invocations.called
        assert response == 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stderr'

    @unittest.skip('TODO')
    def test_send_ssm_shell_command(self):
        pass

    @unittest.skip('TODO')
    def test_start_ec2_instance(self):
        pass

    @unittest.skip('TODO')
    def test_stop_ec2_instance(self):
        pass

    @unittest.skip('TODO')
    def test_wait_ec2_status_ok(self):
        pass

    @unittest.skip('TODO')
    def test_wait_ec2_running(self):
        pass

    @unittest.skip('TODO')
    def test_wait_ec2_stopped(self):
        pass

    @unittest.skip('TODO')
    def test_wait_ec2_terminated(self):
        pass

    @unittest.skip('TODO')
    def test_wait_s3_object_exists(self):
        pass

    @unittest.skip('TODO')
    def test_wait_ssm_command_finished(self):
        pass

    @unittest.skip('TODO')
    def test_terminate_ec2_instance(self):
        pass


if __name__ == '__main__':
    unittest.main()
