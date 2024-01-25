"""
The encryption module is in charge of creating, writing and reading the encrypted
data
"""

__author__ = 'Johnny Ilanga'

from Cryptodome.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from string import ascii_letters
from random import randint, choice
import pickle
from os.path import join as save_path

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


def encrypting_data(encryption_key: bytes, data):
    """
    Encrypting given data

    Args:
        encryption_key (bytes): the key for the encryption
        data (_type_): the data to decrypt
    
    """
    
    # creating our cipher object, used to generate encryption entity
    cipher = AES.new(encryption_key,AES.MODE_CBC)    # encryption mode type CBC: BLOCK CIPHER 

    encrypted_data = cipher.encrypt(pad(data,AES.block_size))
    
    return cipher, encrypted_data


def write_enc_data(cipher: object, path: str ,file_name: str , data: bytes ):
    """
    Saves the encrypted data onto a bin

    Args:
        cipher (object): the encryption object
        path (str): the directory you want to save the file to
        file_name (str): the name of the file
        data (bytes): the encrypted data
    """
    file_path = save_path(path,file_name)
    
    with open(f'{file_path}.bin','wb') as file:
        file.write(cipher.iv)   # iv: buffer for the cipher
        file.write(data)
        file.close
    
    return
