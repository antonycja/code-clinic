"""
This module is designed to authenticate the user and ensure that connection to 
the google api is a success
"""

# The google calender has data containing

# credentials
# Credentials are used to obtain an access token from Google's authorization
# servers so your app can call Google Workspace APIs. This guide describes 
# how to choose and set up the credentials your app needs.

# Client ID and client secrets are created when you create your oauth2 url
# These are not needed for web apps like the one we are about to build 

import os.path

import googleapiclient._auth as auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors as ERR

# permissions being granted to user. Consider it as rules of usage 
SCOPES =  ['https://www.googleapis.com/auth/calendar']  # (Full Access)


def authenticate(cred_path: str, token_path: str):
    
    creds = None
    
    if os.path.exists(token_path):
        
        # if a token exist we create a credentials object with user credentials, 
        # and assigning them permissions based off the scope         
        creds = Credentials.from_authorized_user_file(token_path,SCOPES)

    # Invalid credentials 
    if not creds or not creds.valid:
        
        # if access token is expired, we refresh it 
        if creds and creds.expired and creds.refresh_token:
            
            creds.refresh(Request())
        else:
            # failure to refresh token, leads creation of a new token
            
            # creating flow object used for token generation with permissions specified in scopes
            flow = InstalledAppFlow.from_client_secrets_file(cred_path,SCOPES)
            
            # generating credentials and token
            creds = flow.run_local_server(port=0)
            
        # saving generated token:
        
        dir_path = os.path.dirname(token_path)
        with open(os.path.join(dir_path,'token.json'),'w') as file:
            file.write(creds.to_json())
            file.close()
    
       
    return creds
        

