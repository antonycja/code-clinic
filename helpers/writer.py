"""
This module is used solely for writing and reading functions
This is nothing more than a helper module
"""

import json
import pickle
from os.path import join as save_path

# json file handling
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


def read_json(json_file: str):
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
def capture_pickle(path: str,file_name: str, data  : dict):
    """
    Saves the recovery file. Recovery file only used in emergencies.
    Regenerates encryption token

    Args:
        path: path to save files to
        recovery_data (dict): its a secret
    """
    file_path = save_path(path,file_name)
    with open(f'{file_path}.bin','wb') as file:
        pickle.dump(data,file, protocol=pickle.HIGHEST_PROTOCOL)
        file.close()
        
    return   