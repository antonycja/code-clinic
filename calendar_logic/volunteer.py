from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from booking import is_occupied

calendar_id = "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"

def build_service(creds):
    """
    Creates a google service object using oauth2.0.
    The service is required in order to create,update and delete events

    Args:
        creds (object): google service (object)
    """

    try:
        service = build('calendar', 'v3', credentials=creds)

    except HttpError as error:
        exit("An error occurred:", error)

    return service



def create_volunteer_slot(creds, volunteer_email, starttime, endtime, campus, calendar_id: str = calendar_id):
    """
    Create a volunteer slot event on the specified Google Calendar.

    Args:
        service - (googleapiclient.discovery.Resource): Google Calendar service instance.
        calendar_id (str): ID of the Google Calendar.
        volunteer_email (str): Email of the volunteer.
        event_description (str): Description of the event.
        starttime (str): Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        endtime (str): End time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        campus (str): Location or campus of the event.

    Returns:
        None
    """
    service = build_service(creds)
    if not is_booked(starttime, endtime, volunteer_email, service, calendar_id):
        try:
            event = {
                'summary': 'VOLUNTEER SLOT',
                'location': campus,
                'description': "Join this event for a code-clinic session with a volunteer.",
                'start': {
                    'dateTime': starttime,
                    'timeZone': 'Africa/Johannesburg'
                },
                'end': {
                    'dateTime': endtime,
                    'timeZone': 'Africa/Johannesburg'
                },
                'attendees': [
                    {'email': volunteer_email,
                    'responseStatus': 'accepted'},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'popup', 'minutes': 10}
                    ],
                },
                'maxAttendees': 2
                }

            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            message = "Slot successfully created."
        except HttpError as error:
            message = f"An error occurred: {error}"
    else:
        message = "You are already attending a session at the specified time."

    return message


def is_booked(starttime, endtime, email, service, calendar_id):
    """
    Check if a volunteer has already booked a slot for the specified time.

    Args:
        starttime (str): Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        endtime (str): End time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        email (str): Email of the volunteer.
        service (googleapiclient.discovery.Resource): Google Calendar service instance.
        calendar_id (str): ID of the Google Calendar.

    Returns:
        bool: True if the slot is booked; False otherwise.
    """
    event_id = get_event(service, calendar_id, starttime, endtime, email)
    if not event_id:
        return False
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    if is_occupied(event, email):
        return True
    start = event['start']['dateTime']
    if start == starttime:
        attendee = event['attendees'][0]['email']
        if attendee == email:
            return True
    return False


def get_event(service, calendar_id, starttime, endtime, volunteer_email):
    """
    Retrieve the event ID for the event within the specified time frame.

    Args:
        service (googleapiclient.discovery.Resource): Google Calendar service instance.
        calendar_id (str): ID of the Google Calendar.
        starttime (str): Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        endtime (str): End time of the event in 'YYYY-MM-DDTHH:MM:SS' format.

    Returns:
        str: Event ID if an event is found within the specified time frame; None otherwise.
    """
    try:
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=starttime,
                timeMax=endtime,
                singleEvents=True,
                orderBy='startTime'
            )
        .execute()
        )
        events = events_result.get('items', [])
        if events:
            for event in events:
                if event['attendees'][0]['email'] == volunteer_email:
                    return event['id']
                else:
                    print("You have not volunteered yet.")
                    return None
    except IndexError as error:
        print(f'There is not a slot booked for the specified time')
        return None

def cancel_event(creds, starttime, endtime, volunteer_email, calendar_id = calendar_id):
    """
    Cancel the event within the specified time frame.

    Args:
        service (googleapiclient.discovery.Resource): Google Calendar service instance.
        calendar_id (str): ID of the Google Calendar.
        starttime (str): Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        endtime (str): End time of the event in 'YYYY-MM-DDTHH:MM:SS' format.

    Returns:
        None
    """
    service = build_service(creds)

    try:
        event_id = get_event(service, calendar_id, starttime, endtime, volunteer_email)
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        if len(event['attendees']) > 1:
            message = 'You cannot cancel a slot that has already been booked by a student.'
        
        elif event['attendees'][0]['email'] != volunteer_email:
            message = 'you cannot cancel a slot that you have not volunteered for.'

        else:
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            message = 'Slot successfully cancelled.'

    except TypeError as error:
        message = 'You cannot cancel a slot that you are not attending.'

    return message

def end_time(start_time:str):
    """
    Generates the end time of the meeting.
    Each meeting is meant to last for 30 minutes.

    Args:
        start_time (str): The start time of the meeting

    Returns:
        str : the end time of the meeting
    """
    
    time = start_time.split(':')
    hours = int(time[0])
    min = int(time[1]) + 30
    
    if min >= 60:
        min = 0
        hours += 1
        
        if hours > 23:
            hours = 0
    else:
        pass
    
    if hours < 10:
        hours = f'0{hours}'
    
    if min < 10:
        min = f'0{min}'
    
    return f'{hours}:{min}'


def campus_abb(campus: str):
    """
    Returns the correct campus abbreviation of the students current campus

    Args:
        campus (str): The campus the student is attending

    Returns:
        str : the abbreviation of the campus name
    """
    
    campuses = ['CPT','JHB','DBN','CJC']
    
    if campus == "" or len(campus) < 3:
        return ""

    if campus.upper() in campuses:
        return campus.upper()
    
    if campus.upper() == 'CAPE TOWN':
        campus = campuses[0]
    elif campus.upper() == 'JOHANNESBURG' or campus.upper() == 'JOBURG':
        campus = campuses[1]
    elif campus.upper() == 'DURBAN':
        campus = campuses[2]
    else:
        campus = ""

    return campus

