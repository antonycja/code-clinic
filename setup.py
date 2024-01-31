"""
code clinic setup module
"""

from config import config
from encrypt import encryption
from file_handling import files
from helpers import writer, animation
from authentication import authentication
from os.path import join as save_path

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


def encrypt_it(user_info: dict, dirs: dict):
    """
    Main Encryption method. Encrypts the user data and saves it onto your local machine

    Args:
        user_info (dict): User configuration details
        dirs (dict): dict containing dir paths to store files
    """   
    
    salt, pepper, recon = encryption.generating_salt_and_pepper()
    
    key = encryption.generate_key(salt,pepper)
    encryption.save_key(dirs['key'],'.key','elite',key)
    writer.capture_pickle(dirs['recon'],'SOS','.recon',recon)    
    data = encryption.convert_str_to_bytes(user_info)
    cipher, enc_data = encryption.encrypt_data(key,data)
    encryption.write_enc_data(cipher,dirs["auth"],'.config','elite',enc_data)

    return



def decrypt_it(dirs: dict):
    """
    Main Decrypting Method. Decrypts all the encrypted data

    Args:
        dirs (dict): dict containing dir paths of encrypted files

    Returns:
        dict : user_info (name, mail, pass)
    """

    key = encryption.read_key(dirs["key"],'.key.elite')
    data = encryption.read_enc_data(key,save_path(dirs["auth"],'.config.elite'))
    clean_up = encryption.convert_bytes_to_str(data)
    user_info = encryption.data_ablution(clean_up)

    return user_info
