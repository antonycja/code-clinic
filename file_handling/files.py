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
    
    return


