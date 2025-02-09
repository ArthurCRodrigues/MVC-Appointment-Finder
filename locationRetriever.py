from bs4 import BeautifulSoup, ResultSet
import requests,re,json
from datetime import datetime,timedelta

from model import Location

class LocationRetriever:
    """
    This class will only contain one attribute (locations) that will be set automatically upon instantiation. The attribute itself is a list of location objects with available appointments (regardless of date).
    """
    def __init__(self):
        self.locations = []

    def fetch_locations(self):
        """
        Handles all functions providing the necessary parameters (following the chain logic from the methods) and assign the final value to locations attribute.
        """
        script_tags = self.get_tags('https://telegov.njportal.com/njmvc/AppointmentWizard/12')
        location_data_str = self.find_location(script_tags)
        time_data_str = self.find_time(script_tags)

        location_json,time_dict = self.parse_data(location_data_str, time_data_str)

        if not location_json or not time_dict:
            raise ValueError("Couldn't find data.")

        self.locations = self.get_locations(location_json,time_dict)


    def get_tags(self,url: str):
        """
        Creates the soup from the appointmentWizard website using requests library and filters all the script tags in the document.
        :return:
            bs4 resultSet with all script tags found
        """
        try:
            req = requests.get(url, timeout=10)
            req.raise_for_status()  # Raises an error for bad responses
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        soup = BeautifulSoup(req.text, 'html.parser')
        return soup.find_all('script')

    def find_location(self, script_tags: ResultSet):
        """
        Iterates through the result set from getTags and uses regular expressions on the iterables in order to extract the locationData variable value (if existent).
        :return:
            IF FOUND: variable value as string
            IF NOT FOUND: None
        """
        if script_tags == []:
            return None
         # Regular expressions to extract locationData
        location_pattern = r'var locationData\s*=\s*(\[\{.*?\}\]);'
        for script_tag in script_tags:
            # Extract locationData
            location_match = re.search(location_pattern, str(script_tag), re.DOTALL)
            locationData = location_match.group(1) if location_match else None
            if locationData:
                return locationData

        raise ValueError("Couldn't find data.")

    def find_time(self, script_tags: ResultSet):
        """
        Iterates through the result set from getTags and uses regular expressions on the iterables in order to extract the timeData variable value (if existent).
        :return:
            IF FOUND: variable value as string
            IF NOT FOUND: None
        """
        if script_tags == []:
            return None
        time_pattern = r'var timeData = (\[.*?\])'
        for script_tag in script_tags:
            # Extract timeData
            time_match = re.search(time_pattern, str(script_tag), re.DOTALL)
            timeData = time_match.group(1) if time_match else None
            if timeData:
                return timeData
        raise ValueError("Couldn't find data.")

    def parse_data(self, locationData: str, timeData: str):
        """
        gets both strings from findLocation and findTime and uses json library to map them into python dicts. Hashes time_json dict to make its access linear in the future
        :return:
        """
        try:
            if not locationData or not timeData:
                raise ValueError("Couldn't find data.")
            location_json = json.loads(locationData)
            time_json = json.loads(timeData)
            time_dict = {}
            for obj in time_json:
                if not obj.get("LocationId"):
                    return None,None
                time_dict[obj["LocationId"]] = obj  # Fills a new dictionary with the location id as a key for that dict (linear access)
            # Basically hashed the dict
            return location_json,time_dict
        except json.decoder.JSONDecodeError as e:
            print("Error: ",e)
            return None,None

    def get_locations(self,location_json: dict,time_dict: dict):
        """
        takes both dicts containing location info as parameter and map the ones with available appointments into location objects
        :return:
            list of Location objects with available appointments
        """
        if not location_json or not time_dict:
            raise ValueError("Couldn't find data.")

        locations = []

        for obj in location_json:
            dict = self.get_dict(obj,time_dict)
            if not dict:
                continue
            if dict["FirstOpenSlot"] == "No Appointments Available":
                continue #quits the loop if there are no appointments available for the location

            location_obj = self.make_loc_instance(obj,dict)
            if location_obj:
                locations.append(location_obj)

        return locations

    def get_dict(self,loc_obj,time_dict):
        """
        Search for the loc_obj's id inside of time_dict
        :param loc_obj:
            dict iterable from the list of locations (locationData)
        :param time_dict:
            hashed dict with location id as keys
        :return:
            corresponding value from the iterable's key in time_dict
        """
        try:
            loc_id = loc_obj["LocAppointments"][0]["LocationId"]
            return time_dict.get(loc_id)
        except KeyError:
            print("Invalid Location Data.")
            return None

    def make_loc_instance(self, loc_obj, time_obj ):
        return Location.create_location(loc_obj, time_obj)

class Filter:
    def __init__(self,days, retriever = None):
        """
        Takes the locations from LocationRetriever object and filters it in filter() based on the day range given, returning a new list of location objects which next appointments date match day range given from the current date sorted from most recent to least recent.
        :param days:
            Integer representing the range of days from now in which you wish to find an available appointment.
        """
        self.days = days
        self.retriever = retriever or LocationRetriever()
        if not self.retriever.locations:
            self.retriever.fetch_locations()

    def filter(self):
        """
        Filters self.retriever.locations appending those which appointments lie inside the day range to a new array. Returns the array sorted based on date.
        :return:
        """
        if not self.retriever.locations:
            return []
        filtered_dates = []
        current_date = datetime.now()
        range_date = current_date + timedelta(days=self.days)
        for obj in self.retriever.locations:
            if range_date >= obj.next_appointment_date >= current_date:
                filtered_dates.append(obj)
        return self.sort_locations(filtered_dates)


    def sort_locations(self,locations):
        """
        Sorts a list of Location objects by their next_appointment_date in ascending order.
        """
        return sorted(locations, key=lambda loc: loc.next_appointment_date)



