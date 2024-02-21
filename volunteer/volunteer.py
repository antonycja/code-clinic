from googleapiclient.errors import HttpError
from datetime import datetime, timedelta


def create_volunteer_slot(service, calendar_id, volunteer_email, event_description, date_time, campus):
    
    start_time = date_time
    end_time = start_time + timedelta(minutes = 30)
    try:
        event = {
            'summary': 'Volunteer Slot',
            'location': campus,
            'description': event_description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Africa/Johannesburg'
            },
            'end': {
                'dateTime': end_time.isoformat(),
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
    

