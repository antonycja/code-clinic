"""
The encryption module is in charge of creating, writing and reading the encrypted
data
"""


from Cryptodome.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from string import ascii_letters
from random import randint, choice
from os.path import join as save_path
import re

__author__ = 'Johnny Ilanga'
__all__ = [
    'generate_key',
    'generating_salt_and_pepper',
    'encrypt_data',
    'write_enc_data', 
    'read_enc_data',
    'save_key',
    'read_key',
    'return_data',
    'convert_bytes',
    'convert_str'
    ]


def generating_salt_and_pepper():
    """
    Generates the salt and pepper. The salt is a randomly generated sequence of bytes needed
    for the encryption process. Salt is Key
    
    Returns:
        byte: Returning the salt
        string: The pepper aka password
    """
    
    recovery_key = dict()
    
    salt = get_random_bytes(32)
    recovery_key["salt"] = salt
    
    # randomly generated password. length of password is randomly selected 
    password = "".join([choice(ascii_letters) for i in range(randint(8,17))])
    recovery_key["pepper"] = password
    
    return salt, password, recovery_key


def generate_key(salt: bytes, password: str):
    """
    Generates the encryption key based of the given salt and password
    
    Returns:
        bytes : generated key
    """  
    
    # decryption key length: 32
    return PBKDF2(password,salt,dkLen=32)


def encrypt_data(encryption_key: bytes, data):
    """
    Encrypting given data

    Args:
        encryption_key (bytes): the key for the encryption
        data (_type_): the data to decrypt
    Returns:
        object: cipher object, used for encryption
        bytes: encrypted data
    
    """
    
    # creating our cipher object, used to generate encryption entity
    cipher = AES.new(encryption_key,AES.MODE_CBC)    # encryption mode type CBC: BLOCK CIPHER 

    encrypted_data = cipher.encrypt(pad(data,AES.block_size))
    
    return cipher, encrypted_data


def write_enc_data(cipher: object, path: str ,file_name: str ,ext: str, data: bytes ):
    """
    Saves the encrypted data onto a bin

    Args:
        cipher (object): the encryption object
        path (str): the directory you want to save the file to
        file_name (str): the name of the file
        ext (str): the file extension
        data (bytes): the encrypted data
    """
    file_path = save_path(path,file_name)
    
    with open(f'{file_path}.{ext}','wb') as file:
        file.write(cipher.iv)   # iv: buffer for the cipher
        file.write(data)
        file.close
    
    return


def read_enc_data(key: bytes, path: str):
    """
    Decrypts and reads the data from the file

    Args:
        key (bytes): encryption key
        path(bytes | str): path of relative data source
    Returns:
        str: authentication details 
    """
    with open(path,'rb') as file:
        iv=file.read(16)    # reading first 16 bytes of file
        data = file.read()
        file.close()
    
    cipher = AES.new(key,AES.MODE_CBC,iv=iv)
    auth_data = unpad(cipher.decrypt(data),AES.block_size) # using standard block size
    
    return auth_data



# keys
def save_key(path: str,file_name: str, ext: str,key: bytes):
    """
    Saves the key for the login
    
    Args:
        path (str): location to save the key
        key (bytes): the key
    """
    path = save_path(path,file_name)
    
    with open(f'{path}.{ext}','wb') as file:
        file.write(key)
        file.close()


def read_key(path: str,file_name:  str):
    """
    reads the decryption key
    
    Args:
        path (str): location of the key
        key (bytes): the key
    """
    path = save_path(path,file_name)
    with open(f'{path}','rb') as file:
        key = file.read()
        file.close()

    return key


# helpers

def data_ablution(data: str):
    """
    Returns a dictionary of the users log in credentials

    Args:
        data (str): data source
    """
    credentials = dict()
    
    # cleaning up the str, so we can store in a dictionary
    pattern = re.compile("{|}|'|\s")

    filtered_data = re.sub(pattern,"",data)
    clean_up = filtered_data.split(',')

    for sequence in clean_up:
        meta = sequence.split(':')
        credentials[meta[0]] = meta[1]
        
    return credentials

def convert_bytes_to_str(data: bytes):
    """
    Converts a given byte sequence to strings

    Args:
        data (bytes): byte sequence
    Returns:
        str : converted bytes
    """
    
    return str(data,"utf-8")


def convert_str_to_bytes(data:  str):
    """
    Converts a given string sequence to byte

    Args:
        data (str): str sequence
    Returns:
        byte : converted str
    """
    
    return bytes(str(data),"utf-8")
