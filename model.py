'''

This is the model that keeps all the location info as objects
It will store:
 - Name
 - Street 1
 - City
 - State
 - Zip code
 - Phone Number
 - Appointments available
 - Next Appointment Date

'''
from datetime import datetime
class Location:
    def __init__(self,loc_dict,appointments,next_appointment_date):
        self.name = loc_dict['Name']
        self.street = loc_dict['Street1']
        self.city = loc_dict['City']
        self.state = loc_dict['State']
        self.zip_code = loc_dict['Zip']
        self.phone = loc_dict['PhoneNumber']
        self.appointments = appointments
        self.next_appointment_date = next_appointment_date

    def __str__(self):
        return (
            f"Location Name: {self.name}\n"
            f"Address: {self.street}, {self.city}, {self.state}, {self.zip_code}\n"
            f"Phone Number: {self.phone}\n"
            f"Appointments: {self.appointments}\n"
            f"Next Appointment Date: {self.next_appointment_date}"
        )