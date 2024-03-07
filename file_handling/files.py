"""
Just for file handling and creating folders
"""

import os

__author__ = 'Johnny Ilanga'

# dir operations
def get_home():
    """
    Retrieves the home directory of the machine
    """
    return os.environ.get('HOME')


def create_dir(dir_path: str, dir_name: str):
    """
    Creates the secure dir to store important file
    
    Returns:
        str : the path of the folder that has been created
    """

    # name of the folder
    dir = os.path.join(dir_path,dir_name)
    
    if os.path.exists(dir):
        pass
    else:
        os.makedirs(dir)
    
    return dir


# commit first
def check_user_profile(user_name: str):
    """
    Checks if the user has a profile on this pc

    Args:
        user_name (str): the username of the user

    Returns:
        bool : if the user has a profile
    """
    username = f'.{user_name}'
    data = os.listdir(os.path.join(get_home(),'.elite'))

    if username in data:
        return True

    return False