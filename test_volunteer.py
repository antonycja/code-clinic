import unittest
import datetime
from main import *
import time

class TestVolunteerFunctions(unittest.TestCase):
    
    def setUp(self):
        self.calendar_id = "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"
        self.volunteer_email = "cthomas@student.wethinkcode.co.za"
        self.starttime = '2024-01-01T17:00:00+02:00'
        self.endtime = '2024-01-01T17:30:00+02:00'
        self.campus = 'WTC CPT'

    def test_build_service(self):
        creds = authenticate_user()
        service = build_service(creds)
        self.assertIsNotNone(service)


    def test_create_volunteer_slot(self):
        cancel_event(creds, self.starttime, self.endtime,self.volunteer_email, self.calendar_id)
        message = create_volunteer_slot(creds, self.volunteer_email, self.starttime, self.endtime, self.campus, self.calendar_id)
        self.assertEqual(message, "Slot successfully created.")


    def test_create_volunteer_slot_already_booked(self):
        message = create_volunteer_slot(creds, self.volunteer_email, self.starttime, self.endtime, self.campus, self.calendar_id)
        message = create_volunteer_slot(creds, self.volunteer_email, self.starttime, self.endtime, self.campus, self.calendar_id)
        self.assertEqual(message, "You are already attending a session at the specified time.")
        cancel_event(creds, self.starttime, self.endtime,self.volunteer_email, self.calendar_id)


    def test_cancel_event(self):
        create_volunteer_slot(creds, self.volunteer_email, self.starttime, self.endtime, self.campus, self.calendar_id)
        message = cancel_event(creds, self.starttime, self.endtime,self.volunteer_email, self.calendar_id)
        self.assertEqual(message, 'Slot successfully cancelled.')


    def test_cancel_event_not_attending(self):
        create_volunteer_slot(creds, self.volunteer_email, self.starttime, self.endtime, self.campus, self.calendar_id)
        self.volunteer_email = 'amaposa023@wethinkcode.student.co.za'
        self.starttime = '2024-01-02T17:00:00+02:00'
        self.endtime = '2024-01-02T17:30:00+02:00'
        message = cancel_event(creds, self.starttime, self.endtime,self.volunteer_email, self.calendar_id)
        self.assertEqual(message, 'You cannot cancel a slot that you are not attending.')


    def test_campus_abb(self):
        campus = 'Cape Town'
        abb = campus_abb(campus)
        self.assertEqual(abb, 'CPT')


if __name__ == '__main__':
    unittest.main()
