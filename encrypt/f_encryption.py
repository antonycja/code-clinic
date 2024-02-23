"""
This module deals with authentication encryption and decryption
"""
__author__ = 'Johnny Ilanga'

from cryptography.fernet import Fernet
from os.path import join as save_path
import json
import pickle

# key
def f_keygen():
    """
    Generates the encryption key
    
    Returns:
        bytes: encryption key
    """
    return Fernet.generate_key()
    

# encryption process
def f_encrypt(path: str, data_ref, key: bytes):
    """
    The encryption process. Encrypts the given data

    Args:
        path (str): path to save encrypted data 
        data_ref (_type_): data source
        key (bytes): encryption key
    """
    file_path = save_path(path,'auth')
    enc = Fernet(key)
    data = enc.encrypt(data_ref)
    
    # saving encrypted data
    with open(f'{file_path}.json','wb') as file:
        file.write(data)


# decryption process
def f_decrypt(path: str, key: bytes):
    """
    Decrypts the given data

    Args:
        path (str): the data to decrypt
        key (bytes): key to use
    Returns:
        any : decrypted data
    """
    enc = Fernet(key)
    
    with open(path,'rb') as file:
        decrypt_data = file.read()
    
    data = enc.decrypt(decrypt_data)
    
    return data 
    

# key operations 
def write_key(path: str, key: bytes):
    """
    saves the key to a file

    Args:
        path (str): path to save file
        key (bytes): encryption key 
    """
    
    path = save_path(path,'master')
    
    with open(f'{path}.bin','wb') as file:
        file.write(key)
        file.close()      


def read_key(path:str , key: bytes):
    """
    reads the key fernet key
    """       
    with open(path,'rb') as file:
        key = file.read()
        
    return key


def capture_data(path: str,file_name: str, data  : dict):
    """
    Saves the recovery file. Recovery file only used in emergencies.
    Regenerates encryption token

    Args:
        path: path to save files to
        recovery_data (dict): its a secret
    """
    file_path = save_path(path,file_name)
    with open(f'{file_path}.json','w') as file:
        pickle.dump(data,file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close
        
    return   

# reading
def read_recon(path: str, file_name):
    """
    Reads the recon file and returns a dictionary containing recovery data
    incase user lost encryption key

    Args:
        path (str): path_of_recon_file
    Returns:
        dict : contains recovery data
    """
    file_path = save_path(path,file_name)
    with open(f'{file_path}.bin','rb') as file:
        recovery_data = pickle.load(file)
        file.close()
        
    return recovery_data
     

def convert_data(data: object | dict | list):
    """
    Formats the data to json format so that it can be saved on a .json file

    Args:
        data (object | dict | list): data / data source to convert
    """
    
    json_strings = json.dumps(data, indent=2) # specifying indent depth
    return json_strings

def write_json(path: str, file_name:str ,data: str):
    """
    Saves the formatted data into a .json file

    Args:
        path (str): path to save the file
        file_name (str): the name of the file
        data (str): data / data source to convert
    """
    
    file_path = save_path(path,file_name)
    
    with open(f'{file_path}.json','w') as file:
        file.write(data)
        file.close()
        
    return

def save_to_json(path: str, file_name: str,data_ref: object | dict | list):
    """
    Converts and writes the data to .json file
    
    Args:
        path (str): path to save the file
        file_name (str): the name of the file
        data (object | dict | list): data / data source 
    """
    data = convert_data(data_ref)
    write_json(path,file_name,data)
    
    return



