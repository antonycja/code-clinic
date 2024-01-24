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
from os.path import join as save_path
import os

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
