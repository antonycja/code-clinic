"""
This module is designed for booking functions
"""

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


def book_slot(creds, booking_info : dict, USER_EMAIL) -> tuple:
    """
    Books a slot specified by the user.

    Parameters:
        creds (Credentials): A Credentials object necessary to build a calendar.
        booking_info (dict): Contains information about the booking {'dateTime': date, 'description': description}
        USER_EMAIL (str): The current user's email.
    
    Returns:
        (success, message) (tuple): (var)success is whether the booking was a success or not(boolean). (vara)message is the appropriate message to display.

    """
    try:
        service = build('calendar', 'v3', credentials=creds)
        success, message = update_event(service, booking_info, USER_EMAIL)

        return success, message


    except HttpError as error:
        print("An error occured:", error) 


def update_event(service, booking_info : dict, USER_EMAIL) -> tuple:
    """
    Updates an existing event in order to book a slot.

    Parameters:
        service (Resource): A Resource object with methods for interacting with the service.
        booking_info (dict): {'dateTime': the date and time for the slot, 'description': the reason for booking the slot}
        USER_EMAIL (str): The current user's email.
    
    Returns:
        (success, message) (tuple): (var)success is whether the booking was a success or not(boolean). (vara)message is the appropriate message to display.
    """
    now = dt.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(calendarId=CLINIC_CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get('items', [])

    for event in events:
        if event['start']['dateTime'] == booking_info['dateTime']:
            number_of_attendees = len(event['attendees'])
            if number_of_attendees == 2:
                message = "Slot is already booked. TRY ANOTHER."
                return False, message
                
            
            event['attendees'].append({'email': USER_EMAIL})
            event["summary"] = "Code Clinic Meeting"
            event['description'] = booking_info['description']

            event_id = event['id']

            updated_event = service.events().update(calendarId= CLINIC_CALENDAR_ID, eventId=event_id, body=event).execute()

            message = "Booking Successful!"

            return True, message
    

    message = "There is no volunteer for the slot you selected. TRY ANOTHER."
    return False, message


def create_event(service):
    event = {
        "summary" : "VOLUNTEER SLOT",
        'location': "CPT",
        'description': 'You can book this slot if  you want to volunteer.',
        'colorId' : 6,
        'start': {
            'dateTime': '2024-02-22T16:00:00+02:00',
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': '2024-02-22T16:30:00+02:00',
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


def cancel_booking(creds, booking_info, USER_EMAIL):
    """
    Cancels the booking made by the user.

    Parameters:
        creds (Credentials): A Credentials object necessary to build a calendar.
        booking_info (dict): Contains information about the booking {'dateTime': date and time}
        USER_EMAIL (str): The current user's email.
    
    Returns:
        (success, message) (tuple): (var)success is whether the cancelling was a success or not(boolean). (vara)message is the appropriate message to display.
    """
    try:

        service = build('calendar', 'v3', credentials=creds)

        return remove_attendee(service, booking_info, USER_EMAIL)


    except HttpError as err:
        message = f"An error occured: {err}"
        print(message)


def remove_attendee(service, booking_info : dict, USER_EMAIL):
    """
    Removes an attendee with email=USER_EMAIL at an event that starts at booking_info['dateTime']

    Parameters:
        service (Resource): A Resource object with methods for interacting with the service.
        booking_info (dict): Contains information about the booking {'dateTime': date and time}
        USER_EMAIL (str): The current user's email.
    
    Returns:
        (success, message) (tuple): (var)success(boolean) is whether the removing was a success or not. (var)message(str) is the appropriate message to display.
    """
    date_time = booking_info['dateTime']

    now = dt.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(calendarId=CLINIC_CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()

    events = events_result.get("items", [])

    for event in events:
        if event['start']['dateTime'] == booking_info['dateTime'] and booked_event(event, USER_EMAIL):
            event['attendees'].pop()
            event['summary'] = "VOLUNTEER SLOT"
            event['description'] = "You can book this slot if  you want to volunteer."

            event_id = event['id']

            updated_event = service.events().update(calendarId=CLINIC_CALENDAR_ID, eventId=event_id, body=event).execute()

            message = "Booking Cancelled."
            return True, message

    message = "No booking to cancel."
    return False, message


def booked_event(event, USER_EMAIL: str) -> bool:
    """
    Returns whether the user is the one who booked the event

    Parameters:
        event (Event): An event object with information about the event.
        USER_EMAIL (str): The email of the current user.
    
    Returns:
        booked (bool): True is the user is the one who booked the event, otherwise returns False.
    """
    booked = False
    for attendee in event['attendees']:
        if attendee['email'] == USER_EMAIL:
            booked = True
    
    return booked


def get_start_date_time(user_input:str)-> str:
    """
    Returns the formatted start datetime from user_input

    Parameters:
        user_input (str): date and time from the user in the format ddThh:mm
    
    Returns:
        dateTime (str): Date and time in the format yyyy:mm:ddThh:mm:00+02:00

    """
    now = dt.datetime.utcnow().isoformat() + "Z"
    items = now.split("-")

    current_month = int(items[1])
    current_day = int(items[2][0:2])

    
    day = int(user_input.split("T")[0])
    time = user_input.split("T")[1]


    if day < current_day:
        current_month += 1
    

    if 1<=current_month<=9:
        current_month = f"0{current_month}" 

    return f"2024-{current_month}-{day}T{time}:00+02:00"
