"""
This module is used solely for writing and reading functions
This is nothing more than a helper module
"""

import json
from os.path import join as join_path
import os
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
    
    file_path = join_path(path,file_name)
    
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


