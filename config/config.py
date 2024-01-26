"""
configuration module
"""

import re

# user_data operations    
def generate_logIn_cred():
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
