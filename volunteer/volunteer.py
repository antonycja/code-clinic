from googleapiclient.errors import HttpError
from datetime import datetime, timedelta


def create_volunteer_slot(service, calendar_id):
    start_time = datetime(2023, 3, 1, 9, 0, 0) - timedelta(hours=2)  # Start time (Year, Month, Day, Hour, Minute, Second)

    end_time = datetime(2023, 3, 1, 10, 0, 0)  - timedelta(hours=2) #1 End time (Year, Month, Day, Hour, Minute, Second)

    interval = timedelta(minutes=30) 

    for i in range(20):
        event = {
        'summary': 'Open Slot',
        'location': 'WTC CPT',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'Africa/Johannesburg',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print('Events created: %s' % (event.get('htmlLink')))
        start_time += interval
        end_time += interval


