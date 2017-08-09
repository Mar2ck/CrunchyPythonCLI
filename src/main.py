#!/usr/bin/env python3
#Created on 04/08/2017. Version 0.0.2
from __future__ import unicode_literals
from crunchyroll.apis.meta import MetaApi
from crunchyroll.apis.meta import ScraperApi
import requests
import youtube_dl
import sys
import getpass
import platform
import logging

#TODO List
'''
- Let user select subtitle language
- Force --search, default to --help not search
- Let user pick more then one episode (Done 8/8/17)
- Use ffmpeg to combine mp4 and ass from download into mkv
#ffmpeg -i $SHOWFILENAME.mp4 -i $SHOWFILENAME.enUS.ass -map 0 -map 1 -c copy -metadata:s:s:0 language=eng -disposition:s:0 default $SHOWFILENAME.mkv
- Login to crunchyroll via website so login cookie can be used to get premium content (Simulcasts, 1080p, Premium only shows)
- Let users download shows from their queue
- Finish help section (Done 8/8/17)
'''

#User's OS ("Windows" or "Linux")
userOperatingSystem = platform.system()

#Starting variables
commandLineArguments = sys.argv
crunchyrollMetaAPI = MetaApi()
crunchyrollScraperAPI = ScraperApi(connector=requests)
simulateDownloadBoolean = False
queueArgument = False

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
        print('''CrunchyPythonCLI - Usage: crunchypythoncli --[argument]

--- Command Line Arguments ---

When running the program, certain command line arguments can be passed to obtain different features. In order to use a command line argument, here is how you would do it in a terminal:

>>>crunchypythonapi --(commandLineArgument)

If you want to do multiple command line arguments, you would do them as follows:

>>>crunchypythonapi --(firstArgument) --(secondArgument)

The avaliable command line arguments are:

--simulate
Program will skip the downloading the file. Used for debugging and testing

--auth
Will allow user to login with their Crunchyroll accounts to use their queue and gain premium privledges (1080p, Simulcasts, etc.)

--queue
** Requires --auth be used aswell **
Displays the users Crunchyroll queue (Work in progress)


--- Multi-Episode Selection Guide ---

Input for this is identical to youtube-dl's --playlist-items selection. The playlist number are denoted by [] in episode selection screen.

Relevent exerpt from youtube-dl's README.md:
"Specify indices of the videos in the playlist separated by commas like: "1,2,5,8" if you want to download videos indexed 1, 2, 5, 8 in the playlist.
You can specify range: "1-3,7,10-13", it will download the videos at index 1, 2, 3, 7, 10, 11, 12 and 13."
''')
        quit()
    else:
        print("Unrecognised argument \"" + argumentItem + "\"")
        print("Use \"--help\" to see all availiable arguemnts.")
        quit()


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
        episodeNumberInput = input("Input the id number of the episode(s) you want to watch (Look at --help's \"Multi-Episode Selection Guide\" for help): ")

        ydl_opts = {
            "simulate" : simulateDownloadBoolean,
            "subtitlesformat" : "ass",
            "listsubtitles" : True,
            "writesubtitles" : True,
            "call_home" : False,
            "outtmpl" : "%(season)s - Episode %(episode_number)s: %(episode)s.%(ext)s",
        }

        #ydlCheckSubsOperators = {
        #    "skip_download" : True,
        #    "listsubtitles": True
        #}

        #Simple list comprehension, returns the actual episode the user is trying to view.
        if episodeNumberInput == "":
            print("Downloading all episodes")
        else:
            if "-" in episodeNumberInput or "," in episodeNumberInput:
                print("Downloading multiple episodes")
            if "," not in episodeNumberInput and "-" not in episodeNumberInput:
                #Dict for selected episode
                selectedEpisode = userEpisodes[len(userEpisodes) - int(episodeNumberInput)]
                print("Downloading episode " + selectedEpisode.episode_number)
                #True if premium account is needed to watch
                episodePremiumOnly = not(bool(selectedEpisode.free_available))
                #Unique episode identifier
                episodeMediaID = selectedEpisode.media_id
                #Website url for episode
                episodeURL = selectedEpisode.url
                #Adds "playlist_items" to youtube-dl options (ydl_opts)

            ydl_opts["playlist_items"] = episodeNumberInput
            #ydlCheckSubsOperators["playlist_items"] = episodeNumberInput

        theURLForTheStream = userSearchOutput[userResultInput - 1].url
        #print(crunchyrollScraperAPI.get_media_formats(episodeMediaID)) #Returns the availiable qualities for selected episode

        #with youtube_dl.YoutubeDL(ydlCheckSubsOperators) as ydl:
        #    testOutput = ydl.list_subtitles([theURLForTheStream])
        #    print(testOutput)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([theURLForTheStream])
