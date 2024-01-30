
import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLINIC_CALENDAR_ID = "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"
YEAR = 2024
USER_EMAIL = 'btshulisi023@student.wethinkcode.co.za'
def book_slot(creds, date_time):
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        #display_events(service, CLINIC_CALENDAR_ID)

        #create_event(service)

        update_event(service, date_time)

        os.remove('token.json')
    except HttpError as error:
        print("An error occured:", error) 


def update_event(service, start_date_time):
    now = dt.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(calendarId=CLINIC_CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])
    for event in events:
        if event['start']['dateTime'] == start_date_time:
            event['attendees'].append({'email': USER_EMAIL})
            event_id = event['id']
            updated_event = service.events().update(calendarId= CLINIC_CALENDAR_ID, eventId=event_id, body=event).execute()
            return True
            


def display_events(service, calendar_id):

        now = dt.datetime.utcnow().isoformat() + "Z"

        event_result = service.events().list(calendarId=CLINIC_CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = event_result.get('items', [])

        if not events:
            print("No upcoming events found!")
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


def create_event(service):
    event = {
        "summary" : "Code Clinic Meeting",
        'location': "cpt",
        'description': 'Some more details on this awesome event.',
        'colorId' : 6,
        'start': {
            'dateTime': '2024-01-29T17:00:00+02:00',
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': '2024-01-29T17:30:00+02:00',
            'timeZone': 'Africa/Johannesburg'
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': 'bulelatshulisi@gmail.com'}
        ],
    }

    event = service.events().insert(calendarId=CLINIC_CALENDAR_ID, body=event).execute()

    print(f'event created: {event.get("htmlLink")}')


def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')


    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        
    return creds


if __name__== '__main__':
    creds = authenticate()
    date_time = '2024-01-29T17:00:00+02:00'
    book_slot(creds, date_time)


