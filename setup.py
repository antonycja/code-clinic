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
    if not exists(save_path(user_dir,'.elite')):
        main_dir = files.create_dir(user_dir,'.elite') # main folder
    else:
        main_dir = save_path(user_dir,'.elite')
        
    if not exists(save_path(main_dir,'.access')):
        auth_dir = files.create_dir(main_dir,'.access') # user login details, authentication key and token
    else:
        auth_dir = save_path(main_dir,'.access')
        
    if not exists(save_path(main_dir,'.recon')):
        recon_dir = files.create_dir(main_dir,'.recon') # key recovery data
    else:
        recon_dir = save_path(main_dir,'.recon')
        
    if not exists(save_path(main_dir,'.elite')):
        key_dir = files.create_dir(main_dir,'.elite')   # key
    else:
        key_dir = save_path(main_dir,'.elite')
        
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
    encryption.save_key(dirs['key'],f'.{key_name}',f'{key_ext}',key)
    writer.capture_pickle(dirs['recon'],f'.{recon_name}',f'{recon_ext}',recon)    
    data_to_enc = encryption.convert_str_to_bytes(data)
    cipher, enc_data = encryption.encrypt_data(key,data_to_enc)
    encryption.write_enc_data(cipher,dirs["auth"],f'.{file_name}',f'{file_ext}',enc_data)

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
    info = encryption.data_ablution(clean_up)

    return info

def setup():
    folders = secure_folder()
    cs = authentication.get_credentials()
    user_data = config.generate_logIn_cred()
    encrypt_it(user_data,folders,'keys','elite','SOS','recon','config','elite')
    encrypt_it(cs,folders,'keys','cred','creds','recon','credentials','elite')
    
    return user_data, folders
    

def pre_load():
    """
    Main function
    """
    if exists(save_path(files.get_home(),'.elite')):

        folders = secure_folder()
        success,message = True, None

        # checking if all necessary files are in place
        auth_dir = ['.config.creds','.cs.elite']
        for file in auth_dir:
            if not exists(save_path(folders['auth'],file)):
                success = False
                break

        key_dir = ['.keys.creds','.keys.elite']
        for file in key_dir:
            if not exists(save_path(folders['key'],file)):
                success = False
                break

        recon_dir = ['.creds.recon','.SOS.recon']
        for file in recon_dir:
            if not exists(save_path(folders['recon'],file)):
                success = False
                break

        if success == False:
            message = 'One of more important file is missing.'
            # exit('Run: code-clinic configure')



        return success,message
    else:
        print('Welcome to Code_Clinic\nYou do not appear to have a config file defined, so let me ask you some questions.')
        setup()
        exit('\nSetup complete.\nRun: code_clinic')




def generate_creds(folders):
    """
    Generates the credentials object (creds)
    The creds is an object with methods that can be used alongside the google functions
    for operations with the google api

    Args:
        folders (dict): a dictionary containing all the important folders

    Returns:
        object: returns the credentials object that is used along with google functions
    """

    cs = decrypt_it(folders,'keys','cred','credentials','elite')
    
    #creating a tmp file with the decrypted data
    writer.write_to_json('/tmp','.creds',cs)
    

    if exists(save_path(folders['auth'],'.token.elite')):
        token = decrypt_it(folders,'keys','tk','token','elite')
        writer.write_to_json('/tmp','.token',token)
        
    creds = authentication.authenticate('/tmp/.creds.json','/tmp/.token.json')
    
    if not exists(save_path(folders['auth'],'.token.elite')):
        # saving an encrypted version of the token
        with open('/tmp/token.json','r') as file:
            data = file.read()
        encrypt_it(data,folders,'keys','tk','token','recon','token','elite')


    return creds

if __name__ == '__main__':
    # ADDING PRELOAD
    s,f = pre_load()
    generate_creds(f)