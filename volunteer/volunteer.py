from googleapiclient.errors import HttpError
from datetime import datetime, timedelta


def create_volunteer_slot(service, calendar_id, volunteer_email, event_description, starttime, endtime, campus):
    

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


def get_event(service, calendar_id, starttime, endtime):
    
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