from authentication.auth import *
from volunteer.volunteer import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

creds = authenticate_user()
calendar_id = "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"

try:
    service = build('calendar', 'v3', credentials=creds)

except HttpError as error:
        print("An error occured:", error) 

event_description = 'Join this event if you want to book a session with a volunteer.'
volunteer_email = 'cthomas023@student.wethinkcode.co.za'
date_time = datetime(2024, 2, 22, 8, 0, 0)
campus = 'WTC CPT'


create_volunteer_slot(service, calendar_id, volunteer_email, event_description, date_time, campus)

        