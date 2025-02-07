import unittest
from unittest.mock import patch, MagicMock

import requests
from bs4 import BeautifulSoup
from locationRetriever import LocationRetriever

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
        print(f"Script tags length> {len(script_tags)}")

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

if __name__ == "__main__":
    unittest.main()
