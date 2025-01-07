from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime,timedelta
from model import Location
from bs4 import BeautifulSoup
req = requests.get('https://telegov.njportal.com/njmvc/AppointmentWizard/12')
soup = BeautifulSoup(req.text, 'html.parser')
# Find all script tags
script_tags = soup.find_all('script')
locationData = ""
timeData = ""
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
        break
location_json = json.loads(locationData)
time_json = json.loads(timeData)
time_dict = {}
for obj in time_json:
    time_dict[obj["LocationId"]] = obj #Fills a new dictionary with the location id as a key for that dict (linear access)
#Basically hashed the dict
foos = []
for obj in location_json:
    dict = time_dict[obj["LocAppointments"][0]["LocationId"]]
    if dict["FirstOpenSlot"] == "No Appointments Available":
        continue
    ap_str = dict["FirstOpenSlot"]
    appointments = int(ap_str.split(" ")[0]) #appointments
    #print(ap_str)
    ap_str = ap_str.split("Next Available: ")
    date_obj = datetime.strptime(ap_str[1],"%m/%d/%Y %I:%M %p") #next free appointment
    location_obj = Location(obj, appointments, date_obj)
    foos.append(location_obj)
current_date = datetime.now()
range = 2
range_date = current_date + timedelta(days=2)
filtered_dates = []
for obj in foos:
    if range_date >= obj.next_appointment_date >= current_date:
        filtered_dates.append(obj)
for obj in filtered_dates:
    print(obj.name,"->",obj.next_appointment_date)



