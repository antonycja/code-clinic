"""
The particular module is designed only for login functions
"""

__author__ = 'Johnny Ilanga'


from getpass import getpass
import time
from helpers import writer
from os.path import exists

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

    # replacing none with empty string incase there is no password set by user
    if data["password"] == 'None' or data["password"] == None:
        data["password"] = ""

    if password == data["password"]:
        current_time = sys_time()
        exp = token_exp(current_time)
        print(f'Login successful. Token expires in 0 days 3 hours 59 minutes at {exp}')
        return True,[current_time,exp]

    print(f'login failed for {data["email"]} because Server returned error response')
    return False, ["",""]



def code_clinic_login(data: dict):
    """
    The main log in function for code clinic

    Args:
        data (dict): a dict containing important user related data
    """
    access, exp = login(data)
    dump_token(data["email"],access,exp)


    return access

# Token
def token_exp(login_time: str):
    """
    Returns the token expiration time
    If token expires the user must re-login in order ot use the application

    Args:
        login_time (str): The current time that the user is login
    """

    # splitting the string in parts, and retrieving just the time
    date = login_time.split(" ")[0]
    time = login_time.split(" ")[1]
    # retrieving current hour
    hour = time.split(":")[0]

    # calculating expiration hour
    exp_hour = int(hour) + 4

    if exp_hour > 23:
        exp_hour =  f'{0}{exp_hour - 24}'
    else:
        if exp_hour < 10:
            exp_hour = f'0{exp_hour}'
        else:
            exp_hour = f'{exp_hour}'

    # replacing the current hour with expiration hour
    exp_time = time.replace(hour,str(exp_hour))

    # between midnight till 3, if we created token a few hours before midnight
    if exp_hour in ['01','02','03']:
        new_date = fix_date(date)
        # exp date set to tomorrow
        return login_time.replace(time,exp_time).replace(date,new_date)
    else:
        logout_time = login_time.replace(time,exp_time)

    return logout_time


def dump_token(user_name: str, access: bool, expiration_data: str):
    """
    Creates a snapshot of the access token and dumps it in a file.
    The token snapshot saves user time from by eliminating the login process
    if the token has not expired.

    Args:
        user_name (str): the username of the user the token belongs too
        access (bool): access to application
        expiration_data (str): expiration date and time of the token
    """

    logIn_token = {
        f"{user_name}": {
            "access": access,
            "start": expiration_data[0],
            "expiration": expiration_data[1],
        }
    }
    writer.save_to_json("/tmp", ".logIn_token", logIn_token)


# commit first: added token clearing before exiting if token data is not valid
def check_token(path:str, data: dict ):
    """
    Checks whether the given token is valid. If the token is valid, we will skip
    the login menu. If token is not valid, the program gets terminated.

    Args:
        path (str): The dir of the token
        data (dict): valuable user data

    Returns:
        bool: True/False if their is a valid token
    """


    err_message = f"""Token not present: for user '{data["email"]}' : No matching entry found in secure storage.

Please login using

  code-clinic login
    """

    exp_message = f"""Token expired: for user '{data["email"]}'.

Please login using

  code-clinic login
    """

    # if access == False:
    if exists("/tmp/.logIn_token.json"):
        # reading the username to see if it has a token
        token = writer.read_from_json(path)[f'{data["email"]}']

        if not token["access"]:
            dump_token(data["email"],False,["",""])
            exit(err_message)  # get error from wtc_lms


        if not IsValidToken(token):
            dump_token(data["email"],False,["",""])
            exit(exp_message) # get from lms
    else:
        dump_token(data["email"],False,["",""])
        exit(err_message)



    return True

# Time related concepts

def sys_time():
    """
    Returns the current system time in a human readable format

    Returns:
        str: _The current time
    """

    curr_time = time.strftime(f"%Y-%m-%d %H:%M:%S %z")

    return curr_time

def timeshift(time: str):
    """
    returns the date, hour and minutes of a given timestamp

    Args:
        time (str): timestamp of the time we want formate

    Returns:
        dict : formatted timestamp data
    """

    data = dict()

    time_data = time.split(" ")[1]

    data["date"]= time.split(" ")[0]
    data["hours"] = time_data.split(":")[0]
    data["mins"] = time_data.split(":")[1]

    return data

def fix_date(date: str):
    """
    Fixes the token expiration date, ensuring a smooth login process

    Args:
        date (str): The token expiration date

    Returns:
        _str_: the newly formatted date
    """

    # retrieving month and day
    month = date.split("-")[1]
    day = date.split("-")[2]

    months_30days = ["04","06","09","11"]
    months_31days=["01","03","05","07","08","10","12"]

    # the new date of the new day
    new_day = int(day) + 1

    if month in months_30days and new_day > 30:
        new_month = int(month) + 1
        if new_month < 10:
            new_month = f'{0}{new_month}'
        elif new_month > 12:
            new_month = f'{0}{1}'
        else:
            new_month = str(new_month)
        new_day = f'{0}{1}'

    elif month in months_31days and new_day > 31:
        new_month = int(month) + 1
        if new_month < 10:
            new_month = f'{0}{new_month}'
        elif new_month > 12:
            new_month = f'{0}{1}'
        else:
            new_month = str(new_month)
        new_day = f'{0}{1}'

    elif month == "02" and new_day > 28:
        new_month = f'{0}{3}'
        new_day = f'{0}{1}'

    else:
        # date remains the same
        new_month = month

        if new_day < 10:
            new_day = f'{0}{new_day}'
        else:
            new_day = f'{new_day}'

    # the new/old date formatted.s
    new_date = date.replace(date.split("-")[1],new_month)
    new_date = new_date.replace(new_date.split("-")[2],new_day)

    return new_date


def IsValidToken(token_data: dict, current_date: str = timeshift(sys_time())):
    """
    Validates the token. Checks whether your current login time lies within the 4 hour window
    from when the token was created

    Args:
        token_data (dict): token data. Dict contains access status, created timestamp and expiration timestamp
        current_date (str, optional): Current system timestamp. Defaults to timeshift(sys_time()).

    Returns:
        bool : Validates the token and returns True or False
    """

    token_start = timeshift(token_data["start"])
    token_expiration = timeshift(token_data["expiration"])

    # checking if the date is the same
    if not current_date["date"] == token_start["date"]:
        return False

    # start hour less(<) than current hour and exp less (<) than current hour
    if int(token_start["hours"]) < int(current_date["hours"]) and int(
        token_expiration["hours"]
    ) < int(current_date["hours"]):
        return False

    # if the current hour is the same as the exp hour, we validate based of minutes
    if token_expiration["hours"] == current_date["hours"] and int(
        token_expiration["mins"]
    ) <= int(current_date["mins"]):
        return False

    return True

