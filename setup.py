"""
code clinic setup module
"""

from config import config
from encrypt import encryption
from file_handling import files
from helpers import writer, animation
from authentication import authentication
from os.path import join as save_path
from os.path import exists

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


def encrypt_it(data: dict, dirs: dict, key_name: str, key_ext: str, recon_name: str, recon_ext: str, file_name: str, file_ext: str):
    """
        Main Encryption method. Encrypts the user data and saves it onto your local machine

    Args:
        user_info (dict): User configuration details
        dirs (dict): dict containing dir paths to store files
        key_name (str): The name of the key file
        key_ext (str): the extension of the key file
        recon_name (str): the name of the recon file 
        recon_ext (str): the extension of the recon file
        file_name (str): the name of the file
        file_ext (str): the extension of the file
    """
    
    salt, pepper, recon = encryption.generating_salt_and_pepper()
    
    key = encryption.generate_key(salt,pepper)
    encryption.save_key(dirs['key'],f'.{key_name}',f'.{key_ext}',key)
    writer.capture_pickle(dirs['recon'],f'.{recon_name}',f'.{recon_ext}',recon)    
    data_to_enc = encryption.convert_str_to_bytes(data)
    cipher, enc_data = encryption.encrypt_data(key,data_to_enc)
    encryption.write_enc_data(cipher,dirs["auth"],f'.{file_name}',f'.{file_ext}',enc_data)

    return



def decrypt_it(dirs: dict,key_name: str, key_ext: str, file_name: str ,file_ext: str):
    """
        Main Decrypting Method. Decrypts all the encrypted data

    Args:
        dirs (dict): dict containing dir paths of encrypted files
        key_name (str): the name of the file containing the key 
        key_ext (str): the extension of the file (e.g .txt)
        file_name (str): the name of then file we want to decrypt
        file_ext (str): the extension of the file we want to decrypt
        
    Returns:
        dict : dictionary containing the data requested
    """


    key = encryption.read_key(dirs["key"],f'.{key_name}.{key_ext}')
    data = encryption.read_enc_data(key,save_path(dirs["auth"],f'.{file_name}.{file_ext}'))
    clean_up = encryption.convert_bytes_to_str(data)
    user_info = encryption.data_ablution(clean_up)

    return user_info

def setup():
    folders = secure_folder()
    user_data = config.generate_logIn_cred()
    encrypt_it(user_data,folders)
    
    return user_data, folders
    

def main():
    """
    Main function
    """
    if exists(save_path(files.get_home(),'.elite')):
        print('no code')
    else:
       setup()
       authentication.authenticate()
       
    
    

if __name__ == '__main__':
    main()