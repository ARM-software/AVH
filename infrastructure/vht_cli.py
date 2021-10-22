#!/usr/bin/env python

'''
Copyright 2021 Arm Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


import argparse
import sys
import os
import subprocess
import json
import logging
import platform


# Arm Virtual Hardware AMI version
avh_version="1.0.0"

InstType="c5.large"

# Set verbosity level
verbosity = logging.INFO
# [debugging] Verbosity settings
level = { 10: "DEBUG",  20: "INFO",  30: "WARNING",  40: "ERROR" }
logging.basicConfig(format='[%(levelname)s]\t%(message)s', level = verbosity)
logging.debug("Verbosity level is set to " + level[verbosity])

# No colors for Windows
if platform.system() == "Windows" : 
    green=""
    orange=""
    red=""
    nc=""
else:
    green="\033[0;32m"
    orange="\033[0;33m"
    red="\033[0;31m"
    nc="\033[0m"


def get_avh_imgid(region):
    global avh_version

    cmd_im = "aws ec2 describe-images --region {} --filters Name=name,Values='ArmVirtualHardware-{}*' Name=owner-alias,Values='aws-marketplace' --output json".format(
    	    region, avh_version)

    try:
        out_im = subprocess.check_output(cmd_im, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        logging.error(red + "Could not get Arm Virtual Hardware Instance ID for region {}.".format(region) + nc)
        sys.exit(1)

    outd_im = json.loads(out_im)
    for instance in outd_im['Images']:
        ImgId = instance['ImageId']
        logging.info("Image ID is {}".format(ImgId))

    return ImgId


def start_avh(profile, key, region, initfile):
    global InstType

    print("Starting AVH instance...")

    [n, arr, ImgId] = status_avh(profile, region, False)

    if n > 0 :
        print(orange + "One or more AVH instances are already running." + nc)
        confirm = input("Please confirm to launch a new instance [Y/n]: ")
        if confirm != "Y":
            print("Cancelling... No instance will be started.")
            sys.exit(1)

    cmd = "aws ec2 run-instances --profile {} --image-id {} --instance-type {} --key-name {} --region {} --output json".format(
            profile, ImgId, InstType, key, region)

    if initfile != None :
        cmd = cmd + " --user-data file://{}".format(initfile.name)

    logging.debug("Command is: {}".format(cmd))

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(e.output)
        errtype = str(e.output).split(")")[0].split("(")[1]
        if errtype == "VPCIdNotSpecified":
            logging.info(orange + "Running the start command failed: default VPC not found. Creating VPC..." + nc)

            cmd_vpc = "aws ec2 create-default-vpc --profile {} --region {}".format(
	    	profile, region)

            try:
                out_vpc = subprocess.check_output(cmd_vpc, shell=True).decode("utf-8")
            except subprocess.CalledProcessError:
                logging.error(red + "VPC creation failed." + nc)
                sys.exit(1)

            logging.info("VPC created. Trying to start instance again...")

            try:
                out = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except subprocess.CalledProcessError as e:
                logging.error(red + "Running the start command failed." + nc)
            sys.exit(1)
        else:
            logging.error(red + "Running the start command failed." + nc)
            sys.exit(1)

    outd = json.loads(out)
    for instance in outd['Instances']:
        print("Launched Instance ID {}".format(instance['InstanceId']))

    return

def status_avh(profile, region, printv):
    # Get ImageID from region
    ImgId = get_avh_imgid(region)

    n_instances = 0
    arr_inst = []

    cmd = 'aws ec2 describe-instances --query "Reservations[*].Instances[*].[State.Name, ImageId, PublicIpAddress, InstanceId]" --profile {} --region {} --output json'.format(profile, region)

    logging.debug("Command is: {}".format(cmd))

    try:
        out = subprocess.check_output(cmd, shell=True).decode("utf-8")
    except subprocess.CalledProcessError:
        logging.error(red + "Running the status command failed." + nc)
        sys.exit(1)

    outd = json.loads(out)
    for reservation in range(len(outd)):
        for instance in range(len(outd[reservation])):
            if outd[reservation][instance][1] == ImgId :
                if outd[reservation][instance][0] == 'running' :
                    n_instances += 1
                arr_inst.append([outd[reservation][instance][3], outd[reservation][instance][2], outd[reservation][instance][0]])

    if printv == True :
        print("| Instance ID\t\t| Public IP\t| Status\t|")
        print('=========================================================')
        for i in arr_inst :
            if i[2] == 'running' :
                print("| {}\t| {}\t| ".format(i[0], i[1]) + green + "RUNNING" + nc + "\t|")
            elif i[2] == 'shutting-down' :
                print("| {}\t| {}\t| ".format(i[0], i[1]) + red + "SHUTTING DOWN" + nc + "\t|")
            elif i[2] == 'pending' :
                print("| {}\t| {}\t| ".format(i[0], i[1]) + orange + "{}".format(i[2]) + nc + "\t|")
            else :
                print("| {}\t| {}\t\t| {}\t|".format(i[0], i[1], i[2]))

    return n_instances, arr_inst, ImgId


def stop_avh(profile, region):
    [n, arr, ImgId] = status_avh(profile, region, False)

    if n == 0 :
        logging.error(red + "No AVH instance is running." + nc)
        sys.exit(1)
    else:
        if n > 1:
            print(orange + "Many instances found!" + nc)

        for i in arr :
            if i[2] == 'running' :
                print("Running instance ID {} found (public IP {})".format(i[0], i[1]))

        instanceid = input(orange + "The instance will be terminated and all data will be lost. " + nc + "Please enter the instance ID to stop it (leave empty to cancel): ")

        if(instanceid == ""):
            print("Cancelling... No instance will be stopped.")
        else:
            print(orange + "Stopping AVH instance ID {}...".format(instanceid) + nc)

            cmd = "aws ec2 terminate-instances --profile {} --instance-ids {} --region {}".format(
                    profile, instanceid, region)

            try:
                out = subprocess.check_output(cmd, shell=True).decode("utf-8")
            except subprocess.CalledProcessError:
                logging.error(red + "Running the stop command failed." + nc)

            logging.debug("Command is: {}".format(cmd))
            return


# Command options
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AVH command-line interface for AWS. Starts (launches) a single AVH AMI instance and stops (terminates) it.")
    parser.add_argument("-p", dest="profile", metavar="NAME", action="store", type=str, help=("Name of the profile configuration (default is 'default')"), default="default")
    parser.add_argument("-k", dest="key", metavar="KEY", action="store", type=str, help=("Name of the AWS key. If not specified, a key will be created"))
    parser.add_argument("-r", dest="region", metavar="REGION", action="store", type=str, help=("Name of the AWS region (default is 'us-east-1')"), default="us-east-1")
    parser.add_argument("-i", dest="cloudinit", metavar="FILE", action="store", type=argparse.FileType('r'), help=("Location of cloud-init file for instance configuration"))
    parser.add_argument("command", metavar="start|status|stop", action="store", type=str, help=("Start, status or stop command"))
    args = parser.parse_args()

    # Check AWS CLI is installed
    try:
        awscli_version_f = subprocess.check_output("aws --version", shell=True).decode("utf-8").split()[0].split("/")[1]
    except subprocess.CalledProcessError:
        logging.error(red + "AWS CLI not found." + nc)
        sys.exit(1)

    # AWS CLI version check
    awscli_version_m = float(awscli_version_f.split(".")[0] + "." + awscli_version_f.split(".")[1])
    if awscli_version_m < 2.2 :
        logging.warning(orange + "AWS CLI version is: {}. Minimum required is 2.2".format(awscli_version_m) + nc)

    # Profile check
    try:
        awscli_version_f = subprocess.check_output(
                "aws configure list --profile {}".format(args.profile), 
                shell=True)
    except subprocess.CalledProcessError:
        logging.error(red  + "Profile {} not found.".format(args.profile) + nc)
        sys.exit(1)

    if args.profile == "default" :
        logging.info("Selected profile: {}".format(args.profile))


    # Start / Stop / Status commands
    if args.command.lower() == "start" :
        # Key check
        if args.key == None:
            args.key = "avh_user_{}".format(args.region)
            if os.path.isfile(os.path.join(os.path.expanduser('~'),'.ssh/avh_user_{}.pem'.format(args.region))) == False :
                logging.info(orange + "No key specified and avh_user_{} key not found, creating 'avh_user_{}' key...".format(args.region, args.region) + nc)

                cmd = "aws ec2 create-key-pair --key-name avh_user_{} --profile {} --region {} --output json".format(
                            args.region, args.profile, args.region)
                try:
                    out = subprocess.check_output(cmd, shell=True).decode("utf-8")
                except subprocess.CalledProcessError:
                    logging.error(red + "Creating a key failed." + nc)
                    sys.exit(1)

                outd = json.loads(out)
                key_file = open(os.path.join(os.path.expanduser('~'),'.ssh/avh_user_{}.pem'.format(args.region)), 'x')
                try:
                    key_file.write(outd["KeyMaterial"])
                except:
                    logging.error(red + "Saving key in {}.ssh failed.".format(os.path.expanduser('~') + os.path.sep) + nc)
                    sys.exit(1)

                key_file.close()

                # Set permissions
                if platform.system() == "Linux" :
                    os.system('chmod 600 ~/.ssh/avh_user_{}.pem'.format(args.region))

                logging.info(orange + "Key has been saved as {}.ssh".format(os.path.expanduser('~') + os.path.sep) 
		    + os.path.sep + "avh_user_{}.pem.".format(args.region) + nc)
            else:
                logging.info(orange + "Using 'avh_user_{}' key in {}.ssh ...".format(args.region, os.path.expanduser('~') + os.path.sep) + nc)

        start_avh(args.profile, args.key, args.region, args.cloudinit)

    elif args.command.lower() == "status" :
        status_avh(args.profile, args.region, True)

    elif args.command.lower() == "stop" :
        stop_avh(args.profile, args.region)

    else :
        logging.error(red + "Unknown command." + nc)

    sys.exit(0)

