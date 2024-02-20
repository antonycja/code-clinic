"""
configuration module
"""

import re
from getpass import getpass

__all__ = [
    'generate_logIn_cred'
]


# user_data operations
def generate_logIn_cred(username: str = None, useremail: str = None, password:str = None ):
    """
    Generates the user login credentials
    Returns:
        tuple : username, useremail, password
    """

    # initialization phase
    mail_pattern = '@student.wethinkcode.co.za'
    pattern = re.compile(r"^[a-zA-Z\s]+[0-9]{3}"+f"{mail_pattern}$")
    data = dict()


    if username == None or not re.match(r'^[a-zA-z]+[0-9]{3}$',username):
        while True:
            if username != None and not re.match('^[a-zA-z]+[0-9]{3}$',username):
                print('Incorrect username format: (johndoe023).')

            username = input('Please provide your username: ').lower().strip()

            if re.match('^[a-zA-z]+[0-9]{3}$',username):
                data["username"] = username
                break
    else:
        data["username"] = username

    if useremail == None or not re.match(pattern,useremail):
        while True:

            if useremail != None and not re.match(pattern,useremail) :
                print('Incorrect email format: (johndoe023@student.wethinkcode.co.za).')

            useremail = input('Please provide your email: ').lower().strip()
            if re.match(pattern,useremail):
                data["email"] = useremail
                break
    else:
        data["email"] = useremail

    if password == None:
        while True:

            password = getpass('Please provide a passphrase: ')
            confirm_password = getpass('Enter same passphrase: ')

            if len(password) == 0 and len(confirm_password) == 0:
                data["password"] = None
                break

            if password == confirm_password:
                data["password"] = password
                break
            else:
                print('Passphrases do not match. Try again.\n')

    return data