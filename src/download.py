#!/usr/bin/env python3
from __future__ import unicode_literals
import cfscrape
import youtube_dl


CRUsername = input("Crunchyroll Username: ") #Asks the user to enter their username.
CRPassword = input("Crunchyroll Password: ") #Asks the user to enter their password.

selectedEpisode = "http://www.crunchyroll.com/new-game/episode-1-it-actually-feels-like-i-started-my-job-715393"

#payload = {
#    'name': CRUsername,
#   'password': CRPassword
#}
#
#with cfscrape.create_scraper() as s:
#    p = s.get("https://m.crunchyroll.com/login")
#    p = s.post("https://m.crunchyroll.com/?a=formhandler", data=payload)
#    print(p.text)
#    
#    r = s.get("http://www.crunchyroll.com/home/queue")
#    print (r.text)

ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([selectedEpisode])
