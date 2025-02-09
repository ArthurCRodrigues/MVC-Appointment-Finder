import time
from locationRetriever import Filter
from plyer import notification


def continuous_search(days, check_interval=10):
    """
    Continuously search for available appointments and send a desktop notification when found.

    :param days: The day range for filtering appointments.
    :param check_interval: Time in seconds to wait between each check.
    """
    print(f"Starting continuous search for appointments within the next {days} days...")

    while True:
        try:
            filter_instance = Filter(days)
            available_locations = filter_instance.filter()

            if available_locations:
                print("\nAppointments found!\n")
                for location in available_locations:
                    print(location)
                    # Send a desktop notification for each location found
                    notification.notify(
                        title=f"🎉 Appointment Found at {location.name}!",
                        message=f"Next available: {location.next_appointment_date.strftime('%m/%d/%Y %I:%M %p')}",
                        timeout=10
                    )
                break  # Exit the loop after finding appointments

            else:
                print(f"No appointments found. Checking again in {check_interval} seconds...")

        except Exception as e:
            print(f"An error occurred: {e}. Retrying in {check_interval} seconds...")

        time.sleep(check_interval)


if __name__ == "__main__":
    continuous_search(days=2, check_interval=15)
