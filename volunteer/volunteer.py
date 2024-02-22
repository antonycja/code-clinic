from googleapiclient.errors import HttpError
from datetime import datetime, timedelta


def create_volunteer_slot(service, calendar_id, volunteer_email, event_description, starttime, endtime, campus):
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

    if not is_booked(starttime, endtime, volunteer_email, service, calendar_id):
        try:
            event = {
                'summary': 'Volunteer Slot',
                'location': campus,
                'description': event_description,
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
                    {'email': 'amaposa023@student.wethinkcode.co.za',
                    'responseStatus': 'accepted'}
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
            print("Slot successfully created.")
        except HttpError as error:
            print("An error occured:", error)
    else:
        print("You are already attending a session at the specified time.")


def is_booked(starttime, endtime, email, service, calendar_id) -> bool:
    """
    Check if the volunteer is already booked for a session during the specified time.

    Args:
        starttime (str): Start time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        endtime (str): End time of the event in 'YYYY-MM-DDTHH:MM:SS' format.
        email (str): Email of the volunteer.
        service (googleapiclient.discovery.Resource): Google Calendar service instance.
        calendar_id (str): ID of the Google Calendar.

    Returns:
        bool: True if the volunteer is booked; False otherwise.
    """
    event_id = get_event(service, calendar_id, starttime, endtime)
    if not event_id:
        return False
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    print(event)
    start = event['start']['dateTime']
    if start == starttime:
        attendee = event['attendees'][0]['email']
        print(attendee)
        if attendee == email:
            return True
    return False


def get_event(service, calendar_id, starttime, endtime) -> str:
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
        event = events_result.get('items', [])
        return event[0]['id']
    except IndexError as error:
        print(f'There are not slots booked for the specified time')
        return None

def cancel_event(service, calendar_id, starttime, endtime):
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
    try:
        event_id = get_event(service, calendar_id, starttime, endtime)
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        if len(event['attendees']) > 1:
            print('You cannot cancel a fully booked meeting.')
        else:
            service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            print('Slot successfully cancelled.')

    except TypeError as error:
        print('You cannot cancel a slot that does not exist.')