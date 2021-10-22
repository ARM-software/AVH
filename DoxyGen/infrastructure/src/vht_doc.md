# VHT CLI Script

This script is a wrapper around AWS CLI to start/connect/stop \ref AWS EC2 instance easily.

## Requirements

* Python 3
* AWS CLI. The latest version of the AWS CLI can be downloaded [here for linux](https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip) or [here for Windows](https://awscli.amazonaws.com/AWSCLIV2.msi).

## Usage

This script can be used with one of the argument below:

* `./vht_cli.py start`: to launch an Arm Virtual Hardware AMI instance. If an instance is already running, the user will be asked to confirm a new instance needs to be launched.
* `./vht_cli.py status`: to display an Arm Virtual Hardware AMI instance(s) status and get the instance(s) IP address.
* `./vht_cli.py stop`: to terminate an Arm Virtual Hardware AMI instance. The user will be asked to confirm the instance ID to terminate. Note that the data stored in the instance will be lost.

The script supports additional options:

* `-p` to specify the name of the AWS profile to use (default is `default`).
* `-r` to specify the AWS region where the instance should be launched (default is `us-east-1`).
* `-k` to specify the AWS key name to use. If no key is provided, the script will create a "avh\_user" key.
* `-h` to display help.

Note that the script will create a default Amazon Virtual Private Cloud (VPC) if this is has not been configured for the account and region.

## Usage examples

### Instance start wihout specifying any key

```
$ ./vht_cli.py start
[INFO]	No key specified and avh_user key not found, creating 'avh_user' key...
[INFO]	Key has been saved as /home/<user>/.ssh/avh_user.pem.
Starting Arm Virtual Hardware AWS EC2 instance...
Launched Instance ID i-XXXXXXXXXXXXXXXX
```

### Connecting to the instance

When an instance has been started, with the vht\_cli.py script, its IP address can be retrieved with:

```
$ ./vht_cli.py status
| Instance ID         | Public IP        | Status     |
=======================================================
| i-XXXXXXXXXXXXXXXX  | Y.YYY.YYY.YYY    | RUNNING    |
```


### Instance stop

```
$ ./vht_cli.py stop
Running instance ID i-XXXXXXXXXXXXXXXX found (public IP Y.YYY.YYY.YYY)
The instance will be terminated and all data will be lost. Please enter the instance ID to stop it (leave empty to cancel): i-XXXXXXXXXXXXXXXX
Stopping ORTA instance ID i-XXXXXXXXXXXXXXXX...
```
