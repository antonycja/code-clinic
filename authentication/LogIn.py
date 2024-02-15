"""
The particular module is designed only for login functions
"""

__author__ = 'Johnny Ilanga'


from getpass import getpass
import time

def login(data: dict):
    """
    authenticates the user and ensures that the correct user is logging in
    
    Args:
        folders (dict): folder containing important files such as user config
        data (dict): the config data

    Returns:
        bool : True / False login status
    """

    password = getpass(f'Logging in as {data["email"]} to Code-Clinic\npassword: ')
    if password == data["password"]:
        print('Login successful. Token expires in 0 days 3 hours 59 minutes at 2024-02-15 19:48:06 +02:00')
        return True

    print(f'login failed for {data["email"]} because Server returned error response')
    return False

def sys_time():
    """
    Returns the current system time in a human readable format

    Returns:
        str: _The current time
    """

    curr_time = time.strftime(f"%Y-%m-%d %H:%M:%S %z")

    return curr_time
