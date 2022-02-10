import datetime
import os
import logging
import unittest

from unittest.mock import patch, Mock
from dateutil.tz import tzutc, tzlocal
from vht import vht

# stubbers
# https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html#
# https://stackoverflow.com/questions/37143597/mocking-boto3-s3-client-method-python/37144161#37144161

class TestVhtAws(unittest.TestCase):
    """
        VHT Core Test Cases
    """
    @classmethod
    def setUpClass(cls):
        cls.data = {}
        # mandatory data
        cls.data['gh_workspace'] = 'test\\'
        cls.data['s3_bucket_name'] = 'gh-orta-vht'
        cls.data['s3_keyprefix'] = 'ssm_test'
        # optional data
        cls.data['ami_id'] = 'i-dsad3213d'
        cls.data['ami_version'] = '1.1.0'
        cls.data['iam_profile'] = 'Proj-vht-limited-actions'
        cls.data['instance_id'] = 'i-instance342321'
        cls.data['instance_type'] = 't2.micro'
        cls.data['key_name'] = 'common'
        cls.data['security_group_id'] = 'sg-04022e04e91197ce3'
        cls.data['subnet_id'] = 'subnet-00455495b268076f0'
        cls.data['terminate_ec2_instance'] = True

    def get_vht_aws_instance(self):
        self.set_mandatory_env_vars()
        self.set_create_instance_env_vars()
        self.set_ami_id_env()
        self.set_ami_version_env()
        self.set_instance_id_env()
        self.set_s3_keyprefix_env()
        self.set_key_name_env()
        with patch.object(vht.aws.AWSClient, '_is_aws_credentials_present', return_value=True):
            aws_client = vht.VHTClient("aws").backend
        self.del_ami_id_env()
        self.del_ami_version_env()
        self.del_create_instance_env_vars()
        self.del_instance_id_env()
        self.del_key_name_env()
        self.del_s3_keyprefix_env()
        return aws_client

    def set_mandatory_env_vars(self):
        os.environ["gh_workspace"] = self.data['gh_workspace']
        os.environ["s3_bucket_name"] = self.data['s3_bucket_name']
        os.environ["s3_keyprefix"] = self.data['s3_keyprefix']

    def set_create_instance_env_vars(self):
        os.environ["instance_type"] = self.data['instance_type']
        os.environ["iam_profile"] = self.data['iam_profile']
        os.environ["security_group_id"] = self.data['security_group_id']
        os.environ["subnet_id"] = self.data['subnet_id']
        os.environ["terminate_ec2_instance"] = str(self.data['terminate_ec2_instance'])

    def set_ami_id_env(self):
        os.environ["ami_id"] = self.data['ami_id']

    def set_ami_version_env(self):
        os.environ["ami_version"] = self.data['ami_version']

    def set_instance_id_env(self):
        os.environ["instance_id"] = self.data['instance_id']

    def set_key_name_env(self):
        os.environ["key_name"] = self.data['key_name']

    def set_s3_keyprefix_env(self):
        os.environ["s3_keyprefix"] = self.data['s3_keyprefix']

    def del_ami_id_env(self):
        del os.environ["ami_id"]

    def del_ami_version_env(self):
        del os.environ["ami_version"]

    def del_create_instance_env_vars(self):
        del os.environ["instance_type"]
        del os.environ["iam_profile"]
        del os.environ["security_group_id"]
        del os.environ["subnet_id"]
        del os.environ["terminate_ec2_instance"]

    def del_instance_id_env(self):
        del os.environ["instance_id"]

    def del_key_name_env(self):
        del os.environ["key_name"]

    def del_s3_keyprefix_env(self):
        del os.environ["s3_keyprefix"]

    def test_vht_aws_setup(self):
        with patch.object(vht.aws.AWSClient, '_is_aws_credentials_present', return_value=True):
            self.set_mandatory_env_vars()
            self.set_create_instance_env_vars()

            # test with ami_id
            self.set_ami_id_env()
            aws_client = vht.VHTClient("aws").backend

            # test with key_name
            self.set_key_name_env()
            aws_client = vht.VHTClient("aws").backend
            assert aws_client.key_name == self.data['key_name'], \
                f"Found {aws_client.key_name}. Expected {self.data['key_name']}"
            self.del_key_name_env()

            # test mandatory env vars
            aws_client = vht.VHTClient("aws").backend
            assert aws_client.instance_type == self.data['instance_type'], \
                f"Found {aws_client.instance_type}. Expected {self.data['instance_type']}"
            assert aws_client.iam_profile == self.data['iam_profile'], \
                f"Found {aws_client.iam_profile}. Expected {self.data['iam_profile']}"
            assert aws_client.gh_workspace == self.data['gh_workspace'], \
                f"Found {aws_client.gh_workspace}. Expected {self.data['gh_workspace']}"
            assert aws_client.s3_bucket_name == self.data['s3_bucket_name'], \
                f"Found {aws_client.s3_bucket_name}. Expected {self.data['s3_bucket_name']}"
            assert aws_client.security_group_id == self.data['security_group_id'], \
                f"Found {aws_client.security_group_id}. Expected {self.data['security_group_id']}"
            assert aws_client.subnet_id == self.data['subnet_id'], \
                f"Found {aws_client.subnet_id}. Expected {self.data['subnet_id']}"
            assert aws_client.terminate_ec2_instance == self.data['terminate_ec2_instance'], \
                f"Found {aws_client.terminate_ec2_instance}. Expected {self.data['terminate_ec2_instance']}"

            assert aws_client.ami_id == self.data['ami_id'], \
                f"Found {aws_client.ami_id}. Expected {self.data['ami_id']}"
            assert aws_client.ami_version is None, \
                f"Found {aws_client.ami_version}. Expected None"

            # Negative test
            assert aws_client.instance_id is None, \
                f"Found {aws_client.instance_id}. Expected None"
            assert aws_client.s3_keyprefix == self.data['s3_keyprefix'], \
                f"Found {aws_client.s3_keyprefix}. Expected {self.data['s3_keyprefix']}."
            assert aws_client.key_name is None, \
                f"Found {aws_client.key_name}. Expected \'\'"

            # test with ami_id && ami_version
            self.set_ami_version_env()
            aws_client = vht.VHTClient("aws").backend
            assert aws_client.ami_id == self.data['ami_id'], \
                f"Found {aws_client.ami_id}. Expected {self.data['ami_id']}"
            assert aws_client.ami_version == self.data['ami_version'], \
                f"Found {aws_client.ami_version}. Expected {self.data['ami_version']}"

            # test with ami_version()
            with patch.object(vht.aws.AWSClient, 'get_image_id', return_value=self.data['ami_id']):
                aws_client = vht.VHTClient("aws").backend
                assert aws_client.ami_id == self.data['ami_id'], \
                    f"Found {aws_client.ami_id}. Expected {self.data['ami_id']}"
                assert aws_client.ami_version == self.data['ami_version'], \
                    f"Found {aws_client.ami_version}. Expected {self.data['ami_version']}"
                self.del_ami_version_env()
                self.del_ami_id_env()

            # test with instance id
            self.del_create_instance_env_vars()
            self.set_instance_id_env()
            aws_client = vht.VHTClient("aws").backend
            assert aws_client.instance_id == self.data['instance_id'], \
                f"Found {aws_client.instance_id}. Expected {self.data['instance_id']}"
            assert aws_client.ami_id is None, \
                f"Found {aws_client.ami_id}. Expected None"
            assert aws_client.ami_version is None, \
                f"Found {aws_client.ami_version}. Expected None"

            # test with s3_keyprefix
            self.set_s3_keyprefix_env()
            aws_client = vht.VHTClient("aws").backend
            assert aws_client.s3_keyprefix == self.data['s3_keyprefix'], \
                f"Found {aws_client.s3_keyprefix}. Expected {self.data['s3_keyprefix']}"

    def test_create_instance(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.ec2_client.run_instances = Mock()
        aws_client.wait_ec2_status_ok = Mock()
        aws_client.wait_ec2_running = Mock()

        # setting return values for the mocked methods
        aws_client.wait_ec2_status_ok.return_value = None
        aws_client.wait_ec2_running.return_value = None
        aws_client.ec2_client.run_instances.return_value = {
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
        instance_id = aws_client.create_instance()

        # asserting values
        assert aws_client.ec2_client.run_instances.called
        assert aws_client.wait_ec2_status_ok.called
        assert aws_client.wait_ec2_running.called
        assert instance_id == 'i-064a8d261aea65d9e'

    def test_delete_file_from_cloud(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.s3_client.delete_object = Mock()

        # setting return values for the mocked methods
        aws_client.s3_client.delete_object.return_value = None

        # running the actual method
        response = aws_client.delete_file_from_cloud('key')

        # asserting values
        assert aws_client.s3_client.delete_object.called
        assert response is None

    def test_download_file_from_cloud(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.s3_client.download_file = Mock()

        # setting return values for the mocked methods
        aws_client.s3_client.download_file.return_value = None

        # running the actual method
        response = aws_client.download_file_from_cloud('key', 'filename')

        # asserting values
        assert aws_client.s3_client.download_file.called
        assert response is None

    def test_get_image_id(self):
        aws_client = self.get_vht_aws_instance()
        aws_client.ami_version = self.data['ami_version']

        # mocking methods
        aws_client.ec2_client.describe_images = Mock()

        # setting return values for the mocked methods
        aws_client.ec2_client.describe_images.return_value = {
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
        response = aws_client.get_image_id()

        # asserting values
        assert aws_client.ec2_client.describe_images.called
        assert response == 'ami-0c5eeabe11f3a2685'

    def test_get_instance_state(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.ec2_client.describe_instances = Mock()

        # setting return values for the mocked methods
        aws_client.ec2_client.describe_instances.return_value = {
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
        response = aws_client.get_instance_state()

        # asserting values
        assert aws_client.ec2_client.describe_instances.called
        assert response == 'running'

    @unittest.skip('Find out how to mock s3_resource.Object.get')
    def test_get_s3_file_content(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        # setting return values for the mocked methods
        aws_client.s3_resource.Object('s3_bucket_name', 'key').get = Mock(
            return_value="drwxr-xr-x  13 root root  4096 Apr 30  2021 var"
        )

        # running the actual method
        response = aws_client.get_s3_file_content('key')

        # asserting values
        assert aws_client.s3_resource.Object.called
        assert response == "drwxr-xr-x  13 root root  4096 Apr 30  2021 var"

    def test_get_s3_ssm_command_id_key(self):
        aws_client = self.get_vht_aws_instance()

        command_id = '8f181e5d-8fec-45fa-9bfa-812e76df650c'
        output_type = 'stdout'

        response = aws_client.get_s3_ssm_command_id_key(command_id, output_type)
        expected_response = f"{self.data['s3_keyprefix']}/{command_id}/{self.data['instance_id']}/awsrunShellScript/0.awsrunShellScript/{output_type}"

        assert response == expected_response, \
            f"response = {response} :: expected_response = {expected_response}"

    def test_get_ssm_command_id_status(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.ssm_client.list_commands = Mock()

        # setting return values for the mocked methods
        aws_client.ssm_client.list_commands.return_value = {
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
        response = aws_client.get_ssm_command_id_status(
            command_id='8f181e5d-8fec-45fa-9bfa-812e76df650c'
        )

        # asserting values
        assert aws_client.ssm_client.list_commands.called
        assert response == 'Success'

    def test_get_ssm_command_id_status_details(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.ssm_client.get_command_invocation = Mock()

        # setting return values for the mocked methods
        aws_client.ssm_client.get_command_invocation.return_value = {
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
        response = aws_client.get_ssm_command_id_status_details(
            command_id='8f181e5d-8fec-45fa-9bfa-812e76df650c'
        )

        # asserting values
        assert aws_client.ssm_client.get_command_invocation.called
        assert response == 'Success'

    def test_get_ssm_command_id_stdout_url(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.ssm_client.list_command_invocations = Mock()

        # setting return values for the mocked methods
        aws_client.ssm_client.list_command_invocations.return_value = {
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
        response = aws_client.get_ssm_command_id_stdout_url(
            command_id='da584039-585c-4fd7-b30f-fad58c42c881'
        )

        # asserting values
        assert aws_client.ssm_client.list_command_invocations.called
        assert response == 'https://s3.eu-west-1.amazonaws.com/gh-orta-vht/ssm/da584039-585c-4fd7-b30f-fad58c42c881/i-000f2435623398464/awsrunShellScript/0.awsrunShellScript/stdout'

    def test_get_ssm_command_id_stderr_url(self):
        aws_client = self.get_vht_aws_instance()

        # mocking methods
        aws_client.ssm_client.list_command_invocations = Mock()

        # setting return values for the mocked methods
        aws_client.ssm_client.list_command_invocations.return_value = {
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
        response = aws_client.get_ssm_command_id_stderr_url(
            command_id='da584039-585c-4fd7-b30f-fad58c42c881'
        )

        # asserting values
        assert aws_client.ssm_client.list_command_invocations.called
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
