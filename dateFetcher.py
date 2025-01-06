from bs4 import BeautifulSoup
from datetime import datetime
import requests
from datetime import date
def getDate(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    mydates = soup.find_all("label", {"class": "control-label date-time"})
    txt = mydates[1].text
    date_str = txt.split("for ")[1]
    date_str = date_str.split(" ")
    #date_object = datetime.strptime(date_str, "%B %d, %Y")
    months = {"January":1, "February":2, "March":3,"April":4, "May":5, "June":6, "July":7,"August":8,"September":9, "October":10,"November":11,"December":12}
    response = date(int(date_str[-2][:-1]),months[date_str[0]],int(date_str[1][:-1]))

    print(response)




getDate("https://telegov.njportal.com/njmvc/AppointmentWizard/12/124")