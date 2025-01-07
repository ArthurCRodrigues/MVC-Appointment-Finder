from bs4 import BeautifulSoup
import requests
import json

req = requests.get("https://telegov.njportal.com/njmvc/AppointmentWizard/12")
soup = BeautifulSoup(req.text, 'html.parser')
print(soup)