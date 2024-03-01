from authentication.auth import *
from calendar_logic.volunteer import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

creds = authenticate_user()
calendar_id = "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"

try:
    service = build('calendar', 'v3', credentials=creds)

except HttpError as error:
        print("An error occured:", error) 

event_description = 'Join this event if you need help.'
# volunteer_email = 'amaposa023@student.wethinkcode.co.za'
volunteer_email = 'cthomas023@student.wethinkcode.co.za'
starttime = '2024-03-01T14:00:00+02:00'
endtime = '2024-03-01T14:30:00+02:00'
# starttime = '2024-02-26T17:00:00+02:00'
# endtime = '2024-02-26T17:30:00+02:00'
campus = 'WTC CPT'

if __name__ == '__main__':
    create_volunteer_slot(creds, volunteer_email, starttime, endtime, campus)
    # cancel_event(creds, starttime, endtime, volunteer_email)
