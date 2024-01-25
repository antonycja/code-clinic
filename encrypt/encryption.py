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
import pickle

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



# recon recovery 
def save_recon(path: str, recovery_data: dict):
    """
    Saves the recovery file. Recovery file only used in emergencies.
    Regenerates encryption token

    Args:
        path: path to save files to
        recovery_data (dict): its a secret
    """
    file_path = save_path(path,'recon')
    with open(f'{file_path}.json','wb') as file:
        pickle.dump(recovery_data,file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close
        
    return   

# reading
def read_recon(path: str):
    """
    Reads the recon file and returns a dictionary containing recovery data
    incase user lost encryption key

    Args:
        path (str): path_of_recon_file
    Returns:
        dict : contains recovery data
    """
    
    with open(f'{path}','rb') as file:
        recovery_data = pickle.load(file)
        file.close()
        
    return recovery_data
     