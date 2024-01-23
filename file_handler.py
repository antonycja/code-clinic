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

def animation():
    column, lines = os.get_terminal_size()
    print('-' * column)
    
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
def write_config(data: dict):
    """
    writes user config data into a file
    """
    data_to_write = json.dumps(data,indent=2)
    
    with open('login_credentials.json','w') as f:
        f.write(data_to_write)
        f.close()
    
    print(f'line 84: config data saved')
    return
    