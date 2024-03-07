import unittest
from test_base import captured_output
from file_handling.files import *
from config.config import *
from helpers.writer import *
from encrypt.encryption import *
import random
import string
from os.path import isfile,join


class TestEncKEy(unittest.TestCase):

    def test_salt_and_pepper_return(self):

        with captured_output() as (out,err):
            output = generating_salt_and_pepper()
            self.assertEqual(len(output),3)
            self.assertIsInstance(output,tuple)
            self.assertIsInstance(output[0],bytes)
            self.assertIsInstance(output[1],str)
            self.assertIsInstance(output[2],dict)

    def test_pepper_password(self):

        random.randint = lambda a,b: 8
        string.ascii_letters = 'a'

        with captured_output() as (out,err):
            output = generating_salt_and_pepper()

            password = False
            for value in output[2].values():
                if 'aaaaaaaa' == value:
                    password = True

            self.assertEqual(len(output[1]),8)
            self.assertEqual(output[1],'aaaaaaaa')
            self.assertTrue(password)

    def test_key(self):
        salt = b'[\x08\x7fZ\x054\x1a\xc68\xe0s\x02$~#\x03\xc1J\xbe\x00|\xd8q\xb2\x1bT\xe2_\xf3\xd3\xdck'
        pepper = 'aRYRswmfrvtOD'
        expected_out = b'\x1b\xe4$"\x87,!\x15X\xe8~\xef\x87\xd0!W\xc2\xa6I\xf2?+\xe3\x8c_\xff\xb2A\xe6gj\xb7'
        with captured_output() as (out,err):
            output = generate_key(salt,pepper)
            self.assertIsInstance(output,bytes)
            self.assertEqual(expected_out,output)

    def test_writing_key(self):
        key_name = 'testKey'
        key_path = 'tests/data_for_test/enc'
        ext = 'key'
        keybytes = b'The key must be bytes'

        with captured_output() as (out,err):
            save_key(key_path,key_name,ext,keybytes)
            self.assertTrue(isfile(join(key_path,f'{key_name}.{ext}')),'file not created')

    def test_reading_key(self):
        key_name = 'testKey.key'
        key_path = 'tests/data_for_test/enc'
        keybytes = b'The key must be bytes'

        with captured_output() as (out,err):
            try:
                output = read_key(key_path,key_name)
            except:
                pass
            self.assertTrue(isfile(join(key_path,key_name)),'file does not exist. Fix key writing function')
            self.assertIsInstance(output,bytes)
            self.assertEqual(keybytes,output)


class TestEncryptionFunctions(unittest.TestCase):
    
    def test_encrypt_data_return(self):
        enc_key = b'\x1b\xe4$"\x87,!\x15X\xe8~\xef\x87\xd0!W\xc2\xa6I\xf2?+\xe3\x8c_\xff\xb2A\xe6gj\xb7'
        data = b'data to be encrypted'
        with captured_output() as (out,err):
            cipher, enc_output = encrypt_data(enc_key,data)
            self.assertIsInstance(enc_output,bytes)

    def test_writing_enc(self):
        file_path = 'tests/data_for_test/enc'
        enc_key = b'\x1b\xe4$"\x87,!\x15X\xe8~\xef\x87\xd0!W\xc2\xa6I\xf2?+\xe3\x8c_\xff\xb2A\xe6gj\xb7'
        data = b'data to be encrypted'

        with captured_output() as (out,err):
            cipher, enc_output = encrypt_data(enc_key,data)
            write_enc_data(cipher,file_path,'encryption','test',enc_output)
            self.assertTrue(isfile(join(file_path,'encryption.test')),'file not created')
    
    def test_reading_enc(self):
        file_path = 'tests/data_for_test/enc/encryption.test'
        enc_key = b'\x1b\xe4$"\x87,!\x15X\xe8~\xef\x87\xd0!W\xc2\xa6I\xf2?+\xe3\x8c_\xff\xb2A\xe6gj\xb7'
        expected_data = b'data to be encrypted'
        
        with captured_output() as (out,err):
            try:
                output = read_enc_data(enc_key,file_path)
            except FileNotFoundError:
                pass
            self.assertTrue(isfile(file_path),'file does not exist. Fix encryption writing function')
            self.assertIsInstance(output,bytes)
            self.assertEqual(expected_data,output)


class TestDataConversion(unittest.TestCase):

    def test_convert_bytes_to_str(self):
        data = 'testing these bytes'
        byte = bytes(data,'utf-8')

        with captured_output() as (out,err):
            output = convert_bytes_to_str(byte)
            self.assertIsInstance(output,str)
            self.assertEqual(data,output)

    def test_convert_str_to_bytes(self):
        data = "testing string"
        byte = b'testing string'

        with captured_output() as (out,err):
            output = convert_str_to_bytes(data)
            self.assertIsInstance(output,bytes)
            self.assertEqual(output,byte)

if __name__ == "__main__":
    unittest.main()
