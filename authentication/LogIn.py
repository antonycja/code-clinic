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


def token_exp(login_time: str):
    """
    Returns the token expiration time
    If token expires the user must re-login in order ot use the application

    Args:
        login_time (str): The current time that the user is login
    """
    

    # splitting the string in parts, and retrieving just the time 
    time = login_time.split(" ")[1]
    # retrieving current hour
    hour = time.split(":")[0]
    
    # calculating expiration hour
    exp_hour = int(hour) + 4
    if exp_hour == 24:
        exp_hour = 00
    elif exp_hour > 24:
        pass
      
    # replacing the current hour with expiration hour   
    exp_time = time.replace(hour,str(exp_hour))
    
    logout_time = login_time.replace(time,exp_time)

    return logout_time
     

def sys_time():
    """
    Returns the current system time in a human readable format

    Returns:
        str: _The current time
    """

    curr_time = time.strftime(f"%Y-%m-%d %H:%M:%S %z")

    return curr_time
