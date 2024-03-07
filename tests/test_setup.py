import unittest
from test_base import captured_output
from file_handling.files import *
from config.config import *
from helpers.writer import *
from encrypt.encryption import *
from os.path import isdir, join,exists
from setup import *


class TestSetup(unittest.TestCase):

    def test_gen_secure_folder(self):
        files.get_home = lambda : 'tests/data_for_test/secure_home'
        folders = {
            "main": 'tests/data_for_test/secure_home/.elite',
            "auth": 'tests/data_for_test/secure_home/.elite/.profile369/.access',
            "recon": 'tests/data_for_test/secure_home/.elite/.profile369/.recon',
            "key": 'tests/data_for_test/secure_home/.elite/.profile369/.elite',
            "user": 'tests/data_for_test/secure_home/.elite/.profile369',
            "tmp": '/tmp/.xyzabchijklmnop',
            "usertmp": '/tmp/.xyzabchijklmnop/.profile369'
        }

        # with captured_output as (out,err):
        output = secure_folder('profile369')
        self.assertIsInstance(output,dict)
        self.assertEqual(list(folders.values()),list(output.values()))

        for key, value in output.items():
            self.assertTrue(exists(output[key]),'dir does not exist')
            self.assertTrue(isdir(output[key]),'not a dir')





if __name__ == '__main__':
    unittest.main()
