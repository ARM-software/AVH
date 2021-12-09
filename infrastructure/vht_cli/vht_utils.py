import os
import logging
import sys
import uuid

class AvhUtils():
    def __init__(self):
        pass

    def is_aws_credentials_present(self):
        """
            Verifies presence of AWS Credentias as Environment Variables.
            AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are mandatory
            AWS_SESSION_TOKEN is optional for IAM User credentials.
        """
        if (os.environ.get('AWS_ACCESS_KEY_ID') is None):
            logging.info("AWS_ACCESS_KEY_ID environment variable not present!")
            sys.exit(1)
        else:
            logging.debug('AWS_ACCESS_KEY_ID present!')

        if (os.environ.get('AWS_SECRET_ACCESS_KEY') is None):
            logging.info("AWS_SECRET_ACCESS_KEY environment variable not present!")
            sys.exit(1)
        else:
            logging.debug('AWS_SECRET_ACCESS_KEY present!')

        if (os.environ.get('AWS_SESSION_TOKEN') is None):
            logging.debug('AWS_SESSION_TOKEN environment variable not present!')
            logging.debug('It is expected for an IAM User')
        else:
            logging.debug('AWS_SESSION_TOKEN present!')

    def teardown(self, vht_core, instance_id, terminate_ec2_instance):
        # if terminate_ec2_instance is True Terminate Otherwise Stop instance
        if (terminate_ec2_instance):
            vht_core.terminate_ec2_instance(instance_id)
        else:
            vht_core.stop_ec2_instance(instance_id)
