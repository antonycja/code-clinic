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
            print('Events created: %s' % (event.get('htmlLink')))
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