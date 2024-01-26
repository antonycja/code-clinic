"""
This module is used solely for writing and reading functions
This is nothing more than a helper module
"""

import json
import pickle
from os.path import join as save_path

__all__ = [
    'convert_data',
    'write_to_json',
    'save_to_json',
    'read_from_json',
    'capture_pickle',
    'load_pickle'
]

# json file handling
def convert_data(data: object | dict | list):
    """
    Formats the data to json format so that it can be saved on a .json file

    Args:
        data (object | dict | list): data / data source to convert
    """
    
    json_strings = json.dumps(data, indent=2) # specifying indent depth
    return json_strings

def write_to_json(path: str, file_name:str ,data: str):
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
    write_to_json(path,file_name,data)
    
    return


def read_from_json(json_file: str):
    """
    The path of the json file

    Args:
        json_file (object): _description_
    """
    

    with open(json_file,'r') as file:
        data = json.loads(file.read())
        file.close()
    

    return data
   
   
# pickle 
def capture_pickle(path: str,file_name: str, ext: str ,data  : dict):
    """
    Saves the recovery file. Recovery file only used in emergencies.
    Regenerates encryption token

    Args:
        path: path to save files to
        recovery_data (dict): its a secret
    """
    file_path = save_path(path,file_name)
    with open(f'{file_path}.{ext}','wb') as file:
        pickle.dump(data,file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()
        
    return
def capture_pickle(path: str,file_name: str, ext: str ,data):
    """
    Saves the recovery file. Recovery file only used in emergencies.
    Regenerates encryption token

    Args:
        path: path to save files to
        recovery_data (dict): its a secret
    """
    file_path = save_path(path,file_name)
    with open(f'{file_path}.{ext}','wb') as file:
        pickle.dump(data,file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()
        
    return


def load_pickle(path: str,file_name: str):
    """
    Reads the recon file and returns a dictionary containing recovery data
    incase user lost encryption key

    Args:
        path (str): path_of_recon_file
    Returns:
        dict : contains recovery data
    """
    path_name = save_path(path,file_name)
    with open(f'{path_name}','rb') as file:
        data = pickle.load(file)
        file.close()
        
    return data