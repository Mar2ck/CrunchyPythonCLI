#!/usr/bin/env python3
#Created on 04/08/2017. All the background stuff is here.
from __future__ import unicode_literals
from crunchyroll.apis.meta import MetaApi
import cfscrape
import youtube_dl
import sys

commandLineArguments = sys.argv
api = MetaApi()
simulateBoolean = False #Command line argument for debuging youtube-dl

if "--simulate" in commandLineArguments:
    simulateBoolean = True

doLoginOrNot = input("Do you want to login: ")
if doLoginOrNot == "yes":
    #The main code.
    CRUsername = input("Crunchyroll Username: ") #Asks the user to enter their username.
    CRPassword = input("Crunchyroll Password: ") #Asks the user to enter their password.

    crunchyLoginOutput = api.login(username=CRUsername, password=CRPassword) # Logs into Crunchyroll

userSearchInput = input("Search for a show: ") #Asks the user to input what show they want to look for.
userSearchOutput = api.search_anime_series(userSearchInput)

print("")
for names in range(len(userSearchOutput)):
    print("Show number {0}: ".format(names + 1) + userSearchOutput[names].name) #Prints out the show with a show number.
try:
    userResultInput = int(input("Please enter the show number of the show you would like to watch: ")) #Asks the user to input the show number.
except ValueError:
    print("This is not a valid show.")
    quit()

confirmation = input("Are you sure that {0} is the anime you want to watch?: ".format(userSearchOutput[userResultInput - 1].name)).lower() #Asks the user if the show that they want to watch is correct, returns it in a lower case format.

if confirmation == "yes": #If yes it will return the episodes.
    print("These are the list of episodes available to watch. \n")
    userEpisodes = api.list_media(userSearchOutput[userResultInput - 1]) #Lists the media of the series they are trying to watch.
    for x in userEpisodes:
        print("{0}| {1}".format(x.episode_number, x.name)) #Prints the available list of episodes.
    episodeNumberInput = input("What episode number do you want to watch?: ")
    episodeNameInput = input("If there are two episodes with the same number that you are trying to watch, please input their name: ")

    def returnEpisodeURL(episodeNumber, episodeName):
        if episodeName == "":
            ep = [e for e in userEpisodes if e.episode_number == episodeNumber][0] #Simple list comprehension, returns the actual episode the user is trying to view.
            return ep.url
        else:
            ep = [e for e in userEpisodes if e.episode_number == episodeNumber and e.name == episodeName][0] #Simple list comprehension, returns the actual episode the user is trying to view.
            return ep.url

    theURLForTheStream = returnEpisodeURL(episodeNumberInput, episodeNameInput)
    ydl_opts = {
        "simulate" : simulateBoolean,
        "subtitlesformat" : "ass",
        "subtitleslangs" : ['enUS'],
        "writesubtitles" : True,
        "forcetitle" : True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([theURLForTheStream])

else: #Else it will print bye and quit.
    print("Bye bye")
    quit()
