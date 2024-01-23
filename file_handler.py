"""
Configuration  Module 
"""

__author__ = 'Johnny Ilanga'
__version_ = '1.0'

import os
import re
import json

# The configuration file ticket requirements

#read and write config files
# hidden location in home
# secure storage of hidden files
# required is user information
# Option is between Json and yml
# Json data to DB if using data base
# yml to local machine with login information 


# dir operations
def get_home():
    """
    Retrieves the home directory of the machine
    """
    return os.environ.get('HOME')


def create_secure_dir():
    """
    Creates the secure dir to store important file
    
    Returns:
        str : the path of the folder that has been created
    """
    # getting the home variable (pc account user name)
    home = os.environ.get('HOME')
    dir_name = '.code_doctor'   # name of the folder
    secure_dir = os.path.join(home,dir_name)
    
    if os.path.exists(secure_dir):
        pass
    else:
        os.makedirs(secure_dir)
    
    return secure_dir


def get_secure_dir():
    """
    For emergencies use. Returns what the name of the secure folder is

    Returns:
        str: name of secure folder
    """
    return os.path.join(os.environ.get("HOME"),'.code_doctor')

# user_data operations    
def generating_logIn_cred():
    """
    Generates the user login credentials 
    Returns:
        tuple : username, useremail, password
    """
    
    # initialization phase
    mail_pattern = '@student.wethinkcode.co.za'
    pattern = re.compile(r"^[a-zA-Z\s]+[0-9]{3}"+f"{mail_pattern}$")
    data = dict()

    while True:
        username = input('Enter your username: ').lower().strip()
        if re.match('^[a-zA-z]+[0-9]{3}$',username):
            data["username"] = username
            break
        else:
            print('Incorrect username: (johndoe023).\n')
            

    while True:

        useremail = input('Enter your email: ').lower().strip()
        if re.match(pattern,useremail):
            data["email"] = useremail
            break
        else:
            print('Incorrect email.\n')
            
    
    while True:

        password = input('Enter passphrase: ')
        confirm_password = input('Enter same passphrase: ')
        
        if len(password) == 0 and len(confirm_password) == 0:
            data["password"] = None
            break
        
        if password == confirm_password:
            data["password"] = password
            break
        else:
            print('Passphrases do not match. Try again.\n')
    
    return data


# config file operations
def write_config(data: dict,path: str):
    """
    writes user config data into a file
    
    Args:
        data (dict): the data we want to write
        path (str): the path to write the data to
    """
    data_to_write = json.dumps(data,indent=2)
    
    with open(path,'w') as file:
        file.write(data_to_write)
        file.close()

    return


def read_config(path: str | dict):
    """
    Reads data from a json file. File path is passed as an arg
    The data is read from the file, then returned as a Dictionary or Lits

    Args:
        path (str): path of file

    Returns:
        dict | list: the return data is dependent on the data in the json
    """
    

    with open(path) as file:
        data = json.loads(file.read())
        file.close()
    
    return data

# helper functions   
def animation():
    column, lines = os.get_terminal_size()
    print('-' * column)