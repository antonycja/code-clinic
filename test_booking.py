from unittest import TestCase, main
from booking import book_slot,cancel_booking, get_start_date_time, authenticate, CLINIC_CALENDAR_ID, export_to_ical
import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

USER_EMAIL = 'btshulisi023@student.wethinkcode.co.za'
creds = authenticate()

now = datetime.datetime.utcnow().isoformat() + "Z"
items = now.split("-")

month_now_str = items[1]
day_now_str = items[2][0:2]

day_now_int, month_now_int = int(day_now_str), int(month_now_str)

class TestBooking(TestCase):
    def test_get_start_date_time(self):
         # "2024-06-16 08:00:00"


        

        user_input = f"{day_now_str}T14:00"

        actual_output = get_start_date_time(user_input)
        desired_output = f"2024-{month_now_str}-{day_now_str}T14:00:00+02:00"
        
        self.assertEqual(desired_output, actual_output)
    

    def test_get_start_date_time_oclock(self):
        now = datetime.datetime.utcnow().isoformat() + "Z" # "2024-06-16 08:00:00"
        items = now.split("-")

        month_now_str = items[1]
        day_now_str = items[2][0:2]

        day_now_int, month_now_int = int(day_now_str), int(month_now_str)

        

        user_input = f"{day_now_str}T14"

        actual_output = get_start_date_time(user_input)
        desired_output = f"2024-{month_now_str}-{day_now_str}T14:00:00+02:00"
        
        self.assertEqual(desired_output, actual_output)
    

    def test_get_start_date_time_invalid_time(self):
        now = datetime.datetime.utcnow().isoformat() + "Z" # "2024-06-16 08:00:00"
        items = now.split("-")

        month_now_str = items[1]
        day_now_str = items[2][0:2]

        day_now_int, month_now_int = int(day_now_str), int(month_now_str)

        

        user_input = f"{day_now_str}T7:00"

        actual_output = get_start_date_time(user_input)
        desired_output = "invalid time."
        
        self.assertEqual(desired_output, actual_output)


    def test_get_start_date_time_no_seperator(self):
        now = datetime.datetime.utcnow().isoformat() + "Z" # "2024-06-16 08:00:00"
        items = now.split("-")

        month_now_str = items[1]
        day_now_str = items[2][0:2]

        day_now_int, month_now_int = int(day_now_str), int(month_now_str)

        

        user_input = f"{day_now_str} 14:00"

        actual_output = get_start_date_time(user_input)
        desired_output = "invalid input. No 'T' seperator."
        
        self.assertEqual(desired_output, actual_output)


    def test_book_slot(self):
        service = service = build('calendar', 'v3', credentials=creds)
        
        #Create a volunteer slot
        event = {
        "summary" : "VOLUNTEER SLOT",
        'location': "CPT",
        'description': 'You can book this slot if  you want to volunteer.',
        'colorId' : 6,
        'start': {
            'dateTime': f"2024-{month_now_str}-{day_now_str}T16:00:00+02:00",
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': f'2024-{month_now_str}-{day_now_str}T16:30:00+02:00',
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

        booking_info = dict()
        booking_info['dateTime'] = f"{day_now_str}T16:00"
        booking_info['description'] = "Help me with arrays."

        success, message = book_slot(creds, booking_info, USER_EMAIL)
        desired_success, desired_message = True, "Booking Successful!"

        self.assertEqual(desired_success, success)
        self.assertEqual(desired_message, message)

        #Delete the event
        service.events().delete(calendarId=CLINIC_CALENDAR_ID, eventId=event['id']).execute()


    def test_book_slot_already_booked(self):
        service = service = build('calendar', 'v3', credentials=creds)
        
        #Create a volunteer slot
        event = {
        "summary" : "VOLUNTEER SLOT",
        'location': "CPT",
        'description': 'You can book this slot if  you want to volunteer.',
        'colorId' : 6,
        'start': {
            'dateTime': f"2024-{month_now_str}-{day_now_str}T16:00:00+02:00",
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': f'2024-{month_now_str}-{day_now_str}T16:30:00+02:00',
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

        booking_info = dict()
        booking_info['dateTime'] = f"{day_now_str}T16:00"
        booking_info['description'] = "Help me with arrays."

        success, message = book_slot(creds, booking_info, USER_EMAIL)
        desired_success, desired_message = True, "Booking Successful!"

        self.assertEqual(desired_success, success)
        self.assertEqual(desired_message, message)

        booking_info = dict()
        booking_info['dateTime'] = f"{day_now_str}T16:00"
        booking_info['description'] = "Help me with dics."

        success, message = book_slot(creds, booking_info, USER_EMAIL)
        desired_success, desired_message = False, "Slot is already booked. Try another!"
        #Delete the event
        service.events().delete(calendarId=CLINIC_CALENDAR_ID, eventId=event['id']).execute()
    
    
    def test_book_slot_volunteer(self):
        service = service = build('calendar', 'v3', credentials=creds)
        
        #Create a volunteer slot
        event = {
        "summary" : "VOLUNTEER SLOT",
        'location': "CPT",
        'description': 'You can book this slot if  you want to volunteer.',
        'colorId' : 6,
        'start': {
            'dateTime': f"2024-{month_now_str}-{day_now_str}T16:00:00+02:00",
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': f'2024-{month_now_str}-{day_now_str}T16:30:00+02:00',
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

        booking_info = dict()
        booking_info['dateTime'] = f"{day_now_str}T16:00"
        booking_info['description'] = "Help me with arrays."

        success, message = book_slot(creds, booking_info,  "bulelatshulisi@gmail.com")
        desired_success, desired_message = False, "You are a volunteer for this slot. You cannot book it!"

        self.assertEqual(desired_success, success)
        self.assertEqual(desired_message, message)

        #Delete the event
        service.events().delete(calendarId=CLINIC_CALENDAR_ID, eventId=event['id']).execute()
    
    
    def test_cancel_booking(self):
        service = service = build('calendar', 'v3', credentials=creds)
        
        #Create a volunteer slot
        event = {
        "summary" : "VOLUNTEER SLOT",
        'location': "CPT",
        'description': 'You can book this slot if  you want to volunteer.',
        'colorId' : 6,
        'start': {
            'dateTime': f"2024-{month_now_str}-{day_now_str}T16:00:00+02:00",
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': f'2024-{month_now_str}-{day_now_str}T16:30:00+02:00',
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

        booking_info = dict()
        booking_info['dateTime'] = f"{day_now_str}T16:00"
        booking_info['description'] = "Help me with arrays."

        success, message = book_slot(creds, booking_info, USER_EMAIL)
        desired_success, desired_message = True, "Booking Successful!"

        self.assertEqual(desired_success, success)
        self.assertEqual(desired_message, message)

        #Cancel Booking

        success, message = cancel_booking(creds, booking_info, USER_EMAIL)
        desired_success, desired_message = True, "Booking Cancelled."

        #Delete the event
        service.events().delete(calendarId=CLINIC_CALENDAR_ID, eventId=event['id']).execute()


    def test_export_to_ical(self):
        file_path = "bookings.ics"
        actual_message = export_to_ical(creds, file_path)
        desired_message = f"Bookings exported to {file_path}"

        self.assertEqual(desired_message, actual_message)
        self.assertTrue(os.path.exists(file_path))

        os.remove(file_path)


if __name__=="__main__":
    main()
