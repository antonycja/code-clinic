"""
code clinic setup 
"""

from config import config
from encrypt import encryption
from file_handling import files
from helpers import writer, animation

__author__ = 'Johnny Ilanga'
__version_ = '1.0'


def secure_folder():
    """
    creates the dir tree structure
    
    Returns:
        dict : dir paths
    """
    
    user_dir = files.get_home()
    main_dir = files.create_dir(user_dir,'.elite') # main folder
    auth_dir = files.create_dir(main_dir,'.access')  # user login details, authentication key and token
    recon_dir = files.create_dir(main_dir,'.recon') # key recovery data
    key_dir = files.create_dir(main_dir,'.elite')   # key
    
    return {"main":main_dir, "auth":auth_dir, "recon": recon_dir, "key":key_dir}
