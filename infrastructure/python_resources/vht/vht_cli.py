#!/usr/bin/env python

import argparse
import json
import logging
from vht import vht

def main():
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--create_instance',
                        action='store_true',
                        help='Create a new VHT instance')
    parser.add_argument('--delete_file_from_cloud',
                        type=str,
                        nargs=1,
                        help='Delete a file from cloud')
    parser.add_argument('--download_file_from_cloud',
                        nargs=2,
                        help='Download a file from clould')
    parser.add_argument('--get_image_id',
                        action='store_true',
                        help='Get the image id')
    parser.add_argument('--get_instance_state',
                        action='store_true',
                        help='Get instance state')
    parser.add_argument('--get_process_vht_commands',
                        action='store_true',
                        help='Get process VHT commands to be executed on the instance')
    parser.add_argument('--run',
                        action='store_true',
                        help='Run VHT commands to the instance with default values')
    parser.add_argument('--send_remote_command',
                        nargs='*',
                        help='Send/Execute remote commands to a instance')
    parser.add_argument('--send_remote_command_batch',
                        nargs='*',
                        help='Send/Execute multiple remote commands to a instance')
    parser.add_argument('--start_instance',
                        action='store_true',
                        help='Start instance (if instance_id info is provided)')
    parser.add_argument('--stop_instance',
                        action='store_true',
                        help='Stop instance')
    parser.add_argument('--terminate_instance',
                        action='store_true',
                        help='Terminate instance')
    parser.add_argument('--teardown',
                        action='store_true',
                        help='Terminate (if flag enabled) or stop instance')
    parser.add_argument('--upload_file_to_cloud',
                        nargs=2,
                        help='Terminate (if flag enabled) or stop instance')
    parser.add_argument('-v', '--verbosity',
                        type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Set the output verbosity DEBUG, INFO, WARNING, ERROR. Default: `INFO`')
    parser.add_argument('-b', '--backend',
                        type=str,
                        choices=['aws'],
                        default='aws',
                        help='Select your aws. Default: `aws`')
    parser.parse_args()
    args = parser.parse_args()
    if args.verbosity:
        verbosity = args.verbosity
        level = { "DEBUG": 10, "INFO": 20, "WARNING" : 30, "ERROR" : 40 }
        logging.basicConfig(format='[%(levelname)s]\t%(message)s', level = verbosity)
        logging.debug("Verbosity level is set to " + verbosity)

    # vht_instance using args.backend
    vht_client = vht.VHTClient(args.backend)

    if args.create_instance:
        print(vht_client.create_instance())
    if args.delete_file_from_cloud:
        key = args.delete_file_from_cloud[0]
        vht_client.delete_file_from_cloud(key)
    if args.download_file_from_cloud:
        filename = args.download_file_from_cloud[0]
        key = args.download_file_from_cloud[1]
        vht_client.download_file_from_cloud(filename, key)
    if args.get_image_id:
        print(vht_client.get_image_id())
    if args.get_instance_state:
        print(vht_client.get_instance_state())
    if args.get_process_vht_commands:
        print(vht_client.get_process_vht_commands())
    if args.run:
        vht_client.run()
    if args.send_remote_command:
        # TODO
        pass
    if args.send_remote_command_batch:
        # TODO
        pass
    if args.start_instance:
        vht_client.start_instance()
    if args.stop_instance:
        vht_client.stop_instance()
    if args.terminate_instance:
        vht_client.terminate_instance()
    if args.teardown:
        vht_client.teardown()
    if args.upload_file_to_cloud:
        filename = args.upload_file_to_cloud[0]
        key = args.upload_file_to_cloud[1]
        vht_client.upload_file_to_cloud(filename, key)

if __name__ == '__main__':
    main()
