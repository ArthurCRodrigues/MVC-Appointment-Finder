import idRetriever,dateFetcher
from datetime import datetime
if __name__ == "__main__":
    ids = idRetriever.getIds("https://telegov.njportal.com/njmvc/AppointmentWizard/12")
    for id in ids:
        dateFetcher.getDate(f"https://telegov.njportal.com/njmvc/AppointmentWizard/12/{id}")