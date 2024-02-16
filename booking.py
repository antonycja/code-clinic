
import os.path, sys
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


def book_slot(creds, booking_info : dict):
    try:
        service = build('calendar', 'v3', credentials=creds)

        return update_event(service, booking_info)


    except HttpError as error:
        print("An error occured:", error) 


def update_event(service, booking_info : dict) -> bool:
    now = dt.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(calendarId=CLINIC_CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])

    for event in events:
        if event['start']['dateTime'] == booking_info['dateTime']:
            number_of_attendees = len(event['attendees'])
            if number_of_attendees == 2:
                print("Slot is already booked. TRY ANOTHER.")
                return False
            
            event['attendees'].append({'email': USER_EMAIL})
            event["summary"] = "Code Clinic Meeting"
            event['description'] = booking_info['description']

            event_id = event['id']

            updated_event = service.events().update(calendarId= CLINIC_CALENDAR_ID, eventId=event_id, body=event).execute()

            message = "Booking Successful!"

            return True, message
    

    message = "There is no volunteer for the slot you selected. TRY ANOTHER."
    return False, message


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
        "summary" : "VOLUNTEER SLOT",
        'location': "CPT",
        'description': 'You can book this slot if  you want to volunteer.',
        'colorId' : 6,
        'start': {
            'dateTime': '2024-02-16T16:00:00+02:00',
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': '2024-02-16T16:30:00+02:00',
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


def cancel_booking(creds, booking_info):
    try:

        service = build('calendar', 'v3', credentials=creds)

        return remove_attendee(service, booking_info)


    except HttpError as err:
        message = f"An error occured: {err}"
        print(message)


def remove_attendee(service, booking_info : dict):
    date_time = booking_info['dateTime']

    now = dt.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(calendarId=CLINIC_CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get("items", [])

    for event in events:
        if event['start']['dateTime'] == booking_info['dateTime'] and booked_event(event):
            event['attendees'].pop()
            event['summary'] = "VOLUNTEER SLOT"
            event['description'] = "You can book this slot if  you want to volunteer."

            event_id = event['id']

            updated_event = service.events().update(calendarId=CLINIC_CALENDAR_ID, eventId=event_id, body=event).execute()

            message = "Booking Cancelled."
            return True, message

    message = "No booking to cancel."
    return False, message


def booked_event(event) -> bool:
    for attendee in event['attendees']:
        if attendee['email'] == USER_EMAIL:
            return True
    
    return False
def get_date_time(user_input):
    day = user_input.split("T")[0]
    time = user_input.split("T")[1]

    return f"2024-02-{day}T{time}:00+02:00"



if __name__== '__main__':
    creds = authenticate()

    date_time = '2024-02-13T17:00:00+02:00'
    description = 'I need help with 2D arrays'

    booking_info = dict()

    



    arguments = sys.argv

    if arguments[1] == 'book':
        start_date_time = get_date_time(arguments[2])
        print(start_date_time)
        description = arguments[3]

        booking_info['dateTime'] = start_date_time
        booking_info['description'] = description

        message = book_slot(creds, booking_info)
        print(message)
    elif arguments[1] == 'cancel_booking':

        start_date_time = get_date_time(arguments[2])
        booking_info['dateTime'] = start_date_time
        message = cancel_booking(creds, booking_info)

        print(message)
    os.remove('token.json')

