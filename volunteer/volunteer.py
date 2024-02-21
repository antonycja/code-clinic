from googleapiclient.errors import HttpError
from datetime import datetime, timedelta


def create_volunteer_slot(service, calendar_id, volunteer_email, event_description, date_time, campus):
    
    start_time = date_time
    end_time = start_time + timedelta(minutes = 30)
    if not is_booked(start_time, volunteer_email, service, calendar_id):
        # try:
        #     event = {
        #         'summary': 'Volunteer Slot',
        #         'location': campus,
        #         'description': event_description,
        #         'start': {
        #             'dateTime': start_time.isoformat(),
        #             'timeZone': 'Africa/Johannesburg'
        #         },
        #         'end': {
        #             'dateTime': end_time.isoformat(),
        #             'timeZone': 'Africa/Johannesburg'
        #         },
        #         'attendees': [
        #             {'email': volunteer_email,
        #             'responseStatus': 'accepted'}
        #         ],
        #         'reminders': {
        #             'useDefault': False,
        #             'overrides': [
        #             {'method': 'popup', 'minutes': 10}
        #             ],
        #         },
        #         'maxAttendees': 2
        #         }

        #     event = service.events().insert(calendarId=calendar_id, body=event).execute()
        #     print('Events created: %s' % (event.get('htmlLink')))
        # except HttpError as error:
        #     print("An error occured:", error)
        print("event created")
    else:
        print("You are already attending a session at the specified time.")

def is_booked(start_time, email, service, calendar_id) -> bool:
    events = get_slots(service, calendar_id)

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if start == start_time:
            for attendee in event['attendee']:
                print(attendee['email'])
                if attendee['email'] == email:
                    return True
    
    return False


def get_slots(service, calendar_id):
    today = datetime.today()
    eight_am_today = today.isoformat() + 'T08:00:00Z'
    events_result = service.events().list(calendarId=calendar_id, timeMin=eight_am_today, maxResults=250, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items' , [])
    return events