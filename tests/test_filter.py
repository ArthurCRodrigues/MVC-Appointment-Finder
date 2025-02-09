import unittest
from unittest.mock import patch, MagicMock
from locationRetriever import Filter
from model import Location
from datetime import datetime, timedelta

class TestFilter(unittest.TestCase):
    def test_filter_valid_data(self):
        """
        Test the filter() method with a valid set of Location objects.

        This test creates mock Location objects with varying next appointment dates
        and sets a day range of 3. It verifies that:
        - Only locations within the 3-day range are returned.
        - The returned list is sorted in ascending order by next_appointment_date.
        """
        mock_locations = [
            Location("Location A", "123 Main St", "Springfield", "IL", "62704", "555-1234", 5,
                     datetime.now() + timedelta(days=1)),  # Tomorrow
            Location("Location B", "456 Elm St", "Chicago", "IL", "60601", "312-555-6789", 3,
                     datetime.now() + timedelta(days=3)),  # 3 days later
            Location("Location C", "789 Oak St", "Naperville", "IL", "60563", "630-555-9876", 1,
                     datetime.now() + timedelta(days=5))  # 5 days later
        ]

        filter_instance = Filter(days=3)
        filter_instance.retriever.locations = mock_locations

        filtered_locations = filter_instance.filter()

        # Assertions to check correct filtering and sorting
        self.assertEqual(len(filtered_locations), 2)
        self.assertEqual(filtered_locations[0].name, "Location A")
        self.assertEqual(filtered_locations[1].name, "Location B")

    def test_filter_empty_locations(self):
        """
        Test the filter() method with an empty locations list.

        This test verifies that when no locations are available:
        - The filter() method returns an empty list.
        """
        filter_instance = Filter(days=3)
        filter_instance.retriever.locations = []  # No locations

        filtered_locations = filter_instance.filter()

        # Assert that the result is an empty list
        self.assertEqual(filtered_locations, [])

    def test_filter_no_match(self):
        """
        Test the filter() method when no locations match the day range.

        This test creates mock Location objects where all next appointment dates
        fall outside the specified 3-day range. It verifies that:
        - The filter() method returns an empty list.
        """
        mock_locations = [
            Location("Location A", "123 Main St", "Springfield", "IL", "62704", "555-1234", 5,
                     datetime.now() + timedelta(days=4)),  # 4 days later
            Location("Location B", "456 Elm St", "Chicago", "IL", "60601", "312-555-6789", 3,
                     datetime.now() + timedelta(days=7)),  # 7 days later
            Location("Location C", "789 Oak St", "Naperville", "IL", "60563", "630-555-9876", 1,
                     datetime.now() + timedelta(days=5))  # 5 days later
        ]

        filter_instance = Filter(days=3)
        filter_instance.retriever.locations = mock_locations

        filtered_locations = filter_instance.filter()

        # Assert that no locations match the 3-day range
        self.assertEqual(filtered_locations, [])
