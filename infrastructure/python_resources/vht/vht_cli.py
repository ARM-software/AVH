#!/usr/bin/env python

from vht import vht_core
from vht import vht_utils
import argparse
import ast
import json
import logging

def main():
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-ec2-instance',
                        nargs='*',
                        help='Create a ARM Virtual Hardware Instance')
    parser.add_argument('--download-s3-file',
                        nargs='*',
                        help='Download an S3 file')
    parser.add_argument('--get-ami-id',
                        type=str,
                        help='Get the VHT AMI ID for your AWS region')
    parser.add_argument('--get-ec2-instance-state',
                        type=str,
                        help='Get the EC2 instance state')
    parser.add_argument('--get-s3-file-content',
                        nargs='*',
                        help='Get the S3 file content')
    parser.add_argument('--get-s3-ssm-command-id-key',
                        nargs='*',
                        help='Get the S3 Key from a SSM Output')
    parser.add_argument('--get-ssm-command-id-status',
                        type=str,
                        help='Get SSM Command ID status')
    parser.add_argument('--send-ssm-shell-command',
                        nargs='*',
                        help='Send a shell command to a instance by SSM')
    parser.add_argument('--start-ec2-instance',
                        type=str,
                        help='Start the EC2 instance')
    parser.add_argument('--stop-ec2-instance',
                        type=str,
                        help='Stop the EC2 instance')
    parser.add_argument('--terminate-ec2-instance',
                        type=str,
                        help='Terminate the EC2 instance')
    parser.add_argument('--wait-ssm-command-finished',
                        nargs="*",
                        help='Wait until a SSM command is finished')
    parser.add_argument('-v', '--verbosity',
                        type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Set the output verbosity DEBUG, INFO, WARNING, ERROR')
    parser.parse_args()
    args = parser.parse_args()

    ########### BEGIN VARIABLES ###################################################
    # Set verbosity level
    if args.verbosity:
        verbosity = args.verbosity
        level = { "DEBUG": 10, "INFO": 20, "WARNING" : 30, "ERROR" : 40 }
        logging.basicConfig(format='[%(levelname)s]\t%(message)s', level = verbosity)
        logging.debug("Verbosity level is set to " + verbosity)


    def process_kwargs_cli(args):
        logging.debug(args.arg_name)
        map_args = {}
        for i_args in args.create_ec2_instance:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

        logging.debug("map = {}".format(map_args))

    ########### END VARIABLES #####################################################

    # core_instance = vht_core.VhtCore(s3_bucket_name, s3_keyprefix)
    core_instance = vht_core.VhtCore()

    if args.create_ec2_instance:
        # TODO: Add support to create tags. Complicated parsing.
        logging.info("Creating instance...")
        logging.debug(args.create_ec2_instance)
        map_args = {}
        for i_args in args.create_ec2_instance:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

        logging.debug("map = {}".format(map_args))
        print(core_instance.create_ec2_instance(**map_args))

    if args.download_s3_file:
        map_args = {}
        for i_args in args.download_s3_file:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

        core_instance.download_s3_file(map_args['s3BucketName'], map_args['key'], map_args['filename'])

    if args.get_ami_id:
        print(core_instance.get_ami_id(args.get_ami_id))

    if args.get_ec2_instance_state:
        print(core_instance.get_ec2_instance_state(args.get_ec2_instance_state))

    if args.get_s3_file_content:
        map_args = {}
        for i_args in args.get_s3_file_content:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

        print(core_instance.get_s3_file_content(map_args['s3BucketName'], map_args['key']))

    if args.get_s3_ssm_command_id_key:
        map_args = {}
        for i_args in args.get_s3_ssm_command_id_key:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

        print(core_instance.get_s3_ssm_command_id_key(map_args['InstanceId'],
                                                    map_args['CommandId'],
                                                    map_args['s3KeyPrefix'],
                                                    map_args['OutputType']))

    if args.get_ssm_command_id_status:
        print(core_instance.get_ssm_command_id_status(args.get_ssm_command_id_status))

    if args.send_ssm_shell_command:
        map_args = {}
        for i_args in args.send_ssm_shell_command:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

            # print(map_args.keys())
            if 'workingDir' not in map_args.keys():
                map_args['workingDir'] = '/'
            if 'outputType' not in map_args.keys():
                map_args['outputType'] = 'command_id'
            if 'timeoutSeconds' not in map_args.keys():
                map_args['timeoutSeconds'] = 600

        print(core_instance.send_ssm_shell_command(map_args['InstanceId'],
                                                map_args['commandList'],
                                                map_args['s3BucketName'],
                                                map_args['s3KeyPrefix'],
                                                map_args['workingDir'],
                                                map_args['outputType'],
                                                map_args['timeoutSeconds']))

    if args.start_ec2_instance:
        core_instance.start_ec2_instance(args.start_ec2_instance)

    if args.stop_ec2_instance:
        core_instance.stop_ec2_instance(args.stop_ec2_instance)

    if args.terminate_ec2_instance:
        core_instance.terminate_ec2_instance(args.terminate_ec2_instance)

    if args.wait_ssm_command_finished:
        map_args = {}
        for i_args in args.wait_ssm_command_finished:
            logging.debug(i_args)
            key, value = i_args.split('=')
            logging.debug(type(value))

            # convert a string to a list
            if value[0] == '[':
                value = value.strip('[]').split(', ')
            # convert a string to a dict
            elif value[0] == '{':
                json_acceptable_string = value.replace("'", "\"")
                value = json.loads(json_acceptable_string)
                isinstance(value, dict)
            # convert a string to a number
            elif value.isdigit():
                value = int(value)

            logging.debug(type(value))
            map_args[key] = value

            # print(map_args.keys())
            if 'delay' not in map_args.keys():
                map_args['delay'] = 5
            if 'max_attempts' not in map_args.keys():
                map_args['max_attempts'] = 120

        core_instance.wait_ssm_command_finished(map_args['InstanceId'], map_args['CommandId'])

if __name__ == '__main__':
    main()
