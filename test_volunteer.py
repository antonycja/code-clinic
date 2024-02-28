import unittest
import datetime
from main import *
import time

try:
    service = build('calendar', 'v3', credentials=creds)

except HttpError as error:
        print("An error occured:", error)

class Test_Volunteer(unittest.TestCase):
    
    def test_get_event(self):
        self.assertEqual(volunteer.get_event())