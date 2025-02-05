from bs4 import BeautifulSoup
import requests,re,json
from datetime import datetime,timedelta

from model import Location

class LocationRetriever:
    """
    This class will only contain one attribute (locations) that will be set automatically upon instantiation. The attribute itself is a list of location objects with available appointments (regardless of date).
    """
    def __init__(self):
        self.locations = self.__getLocations()

    def __getTags(self):
        """
        Creates the soup from the appointmentWizard website using requests library and filter all the script tags in the document.
        :return:
            bs4 resultSet with all script tags found
        """
        try:
            req = requests.get('https://telegov.njportal.com/njmvc/AppointmentWizard/12', timeout=10)
            req.raise_for_status()  # Raises an error for bad responses
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

        soup = BeautifulSoup(req.text, 'html.parser')
        return soup.find_all('script')

    def __findLocation(self):
        """
        Iterates through the result set from __getTags and uses regular expressions on the iterables in order to extract the locationData variable value (if existent).
        :return:
            IF FOUND: variable value as string
            IF NOT FOUND: None
        """
        try:
            script_tags = self.__getTags()
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
        except (re.error, ValueError) as e:
            print("Error: ",e)
            return None

    def __findTime(self):
        """
                Iterates through the result set from __getTags and uses regular expressions on the iterables in order to extract the timeData variable value (if existent).
                :return:
                    IF FOUND: variable value as string
                    IF NOT FOUND: None
                """
        try:
            script_tags = self.__getTags()
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
        except (re.error, ValueError) as e:
            print("Error: ",e)
            return None,None

    def __parseData(self):
        """
        gets both strings from __findLocation and __findTime and uses json library to map them into python dicts. Hashes time_json dict to make its access linear in the future
        :return:
        """
        try:
            locationData = self.__findLocation()
            timeData = self.__findTime()
            if not locationData or not timeData:
                raise ValueError("Couldn't find data.")
            location_json = json.loads(locationData)
            time_json = json.loads(timeData)
            time_dict = {}
            for obj in time_json:
                time_dict[obj["LocationId"]] = obj  # Fills a new dictionary with the location id as a key for that dict (linear access)
            # Basically hashed the dict
            return location_json,time_dict
        except json.decoder.JSONDecodeError as e:
            print("Error: ",e)
            return None,None

    def __getLocations(self):
        """
        filters those locations which have available appointments and pass them to Location model. Also extract the number of available appointments and parse the next appointment date (string) to a datetime object
        :return:
            list of Location objects with available appointments
        """
        location_json,time_dict = self.__parseData()
        if not location_json or not time_dict:
            raise ValueError("Couldn't find data.")

        locations = []

        for obj in location_json:
            dict = time_dict.get(obj["LocAppointments"][0]["LocationId"]) #obj["LocAppointments"][0]["LocationId"] is the way to access each iterable's (location) id
            if not dict:
                raise KeyError("ID doesn't exist in time_dict")

            if dict["FirstOpenSlot"] == "No Appointments Available":
                continue #quits the loop if there are no appointments available for the location

            appointment_str = dict["FirstOpenSlot"]
            try:
                appointments = int(appointment_str.split(" ")[0]) # number of appointments
            except ValueError:
                print(f"Warning: Could not parse appointment count in {appointment_str}")
                continue

            try:
                appointment_str = appointment_str.split("Next Available: ")
                date_obj = datetime.strptime(appointment_str[1], "%m/%d/%Y %I:%M %p")  # next free appointment (parse into datetime obj)
            except (IndexError,ValueError) as e:
                print(f"Error:{e},skipping...")
                continue

            location_obj = Location(obj, appointments, date_obj) #pass to Location model
            locations.append(location_obj)

        return locations

class Filter:
    def __init__(self,days):
        """
        Takes the locations from LocationRetriever object and filters it in filter() based on the day range given, returning a new list of location objects which next appointments date match day range given from the current date sorted from most recent to least recent.
        :param days:
            Integer representing the range of days from now in which you wish to find an available appointment.
        """
        self.days = days
        self.retriever = LocationRetriever()

    def filter(self):
        """
        Filters self.retriever.locations appending those which appointments lie inside the day range to a new array. Returns the array sorted based on date.
        :return:
        """
        filtered_dates = []
        current_date = datetime.now()
        range_date = current_date + timedelta(days=self.days)
        for obj in self.retriever.locations:
            if range_date >= obj.next_appointment_date >= current_date:
                filtered_dates.append(obj)
        return self.__sort_locations(filtered_dates)


    def __sort_locations(self,locations):
        """
        Sorts a list of Location objects by their next_appointment_date in ascending order.
        """
        return sorted(locations, key=lambda loc: loc.next_appointment_date)