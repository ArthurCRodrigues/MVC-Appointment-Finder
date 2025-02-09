import unittest
from unittest.mock import patch, MagicMock
from model import Location
from datetime import datetime

class TestLocation(unittest.TestCase):
    def test_get_appointment_number_valid_data(self):
        """
        Test get_appointment_number() with valid appointment string.

        This test verifies that when a valid appointment string is passed,
        the method correctly extracts and returns the number of available slots.
        """
        appointment_str = "5 slots available - Next Available: 03/15/2024 09:00 AM"
        appointment_number = Location.get_appointment_number(appointment_str)
        self.assertEqual(appointment_number, 5)

    def test_get_appointment_number_invalid_data(self):
        """
        Test get_appointment_number() with an invalid appointment string.

        This test ensures that the method returns None when it cannot parse
        a valid appointment number from the given string.
        """
        appointment_number = Location.get_appointment_number("Invalid appointment number")
        self.assertIsNone(appointment_number)

    def test_get_next_date_valid_data(self):
        """
        Test get_next_date() with a valid appointment string.

        This test verifies that the method extracts and returns a valid datetime object
        for the next available appointment from the given string.
        """
        appointment_str = "5 slots available - Next Available: 03/15/2024 09:00 AM"
        appointment_date = Location.get_next_date(appointment_str)
        self.assertEqual(appointment_date, datetime(2024, 3, 15, 9, 0))

    def test_get_next_date_invalid_data(self):
        """
        Test get_next_date() with an invalid appointment string.

        This test ensures that the method returns None when it cannot parse
        a valid appointment date from the given string.
        """
        appointment_date = Location.get_next_date("Invalid appointment date")
        self.assertIsNone(appointment_date)

    def test_create_location_valid(self):
        """
        Test create_location() with valid input data.

        This test verifies that when both location_dict and time_dict contain valid data,
        the method creates a Location object with the expected attributes.
        """
        location_dict = {
            "Name": "Health Center",
            "Street1": "123 Main St",
            "City": "Alpine",
            "State": "NJ",
            "Zip": "62704",
            "PhoneNumber": "555-1234",
        }
        time_dict = {
            "LocationId": 101,
            "FirstOpenSlot": "5 slots available - Next Available: 03/15/2024 09:00 AM",
            "status": "Available"
        }

        location_obj = Location.create_location(location_dict, time_dict)

        self.assertEqual(type(location_obj), Location)
        self.assertEqual(location_obj.name, "Health Center")
        self.assertEqual(location_obj.street, "123 Main St")
        self.assertEqual(location_obj.appointments, 5)
        self.assertEqual(location_obj.next_appointment_date.strftime("%m/%d/%Y %I:%M %p"), "03/15/2024 09:00 AM")

    def test_create_location_invalid(self):
        """
        Test create_location() with empty dictionaries.

        This test verifies that when location_dict and time_dict are empty,
        the method returns None, indicating that it cannot create a valid Location object.
        """
        location_obj = Location.create_location({}, {})
        self.assertIsNone(location_obj)

    def test_create_location_missing_keys(self):
        """
        Test create_location() with missing keys in time_dict.

        This test ensures that when the required keys (e.g., FirstOpenSlot) are missing from time_dict,
        the method returns None, indicating an incomplete data set.
        """
        location_dict = {
            "Name": "Health Center",
            "Street1": "123 Main St",
            "City": "Alpine",
            "State": "NJ",
            "Zip": "62704",
            "PhoneNumber": "555-1234",
        }
        time_dict = {
            "LocationId": 101,
            "status": "Available"
        }

        location_obj = Location.create_location(location_dict, time_dict)
        self.assertIsNone(location_obj)

if __name__ == "__main__":
    unittest.main()
