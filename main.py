from bs4 import BeautifulSoup
import requests,re

if __name__ == "__main__":
    req = requests.get('https://telegov.njportal.com/njmvc/AppointmentWizard/12')
    if req.status_code == 200:
        soup = str(BeautifulSoup(req.text, 'html.parser'))
        ids = list({int(id) for id in re.findall(r'"LocationId":(\d+)', soup)}) #inline function gotten from GPT
        print(ids)

    else:
        print("Failed to retrieve info")
