#!/usr/bin/env python3
import cfscrape

CRUsername = input("Crunchyroll Username: ") #Asks the user to enter their username.
CRPassword = input("Crunchyroll Password: ") #Asks the user to enter their password.

payload = {
    'name': CRUsername,
    'password': CRPassword
}

with cfscrape.create_scraper() as s:
    p = s.get("https://m.crunchyroll.com/login")
    p = s.post("https://m.crunchyroll.com/?a=formhandler", data=payload)
    print(p.text)
    
    #r = s.get("http://www.crunchyroll.com/home/queue")
    #print (r.text)
