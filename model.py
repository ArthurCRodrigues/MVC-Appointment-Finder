from datetime import datetime

class Location:
    def __init__(self, name,street,city,state,zip_code,phone,appointments,next_appointment_date):
        """
        Location Model that creates a location object with the basic info (Name, Address, Zip Code, Phone, Number of Appointments, and Next Appointment Date)
        :param loc_dict: Python dictionary that contains 'Name', 'Street1', 'City', 'State', 'Zip', 'PhoneNumber'
        :param appointments: Integer representing the number of available appointments
        :param next_appointment_date: Datetime object representing the next available appointment date
        """
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.appointments = appointments
        self.next_appointment_date = next_appointment_date

    @staticmethod
    def get_valid_field(data, key, default):
        """Returns a valid field value or a default if missing or empty."""
        value = data.get(key, "").strip()
        return value if value else default

    @staticmethod
    def get_valid_zip(zip_code):
        """Returns a cleaned zip code or 'N/A' if invalid."""
        return str(zip_code) if zip_code and str(zip_code).isdigit() else "N/A"

    @staticmethod
    def get_valid_phone(phone):
        """Returns a formatted phone number or 'N/A' if missing."""
        return phone if phone and phone.replace(" ", "").replace("-", "").isdigit() else "N/A"

    @staticmethod
    def get_valid_date(date):
        """Ensures next_appointment_date is valid or returns 'Unknown'."""
        return date if isinstance(date, datetime) else "Unknown"

    @classmethod
    def create_location(cls,loc_dict,date_obj):
        if not loc_dict or not date_obj:
            return None

        name = cls.get_valid_field(loc_dict, 'Name', "Unknown Location")
        street = cls.get_valid_field(loc_dict, 'Street1', "Unknown Street")
        city = cls.get_valid_field(loc_dict, 'City', "Unknown City")
        state = cls.get_valid_field(loc_dict, 'State', "Unknown State")
        zip_code = cls.get_valid_zip(loc_dict.get('Zip', "N/A"))
        phone = cls.get_valid_phone(loc_dict.get('PhoneNumber', "N/A"))

        appointment_str = date_obj.get("FirstOpenSlot")
        if not appointment_str:
            return None
        appointments = cls.get_appointment_number(appointment_str)
        next_appointment = cls.get_next_date(appointment_str)

        return cls(name,street,city,state,zip_code,phone,appointments,cls.get_valid_date(next_appointment))



    @staticmethod
    def get_appointment_number(appointment_str):
        try:
            appointments = int(appointment_str.split(" ")[0])  # number of appointments
            return appointments
        except ValueError:
            print(f"Warning: Could not parse appointment count in {appointment_str}")
            return None

    @staticmethod
    def get_next_date(appointment_str):
        try:
            str_split = appointment_str.split("Next Available: ")
            date_obj = datetime.strptime(str_split[1],
                                         "%m/%d/%Y %I:%M %p")  # next free appointment (parse into datetime obj)
            return date_obj
        except (IndexError,ValueError) as e:
            print(f"Error: {e}")
            return None


    def __str__(self):
        return (
            f"Location Name: {self.name}\n"
            f"Address: {self.street}, {self.city}, {self.state}, {self.zip_code}\n"
            f"Phone Number: {self.phone}\n"
            f"Appointments: {self.appointments}\n"
            f"Next Appointment Date: {self.next_appointment_date}"
        )
