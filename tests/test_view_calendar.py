import unittest
from calendar_logic.view_calendar import *
from auth import authenticate_user
from data import data

import random


class Test_view_calendar(unittest.TestCase):

    def setUp(self):
        self.creds = authenticate_user()
        self.service = build("calendar", "v3", credentials=self.creds)
        self.filename = "calendar_data.csv"
        self.calendar_dict = {"personal": "primary",
                              "clinic": "c_7f60d63097ebf921579ca266668826f490dc72478a9d37d17ad62046836f598a@group.calendar.google.com"}
        self.cal_type_list = ["PERSONAL calendar", "CODE CLINIC calendar"]

        self.events_list = data
        pass

    def test_get_valid_personal_events(self):
        rand_days = random.randint(2, 10)
        result = get_events(
            self.service, self.calendar_dict["personal"], rand_days)
        if result:
            self.assertIsInstance(result, list)
        else:
            self.assertIsNone(result)

    def test_get_invalid_personal_events(self):
        rand_days = random.randint(-5, 0)
        result = get_events(
            self.service, self.calendar_dict["personal"], rand_days)
        self.assertIsNone(result)
        result = get_events(self.service, self.calendar_dict["personal"], "")
        self.assertIsNone(result)
        result = get_events(self.service, 5, rand_days)
        self.assertIsNone(result)

    def test_get_valid_clinic_events(self):
        rand_days = random.randint(1, 10)
        result = get_events(
            self.service, self.calendar_dict["clinic"], rand_days)
        if result:
            self.assertIsInstance(result, list)
        else:
            self.assertIsNone(result)

    def test_get_invalid_clinic_events(self):
        rand_days = random.randint(-5, 0)
        result = get_events(
            self.service, self.calendar_dict["clinic"], rand_days)
        self.assertIsNone(result)

    def test_determine_calendar(self):
        result = determine_calendar(10, self.cal_type_list, self.calendar_dict)
        cal_type1, calendars1 = determine_calendar(
            0, self.cal_type_list, self.calendar_dict)
        cal_type2, calendars2 = determine_calendar(
            1, self.cal_type_list, self.calendar_dict)
        cal_type3, calendars3 = determine_calendar(
            2, self.cal_type_list, self.calendar_dict)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[1], list)
        self.assertIsInstance(result[0], str)
        self.assertEqual(cal_type1.lower(), "all calendars")
        self.assertListEqual(calendars1, list(self.calendar_dict.values()))
        self.assertEqual(cal_type2, self.cal_type_list[0])
        self.assertListEqual(calendars2, [self.calendar_dict["personal"]])
        self.assertEqual(cal_type3, self.cal_type_list[1])
        self.assertListEqual(calendars3, [self.calendar_dict["clinic"]])

    def test_create_event_info(self):
        result = create_event_info(self.events_list[1], self.cal_type_list[1])
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(len(result[0]), 8)
        self.assertEqual(result[0]["Calendar"], self.cal_type_list[1])
        self.assertIsInstance(result[0]["attendees"], list)
        

    def test_filter_events_valid(self):
        new_data = create_event_info(self.events_list[1], self.cal_type_list[1])
        result = filter_calendar_events(["wtc"], new_data)
        self.assertEqual(len(result), 1)
        self.assertDictEqual(result[0], new_data[1])
        
        result = filter_calendar_events(["Meeting"], new_data)
        self.assertEqual(len(result), 1)
        self.assertDictEqual(result[0], new_data[0])
        
        result = filter_calendar_events(["not bOOKED"], new_data)
        self.assertEqual(len(result), 5)
        self.assertListEqual(result, new_data[1:])
        
    
    def test_filter_events_multiple(self):
        new_data = create_event_info(self.events_list[1], self.cal_type_list[1])
        result = filter_calendar_events(["cpt"], new_data)
        self.assertEqual(len(result), 6)
        self.assertListEqual(result, new_data)
        
        result = filter_calendar_events(["wtc", "not booked"], new_data)
        self.assertEqual(len(result), 1)
        
        result = filter_calendar_events(["cpt", "meeting"], new_data)
        self.assertEqual(len(result), 1)
        
        result = filter_calendar_events(["cpt", "slot", "13:00"], new_data)
        self.assertEqual(len(result), 1)

    def test_filter_events_invalid(self):
        new_data = create_event_info(self.events_list[1], self.cal_type_list[1])
        result = filter_calendar_events(["w"], new_data)
        self.assertEqual(len(result), len(new_data))

        

if __name__ == "__main__":
    unittest.main()
