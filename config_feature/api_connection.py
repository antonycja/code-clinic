import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# Read more about scopes here: https://developers.google.com/calendar/api/auth
# TODO: Change When we want to do more than just reading.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authenticate_user():
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


def get_data_from_calendar_api(service, calendar=1, max_results=7):

        # Calling the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print(f"Getting the upcoming {max_results} events")
        events_result = (
            service.events()
            .list(
                calendarId=f'{"c_965b5696a1903c71011a25a8eb71e97b3d847410f8ee919764cd46e585d1c528@group.calendar.google.com" if calendar == 2 else "primary"}',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next max_events events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            start = start.replace("T", " at ")
            start = start[:19]
            print(start, "->", event["summary"])



def get_calendar_results(calendar, max_results):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    user_credentials = authenticate_user()

    try:
        service = build("calendar", "v3", credentials=user_credentials)
        get_data_from_calendar_api(service, calendar, max_results)

    except HttpError as error:
        print(f"An error occurred: {error}")


# if __name__ == "__main__":
#     main()
