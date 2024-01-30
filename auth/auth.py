import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_user():
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    user_credentials = None  # Default the user credentials to nothing
    token = "token.json"
    cred_file_name = "credentials.json"

    """The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time."""
    # check if the token.json file exists
    if os.path.exists(token):
        # update the user credentials  to the token info if it exists
        user_credentials = Credentials.from_authorized_user_file(token, SCOPES)

    # Check if the user credentials don't exists or are not valid then let them sign in
    if not user_credentials or not user_credentials.valid:
        # check if the token has not expired
        if user_credentials and user_credentials.expired and user_credentials.refresh_token:
            # Refresh the credentials if they already exist but expired
            user_credentials.refresh(Request())
        else:
            # Run the authentication process
            authentication_process = InstalledAppFlow.from_client_secrets_file(
                cred_file_name, SCOPES)
            user_credentials = authentication_process.run_local_server(port=0)

        # Save the credentials for next execution
        with open(token, "w") as tkn:
            tkn.write(user_credentials.to_json())

    return user_credentials