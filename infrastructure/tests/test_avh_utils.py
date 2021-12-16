import unittest
import os

from avh_cli.avh_utils import AvhUtils


class TestAvhUtils(unittest.TestCase):
    def test_is_aws_credentials_present(self):
        utils = AvhUtils()
        utils.is_aws_credentials_present()


if __name__ == '__main__':
    unittest.main()
