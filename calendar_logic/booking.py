"""
This module is designed for booking functions
"""


import datetime as dt
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



CLINIC_CALENDAR_ID = "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"
YEAR = 2024
months = {
    1 : 31,
    2 : 29,
    3 : 31,
    4 : 30,
    5 : 31,
    6 : 30,
    7 : 31,
    8 : 31,
    9 : 30,
    10: 31,
    11: 30,
    12: 31,
}




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
            elif is_volunteer(event, USER_EMAIL):
                message = "You are a volunteer for this slot. You cannot book it!"
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

def is_volunteer(event, USER_EMAIL) -> bool:
    return is_attendee(event, USER_EMAIL)


def is_attendee(event, USER_EMAIL):
    attendee = event['attendees'][0]

    return attendee['email'] == USER_EMAIL



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
        message = f"An error occurred: {err}"
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
            event['description'] = "You can book this slot if you need help."

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

    if "T" not in user_input:
        return "invalid input. No 'T' seperator."
    
    if not user_input.split("T")[0].isdigit():
        return "invalid input. Day is not a digit."
    
    day = int(user_input.split("T")[0])
    time = user_input.split("T")[1]

    if not time_valid(time):
        return "invalid time."
    
    time = format_time(time)


    if day < current_day:
        booking_month = current_month + 1
    else:
        booking_month = current_month

    if day > months[int(current_month)]:
        return "invalid date."
    
    current_date = dt.datetime(2024, current_month, current_day )
    booking_date = dt.datetime(2024, booking_month, day )

    delta = booking_date - current_date

    difference_in_days = delta.days

    if difference_in_days > 6:
        print(difference_in_days)
        return "invalid date. Out of range."


    if 1<=current_month<=9:
        current_month = f"0{current_month}" 

    if 1 <= day <= 9:
        day = f"0{day}"



    return f"2024-{booking_month}-{day}T{time}:00+02:00"


def format_time(time : str):
    """
    Formats time from user into the hh:mm format

    Parameters:
    time (str): can be in the hh:mm format or hh

    Returns:
    time (str): in the format hh:mm
    """
    if ":" in time:
        times = time.split(":")
        hh = int(times[0])
        mm = int(times[1])

        if 8 <= hh <= 9:
            hh = f"0{hh}"

        if mm == 0:
            mm = "00"

        time = f"{hh}:{mm}"
    else:
        hh = int(time)

        if 8 <= hh <= 9:
            hh = f"0{hh}"

        time = f"{hh}:00"

    return time


def time_valid(time : str)->bool:
    """
    Check if the time provided by the user is valid.

    Parameters:
    time (str): Time provided by the user in the format hh:mm or hh

    Returns:
    is_time_valid (bool): Returns True if the time is valid False otherwise.
    """

    hour_valid = False
    minute_valid = False
    if ':' in time:
        times = time.split(":")
        hh = times[0]
        mm = times[1]
        if hh.isdigit():
            hh = int(hh)
            hour_valid = 8 <= hh <= 17
        
        if mm.isdigit():
            mm = int(mm)
            minute_valid = mm in [0, 30]
    else:
        minute_valid = True
        if time.isdigit():
            hh = int(time)
            hour_valid = 8 <= hh <= 17
    
    is_time_valid = minute_valid and hour_valid

    return is_time_valid      
