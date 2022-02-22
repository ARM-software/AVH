# VHT python resources

Python module and CLI which interact with VHT. The main goal is to provide CIs and the end-user tools to easily manipulate VHT tasks.
The VHTClient() (from vht.py file) provides the front-end APIs.
For now, only `aws` backend is implemented.

There are two main Python components:
* `VHT Python module` which can be imported into your Python code to create / manage / terminate VHT Instances
* `VHT CLI` is a command-line interface for VHT Python Module

## How to Install
* Clone this repo `git clone https://github.com/ARM-software/VHT.git`
* Go to `infrastructure/python_resources` folder
* `pip install .`

## How to run VHT module
```
from vht import vht

vht.VHTClient("aws").run()
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
Tests for the VHT Python Module. Running unittests locally (please install tox `pip install tox`):
```
tox -c tox_unittest.ini
```

### vht
VHT python packages which includes:
* `vht_cli.py`: VHT Command Line Interface tool
* `aws.py`: AWS backend that provides methods to quickly and easily create/delete/interact with VHT intances in AWS
* `vht.py`: Front end class which exposes all methods available for the user.

## Examples using VHT Python Module
* [Jenkins](https://github.com/ARM-software/VHT-GetStarted/blob/main/.jenkins/Using-VHT-Module/pipeline/Jenkinsfile)
* [GitHub Action](https://github.com/ARM-software/VHT-AMI/blob/master/vht_github_action.py)

## Examples using VHT CLI
* [tests/examples](https://github.com/ARM-software/VHT/blob/main/infrastructure/python_resources/tests/examples)
* [tests/test_vht_cli.sh](https://github.com/ARM-software/VHT/blob/main/infrastructure/python_resources/tests/test_vht_cli.sh)
