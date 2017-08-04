#!/usr/bin/env python3
from requests import session
import cfscrape

CRUsername = input("Crunchyroll Username: ") #Asks the user to enter their username.
CRPassword = input("Crunchyroll Password: ") #Asks the user to enter their password.

payload = {
    'action': 'login',
    'username': CRUsername,
    'password': CRPassword
}

with cfscrape.create_scraper() as s:
    p = s.get("https://www.crunchyroll.com/login")
    p = s.post("https://www.crunchyroll.com/login", data=payload)
    print(p.content)

#with session() as c:
#    c.post('https://www.crunchyroll.com/login', data=payload)
#    response = c.get('http://www.crunchyroll.com/home/queue')
#    print(response.headers)
#    print(response.text)
