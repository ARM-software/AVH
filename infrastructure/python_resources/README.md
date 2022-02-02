# VHT python resources

Python resources which interact with VHT and AWS resources (initially). The main goal is to provide CIs and the end-user tools a way to easily implement VHT-related tasks.

There are two main Python components:
* `VHT Python module` which can be imported into your Python code to create / manage / terminate VHT Instances
* `VHT CLI` is a command-line interface for VHT Python Module

## How to Install
* Clone this repo `git clone https://github.com/ARM-software/VHT.git`
* Go to `infrastructure/python_resources` folder
* `pip install .`

## How to import VHT module
```
from vht import vht_core
from vht import vht_utils

# Instances
core_instance = vht_core.VhtCore()
utils_instance = vht_utils.VhtUtils()
```

## How to control log verbosity
### VHT module

Add this to the Python code
```
verbosity = 'INFO'
level = { "DEBUG": 10, "INFO": 20, "WARNING" : 30, "ERROR" : 40 }
logging.basicConfig(format='[%(levelname)s]\t%(message)s', level = verbosity)
logging.debug("Verbosity level is set to " + verbosity)
```

### VHT CLI
You can use the `-v` option:
```
vht_cli -v 'INFO' --get-ami-id '1.0.0'
```

## Folder content
### tests
Tests for the VHT Python Module

### vht
VHT python packages which includes:
* `vht_cli`: VHT Command Line Interface tool
* `vht_core`: Python Module which wraps AWS calls and provide methods to quickly and easily create/delete/interact with VHT intances in AWS
* `vht_utils`: Helper methods for `vht_cli`

## Examples using VHT Python Module
* [Jenkins](https://github.com/ARM-software/VHT-GetStarted/blob/main/.jenkins/Using-VHT-Module/pipeline/Jenkinsfile)
* [GitHub Action](https://github.com/ARM-software/VHT-AMI/blob/master/vht_github_action.py)

## Examples using VHT CLI
* [tests/examples](https://github.com/ARM-software/VHT/blob/main/infrastructure/python_resources/tests/examples)
* [tests/test_vht_cli.sh](https://github.com/ARM-software/VHT/blob/main/infrastructure/python_resources/tests/test_vht_cli.sh)
