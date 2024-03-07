import unittest
from test_base import captured_output
from file_handling.files import *
from config.config import *
from helpers.writer import *
from encrypt.encryption import *
from os.path import isdir, join

class TestFileHandling(unittest.TestCase):
    
    def test_user_dir(self):
        expected_out = os.environ.get("HOME")

        with captured_output() as (out,err):
            output = get_home()
            self.assertEqual(expected_out,output)

    def test_dir_creation(self):
        maindir = 'tests/data_for_test'

        with captured_output() as (out,err):
            create_dir(maindir,'test_dir')
            self.assertTrue(isdir(join(maindir,'test_dir')))

        try:
            os.rmdir(join('tests/data_for_test/test_dir'))
        except Exception as f:
            print(f)
            
    def test_profile_dir_exists(self):

        with captured_output() as (out,err):
            os.path.join = lambda a,b: 'tests/data_for_test/home/.elite'
            output = check_user_profile('profile123')
            self.assertTrue(output)

    def test_profile_dir_not_exist(self):
        
        with captured_output() as (out,err):
            os.path.join = lambda a,b: 'tests/data_for_test/home/.elite'
            output = check_user_profile('test113')
            self.assertFalse(output)

if __name__ == "__main__":
    unittest.main()