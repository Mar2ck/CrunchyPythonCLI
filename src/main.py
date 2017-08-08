#!/usr/bin/env python3
#Created on 04/08/2017. All the background stuff is here.
from __future__ import unicode_literals
from crunchyroll.apis.meta import MetaApi
from crunchyroll.apis.meta import ScraperApi
import requests
import youtube_dl
import sys
import getpass
import platform

#User's OS ("Windows" or "Linux")
userOperatingSystem = platform.system()

#Convert mp4 and ass to mkv with ffmpeg
#ffmpeg -i video.mp4 -i subtitle.enUS.ass -map 0 -map 1 -c copy -metadata:s:s:0 language=eng -disposition:s:0 default output.mkv

#Starting variables
commandLineArguments = sys.argv
crunchyrollMetaAPI = MetaApi()
crunchyrollScraperAPI = ScraperApi(connector=requests)
simulateDownloadBoolean = False
queueArgument = False
episodeNumberInput = ""

#Loop variables
crunchyrollLoginAttempt = False
showSearchSuccess = False
showResultsSelectionCorrect = False
doLoginOrNot = False

#Command line arguments
for argumentItem in commandLineArguments[1:]:
    if argumentItem == "--simulate":
        simulateDownloadBoolean = True
    elif argumentItem == "--auth":
        doLoginOrNot = True
    elif argumentItem == "--queue":
    	queueArgument = True
    	#list_queue
    elif argumentItem == "--help":
        #Todo: Write out all availiable command line arguments
        #print("Test help")
        quit()
    else:
        print("Unrecognised argument " + argumentItem + "\n")

#User Authentication
if doLoginOrNot == True:
    while crunchyrollLoginAttempt == False: #Asks user for Crunchyroll credentials and passes these to api so user can be authenticated
        CRUsername = input("Crunchyroll Username: ")
        CRPassword = getpass.getpass("Crunchyroll Password: ")
        try:
            crunchyrollLoginOutput = crunchyrollMetaAPI.login(username=CRUsername, password=CRPassword)
            print(crunchyrollLoginOutput)
        except:
            print("Login Error\n\nTry again to login")
        else:
            print("Login Success")
            crunchyrollLoginAttempt = True
else:
    print("User not authorized. To gain premium user benefits launch with command line \"--auth\"\n")

if queueArgument == True:
    if crunchyrollLoginAttempt == True:
        userQueue = crunchyrollMetaAPI.list_queue()
        print("\nQueue Items:")
        userQueueItemNumber = 1
        for userQueueItem in userQueue:
            print("{0}: {1}".format(userQueueItemNumber, userQueueItem.name))
            userQueueItemNumber += 1
    else:
        print("Queue feature only works when logged in. Use \"--auth\" to login")
        quit()
else:
    #Search for a show
    while showSearchSuccess == False:
        userSearchInput = input("Search for a show: ")
        userSearchOutput = crunchyrollMetaAPI.search_anime_series(userSearchInput)
        if len(userSearchOutput) == 0:
            print("There was no shows with your search.\n\nTry again to search")
        else:
            showSearchSuccess = True

    while showResultsSelectionCorrect == False:
        print("\nSearch Results:")
        for names in range(len(userSearchOutput)):
            print("[{0}]: ".format(names + 1) + userSearchOutput[names].name) #Prints out the show with a show number.
        showResultsSelectionNumber = input("Please enter the show number of the show you would like to watch: ")
        try:
            userResultInput = int(showResultsSelectionNumber) #Asks the user to input the show number.
        except:
            print("Number entered or their is an error, please try again.")
        else:
            showResultsSelectionCorrect = True

    #Asks the user if the show that they want to watch is correct, returns it in a lower case format.
    confirmation = input("Are you sure that {0} is the anime you want to watch?: ".format(userSearchOutput[userResultInput - 1].name)).lower()

    if confirmation == "yes": #If yes it will return the episodes.
        print("These are the list of episodes available to watch. \n")
        userEpisodes = crunchyrollMetaAPI.list_media(userSearchOutput[userResultInput - 1]) #Lists the media of the series they are trying to watch.
        #Number of episodes show has availiable
        userEpisodeNumber = len(userEpisodes)
        for x in userEpisodes:
            print("[{0}] Episode {1}: {2}".format(userEpisodeNumber, x.episode_number, x.name)) #Prints the available list of episodes.
            userEpisodeNumber -= 1
        episodeNumberInput = input("Input the id number of the episode you want to watch (Type nothing to download everything): ")

        ydl_opts = {
            "simulate" : simulateDownloadBoolean,
            "subtitlesformat" : "ass",
            "subtitleslangs" : ['enUS'],
            "writesubtitles" : True,
            "call_home" : False,
            "outtmpl" : "%(season)s - Episode %(episode_number)s: %(episode)s.%(ext)s",
        }

        #Simple list comprehension, returns the actual episode the user is trying to view.
        if episodeNumberInput != "":
            ep = [e for e in userEpisodes if e.media_id == episodeNumberInput][0]
            episodePremiumOnly = not(bool(ep.free_available)) #True if premium account is needed to watch
            episodeMediaID = ep.media_id #Unique episode identifier
            episodeURL = ep.url
            ydl_opts["playlist_items"] = episodeNumberInput
        else:
            episodeNumberInput = False

        theURLForTheStream = userSearchOutput[userResultInput - 1].url
        #print(crunchyrollScraperAPI.get_media_formats(episodeMediaID)) #Returns the availiable qualities for selected episode

        print(ydl_opts)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([theURLForTheStream])
