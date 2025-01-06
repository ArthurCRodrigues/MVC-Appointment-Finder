from bs4 import BeautifulSoup
import requests,re

def getIds(url):
    req = requests.get(url)
    if req.status_code == 200:
        soup = str(BeautifulSoup(req.text, 'html.parser'))
        ids = list({int(id) for id in re.findall(r'"LocationId":(\d+)', soup)})  # inline function gotten from GPT
        return ids

    else:
        raise Exception("Couldn't get ids")
