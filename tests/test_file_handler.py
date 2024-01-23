import unittest
from test_base import captured_io, captured_output
from io import StringIO
from file_handler import *
import os

class Test_data_generation(unittest.TestCase):
    
    def test_correct_output(self):
        name = 'james023'
        email = 'james023@student.wethinkcode.co.za'
        password = '123'
        with captured_io(StringIO(f'{name}\n{email}\n{password}\n{password}\n')) as (out,err):
            data = generating_logIn_cred()
            self.assertEqual(data['username'],name)
            self.assertEqual(data['email'],email)
            self.assertEqual(data['password'],password)

    
    def test_function_data_type(self):
        name = 'james023'
        email = 'james023@student.wethinkcode.co.za'
        password = '123'
        with captured_io(StringIO(f'{name}\n{email}\n{password}\n{password}\n')) as (out,err):
            data = generating_logIn_cred()
            self.assertIsInstance(data,dict)
            self.assertEqual(len(data),3)
    
    def test_function_incorrect_type(self):
        name = 'james023'
        email = 'james023@student.wethinkcode.co.za'
        password = '123'
        expected_output = '''Enter your username: Enter your email: Enter passphrase: Enter same passphrase: Passphrases do not match. Try again.
\nEnter passphrase: Enter same passphrase:'''
        with captured_io(StringIO(f'{name}\n{email}\n{password}\n12345\n{password}\n{password}')) as (out,err):
            data = generating_logIn_cred()
            output = out.getvalue().strip()
            self.assertEqual(expected_output,output)


    def test_no_passphrase(self):
        name = 'james023'
        email = 'james023@student.wethinkcode.co.za'
        password = ''
        with captured_io(StringIO(f'{name}\n{email}\n{password}\n{password}\n')) as (out,err):
            data = generating_logIn_cred()
            self.assertIsNone(data['password'])

    

class Test_Config_File(unittest.TestCase):
    
    def test_write_data(self):
        path = 'tests/test_config.json'
        name = 'johndoe023'
        email = 'johndoe023@student.wethinkcode.co.za'
        password = '1234'
        with captured_io(StringIO(f'{name}\n{email}\n{password}\n{password}\n')) as (out,err):
            data = generating_logIn_cred()
            write_config(data,path)
            folder = [file for file in os.listdir('tests') if file == 'test_config.json']
            self.assertEqual(len(folder),1)
    
    def test_read_data(self):
        path = 'tests/test_config.json'
        name = 'johndoe023'
        email = 'johndoe023@student.wethinkcode.co.za'
        password = '1234'
        with captured_output() as (out,err):
            data = read_config(path)
            self.assertIsInstance(data,dict)
            self.assertEqual(data['username'],name)
            self.assertEqual(data['email'],email)
            self.assertEqual(data['password'],password)
            
            
           
            
    
    
    
if __name__ == '__main__':
    unittest.main()
    