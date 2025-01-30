from bs4 import BeautifulSoup
import requests,re,json
from datetime import datetime,timedelta

from model import Location

class LocationRetriever:
    def __init__(self):
        self.locations = self.__getLocations()

    def __getTags(self):
        try:
            req = requests.get('https://telegov.njportal.com/njmvc/AppointmentWizard/12')
            soup = BeautifulSoup(req.text, 'html.parser')
            # Find all script tags
            script_tags = soup.find_all('script')
            return script_tags
        except requests.exceptions.RequestException as e:
            print("Error: ",e)
            return []

    def __findData(self):
        try:
            script_tags = self.__getTags()
            if script_tags == []:
                return None,None
            # Regular expressions to extract locationData and timeData
            location_pattern = r'var locationData\s*=\s*(\[\{.*?\}\]);'
            time_pattern = r'var timeData = (\[.*?\])'
            # Print the script tags
            for script_tag in script_tags:
                # Extract locationData
                location_match = re.search(location_pattern, str(script_tag), re.DOTALL)
                locationData = location_match.group(1) if location_match else None

                # Extract timeData
                time_match = re.search(time_pattern, str(script_tag), re.DOTALL)
                timeData = time_match.group(1) if time_match else None
                if locationData and timeData:
                    return locationData,timeData
            raise ValueError("Couldn't find data.")
        except (re.error, ValueError) as e:
            print("Error: ",e)
            return None,None

    def __parseData(self):
        try:
            locationData,timeData = self.__findData()
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
        location_json,time_dict = self.__parseData()
        locations = []
        for obj in location_json:
            dict = time_dict[obj["LocAppointments"][0]["LocationId"]]
            if dict["FirstOpenSlot"] == "No Appointments Available":
                continue
            ap_str = dict["FirstOpenSlot"]
            appointments = int(ap_str.split(" ")[0])  # appointments
            # print(ap_str)
            ap_str = ap_str.split("Next Available: ")
            date_obj = datetime.strptime(ap_str[1], "%m/%d/%Y %I:%M %p")  # next free appointment
            location_obj = Location(obj, appointments, date_obj)
            locations.append(location_obj)
        return locations

class Filter:
    def __init__(self,days):
        self.days = days
        self.retriever = LocationRetriever()

    def filter(self):
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