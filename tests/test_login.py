import unittest
from authentication import LogIn
from test_base import captured_io, captured_output
from io import StringIO
from file_handling.files import *
from config.config import *
from helpers.writer import *
from authentication.LogIn import *

class TestLogin(unittest.TestCase):

    def test_login_return_type(self):
        data = {"email": 'test@gmail.com',"password":'1234'}

        with captured_io(StringIO('1234\n')) as (out,err):
            output = login(data)
            self.assertIsInstance(output,tuple)
            self.assertIsInstance(output[0],bool)
            self.assertIsInstance(output[1],list)


    def test_login_correct_pass(self):
        data = {"email": 'test@gmail.com',"password":'1234'}
        time.strftime = lambda a: '2021-09-01 10:54:28 +0200'
        exp = '2021-09-01 14:54:28 +0200'

        with captured_io(StringIO('1234\n')) as (out,err):
            output = login(data)
            returned_data = output
            expected_out = f'Login successful. Token expires in 0 days 3 hours 59 minutes at {exp}'
            output = out.getvalue().strip()
            self.assertEqual(expected_out,output)
            self.assertTrue(returned_data[0])
            self.assertEqual(returned_data[1],['2021-09-01 10:54:28 +0200','2021-09-01 14:54:28 +0200'])

    def test_login_incorrect_pass(self):
        data = {"email": 'test@gmail.com',"password":'None'}
        time.strftime = lambda a: '2021-09-01 10:54:28 +0200'
        exp = '2021-09-01 14:54:28 +0200'

        with captured_io(StringIO('1234\n')) as (out,err):
            output = login(data)
            returned_data = output
            expected_out = f'login failed for {data["email"]} because Server returned error response'
            output = out.getvalue().strip()
            self.assertEqual(expected_out,output)
            self.assertFalse(returned_data[0])
            self.assertEqual(returned_data[1],['',''])


    def test_empty_pass(self):
        data = {"email": 'test@gmail.com',"password":'None'}
        time.strftime = lambda a: '2021-09-01 10:54:28 +0200'
        exp = '2021-09-01 14:54:28 +0200'

        with captured_io(StringIO('\n')) as (out,err):
            output = login(data)
            returned_data = output
            expected_out = f'Login successful. Token expires in 0 days 3 hours 59 minutes at {exp}'
            output = out.getvalue().strip()
            self.assertEqual(expected_out,output)

class TestToken(unittest.TestCase):

    def test_token_exp_single(self):

        with captured_output() as (out,err):
            # single digit hour (06)
            login_time = '2021-09-01 06:54:28 +0200'
            expected_out = '2021-09-01 10:54:28 +0200'
            output = token_exp(login_time)
            self.assertIsInstance(output,str)
            self.assertEqual(expected_out,output)

    def test_exp_next_day(self):

        with captured_output() as (out,err):
            login_time = '2021-09-01 23:54:28 +0200'
            expected_out = '2021-09-02 03:54:28 +0200'
            output = token_exp(login_time)
            self.assertEqual(expected_out,output)

    def test_exp_midnight_hour_fix(self):

        with captured_output() as (out,err):
            login_time = '2021-09-01 20:54:28 +0200'
            expected_out = '2021-09-02 00:54:28 +0200'
            output = token_exp(login_time)
            self.assertEqual(expected_out,output)

    def test_token_return_True(self):

        path = 'tests/data_for_test/token_data/.logIn_token.json'
        folder = {"usertmp":"tests/data_for_test/token_data"}
        data = {'email':'test@gmail.com'}
        expected_out = f"""Token not present: for user test@gmail.com: No matching entry found in secure storage.

Please login using

  code-clinic login
    """
        # check_token = check_token(path,,folder)
        # with self.assertRaises(SystemExit) as exit_code:
        #     output = check_token.g
        # with captured_output() as (out,err):
        with self.assertRaises(SystemExit) as cm:
            check_token(path,data,folder)
            # output = out.getvalue()
            # print(cm.msg)
            self.assertNotEqual(cm.exception.code,expected_out)
            print(cm.exception.args[0])
            




if __name__ == '__main__':
    unittest.main()
