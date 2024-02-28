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

class Test_Volunteer(unittest.TestCase):
    
    def test_get_event(self):
        self.assertEqual(volunteer.get_event())