import unittest
from unittest.mock import patch, MagicMock

import requests
from bs4 import BeautifulSoup
from locationRetriever import LocationRetriever
from model import Location
from datetime import datetime, timedelta

class TestLocationRetriever(unittest.TestCase):
    @patch("locationRetriever.requests.get")  # Mock requests.get()
    def test_get_tags_success(self, mock_get):
        """Test get_tags() returns script tags when given a valid HTML response"""
        mock_html = """
        <html>
            <head></head>
            <body>
                <script>var locationData = [{...}];</script>
                <script>var timeData = [{...}];</script>
            </body>
        </html>
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_html

        retriever = LocationRetriever()
        script_tags = retriever.get_tags("Doensn't matter!")

        self.assertEqual(len(script_tags), 2)  # Expecting two <script> tags
        self.assertIsInstance(script_tags, list)
        self.assertIsInstance(script_tags[0], type(BeautifulSoup().new_tag("script")))  # Check if script tag

    @patch("locationRetriever.requests.get")
    def test_get_tags_request_failure(self, mock_get):
        """Test get_tags() handles failed requests properly"""
        mock_get.side_effect = requests.RequestException("Network Error")

        retriever = LocationRetriever()
        script_tags = retriever.get_tags("https://telegov.njportal.com/njmvc/AppointmentWizard/12")

        self.assertEqual(script_tags, [])  # Should return an empty list

    @patch("locationRetriever.requests.get")
    def test_get_tags_no_script_tags(self,mock_get):
        """Test get_tags() returns [] when given a HTML with no script tags"""
        mock_html = "<html><head></head><body><p>No scripts here</p></body></html>"
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_html

        retriever = LocationRetriever()
        script_tags = retriever.get_tags("https://telegov.njportal.com")

        self.assertEqual(script_tags, [])

    def test_find_location_valid_data(self):
        script_tags = [
            BeautifulSoup('<script>console.log("Some script");</script>', 'html.parser').script,
            BeautifulSoup('<script>var locationData = [{"id": 1, "name": "Location A"}];</script>',
                          'html.parser').script,
        ]

        retriever = LocationRetriever()
        location_data = retriever.find_location(script_tags)

        self.assertEqual(location_data,'[{"id": 1, "name": "Location A"}]')
        self.assertEqual(type(location_data),str)

    def test_find_location_no_locationData(self):
        script_tags = [
            BeautifulSoup('<script>console.log("This is some irrelevant script.");</script>', 'html.parser').script,
            BeautifulSoup('<script>var timeData = [{"id": 1, "time": "10:00 AM"}];</script>', 'html.parser').script,
            BeautifulSoup('<script>function testFunc() { console.log("test"); }</script>', 'html.parser').script,
            BeautifulSoup('<script>var otherData = [{"id": 2, "data": "example"}];</script>', 'html.parser').script,
        ]

        retriever = LocationRetriever()

        with self.assertRaises(ValueError) as context:
            location_data = retriever.find_location(script_tags)

        self.assertEqual(str(context.exception),"Couldn't find data.")

    def test_find_location_empty_script_tags(self):
        script_tags = []

        retriever = LocationRetriever()
        location_data = retriever.find_location(script_tags)

        self.assertEqual(location_data,None)

    def test_find_time_valid_data(self):
        script_tags = [
            BeautifulSoup('<script>console.log("This is some irrelevant script.");</script>', 'html.parser').script,
            BeautifulSoup('<script>var timeData = [{"id": 1, "time": "10:00 AM"}];</script>', 'html.parser').script,
            BeautifulSoup('<script>function testFunc() { console.log("test"); }</script>', 'html.parser').script,
            BeautifulSoup('<script>var otherData = [{"id": 2, "data": "example"}];</script>', 'html.parser').script,
        ]

        retriever = LocationRetriever()
        time_data = retriever.find_time(script_tags)

        self.assertEqual(time_data,'[{"id": 1, "time": "10:00 AM"}]')
        self.assertEqual(type(time_data),str)

    def test_find_time_no_script_tags(self):
        script_tags = [
            BeautifulSoup('<script>console.log("Some script");</script>', 'html.parser').script,
            BeautifulSoup('<script>var locationData = [{"id": 1, "name": "Location A"}];</script>',
                          'html.parser').script,
        ]

        retriever = LocationRetriever()

        with self.assertRaises(ValueError) as context:
            time_data = retriever.find_time(script_tags)

        self.assertEqual(str(context.exception),"Couldn't find data.")

    def test_find_time_empty_script_tags(self):
        script_tags = []

        retriever = LocationRetriever()
        time_data = retriever.find_time(script_tags)

        self.assertEqual(time_data,None)

    def test_pase_data_valid_data(self):

        location_data = '[{"id": 1, "name": "Location A"}]'
        time_data = '[{"LocationId": 1, "name": "Location A"}]'

        retriever = LocationRetriever()
        location_dict,time_dict = retriever.parse_data(location_data,time_data)

        expected_location_dict = [{'id': 1, 'name': 'Location A'}]
        expected_time_dict = {1: {'LocationId': 1, 'name': 'Location A'}}

        self.assertEqual(location_dict,expected_location_dict)
        self.assertEqual(time_dict,expected_time_dict)

        self.assertEqual(type(location_dict),list) #list of dicts
        self.assertEqual(type(time_dict),dict)

    def test_parse_data_missing_keys(self):
        """Missing LocationId"""
        location_data = '[{"id": 1, "name": "Location A"}]'
        time_data = '[{"id": 1, "name": "Location A"}]'

        retriever = LocationRetriever()
        location_dict,time_dict = retriever.parse_data(location_data,time_data)

        self.assertIsNone(location_dict)
        self.assertIsNone(time_dict)

    def test_parse_data_None_input(self):
        retriever = LocationRetriever()

        with self.assertRaises(ValueError) as context:
            location_dict, time_dict = retriever.parse_data(None, None)

        self.assertEqual(str(context.exception),"Couldn't find data.")

    def test_parse_data_malformed_input(self):

        malformed_location_data = '[{"id": 1, "name": "Location A"'  # Missing closing brace
        malformed_time_data = '[{"id": 1, "time": "10:00 AM"'  # Missing closing brace

        retriever = LocationRetriever()

        location_dict, time_dict = retriever.parse_data(malformed_location_data, malformed_time_data)

        self.assertIsNone(location_dict)
        self.assertIsNone(time_dict)

    def test_get_dict_valid_data(self):

        location_dict = {
            "name": "Location A",
            "LocAppointments": [
                {"LocationId": 101, "status": "Available", "nextSlot": "03/15/2024 09:00 AM"}
            ]
        }
        time_dict = {101: {'LocationId': 101, 'name': 'Location A'},102: {'LocationId': 102, 'name': 'Location B'}}

        retriever = LocationRetriever()
        found_dict = retriever.get_dict(location_dict, time_dict)

        self.assertEqual(found_dict,{'LocationId': 101, 'name': 'Location A'})
        self.assertEqual(type(found_dict),dict)

    def test_get_dict_not_found(self):
        location_dict = {
            "name": "Location A",
            "LocAppointments": [
                {"LocationId": 101, "status": "Available", "nextSlot": "03/15/2024 09:00 AM"}
            ]
        }
        time_dict = {103: {'LocationId': 103, 'name': 'Location C'}, 104: {'LocationId': 104, 'name': 'Location D'}}

        retriever = LocationRetriever()
        found_dict = retriever.get_dict(location_dict, time_dict)

        self.assertIsNone(found_dict)

    def test_get_dict_invalid_input(self):

        retriever = LocationRetriever()
        found_dict = retriever.get_dict({}, {})

        self.assertIsNone(found_dict)

    def test_get_locations_valid_data(self):
        def test_get_locations_success(self):
            """Test get_locations() with valid location_json and time_dict"""
            retriever = LocationRetriever()

            # Mocked location_json and time_dict for the test
            location_json = [
                {
                    "id": 1,
                    "name": "Location A",
                    "LocAppointments": [
                        {"LocationId": 101, "status": "Available", "nextSlot": "03/15/2024 09:00 AM"}
                    ]
                }
            ]

            time_dict = {
                101: {
                    "LocationId": 101,
                    "FirstOpenSlot": "5 slots available - Next Available: 03/15/2024 09:00 AM",
                    "status": "Available"
                }
            }

            # Call get_locations() with the mocked data
            locations = retriever.get_locations(location_json, time_dict)

            # Assertions
            self.assertIsInstance(locations, list)
            self.assertEqual(len(locations), 1)
            self.assertIsInstance(locations[0], Location)
            self.assertEqual(locations[0].name, "Location A")
            self.assertEqual(locations[0].appointments, 5)
            self.assertEqual(locations[0].next_appointment_date.strftime("%m/%d/%Y %I:%M %p"), "03/15/2024 09:00 AM")

    def test_get_locations_invalid_input(self):
        retriever = LocationRetriever()
        with self.assertRaises(ValueError) as context:
            retriever.get_locations({}, {})
        self.assertEqual(str(context.exception),"Couldn't find data.")

    def test_get_locations_return_empty_no_available(self):
        retriever = LocationRetriever()
        # Mocked location_json and time_dict for the test
        location_json = [
            {
                "id": 1,
                "name": "Location A",
                "LocAppointments": [
                    {"LocationId": 101, "status": "Available", "nextSlot": "03/15/2024 09:00 AM"}
                ]
            }
        ]

        time_dict = {
            101: {
                "LocationId": 101,
                "FirstOpenSlot": "No Appointments Available",
                "status": "Available"
            }
        }

        locations = retriever.get_locations(location_json, time_dict)
        self.assertEqual(locations,[])


if __name__ == "__main__":
    unittest.main()
