#!/usr/bin/env python3
#Created on 04/08/2017. All the background stuff is here.
from __future__ import unicode_literals
from crunchyroll.apis.meta import MetaApi
import youtube_dl
import sys

#Starting variables
commandLineArguments = sys.argv
api = MetaApi()
simulateDownloadBoolean = False

#Loop variables
crunchyrollLoginAttempt = False
showResultsSelectionCorrect = False
doLoginOrNot = False

#Command line argument for debugging
if "--simulate" in commandLineArguments:
    simulateDownloadBoolean = True
if "--auth" in commandLineArguments:
    doLoginOrNot = True
if "--help" in commandLineArguments:
    #Todo: Write out all availiable command line arguments
    #print("Test help")
    quit()

#User Authentication
if doLoginOrNot == True:
    while crunchyrollLoginAttempt == False: #Asks user for Crunchyroll credentials and passes these to api so user can be authenticated
        CRUsername = input("Crunchyroll Username: ")
        CRPassword = input("Crunchyroll Password: ")
        try:
            crunchyLoginOutput = api.login(username=CRUsername, password=CRPassword)
        except:
            print("Login Error\n\nTry again to login")
        else:
            print("Login Success")
            crunchyrollLoginAttempt = True
else:
    print("User not authorized. To gain premium user benefits launch with command line \"--auth\"\n")

#Search for a show.
userSearchInput = input("Search for a show: ")
userSearchOutput = api.search_anime_series(userSearchInput)

print("\n")

while showResultsSelectionCorrect == False:
    if len(userSearchOutput) == 0:
        print("There was no show(s) with your search.")
    for names in range(len(userSearchOutput)):
        print("Show number {0}: ".format(names + 1) + userSearchOutput[names].name) #Prints out the show with a show number.
    try:
        userResultInput = int(input("Please enter the show number of the show you would like to watch: ")) #Asks the user to input the show number.
    except:
        print("Number entered is not valid, try again")
    else:
        showResultsSelectionCorrect = True

confirmation = input("Are you sure that {0} is the anime you want to watch?: ".format(userSearchOutput[userResultInput - 1].name)).lower() #Asks the user if the show that they want to watch is correct, returns it in a lower case format.

if confirmation == "yes": #If yes it will return the episodes.
    print("These are the list of episodes available to watch. \n")
    userEpisodes = api.list_media(userSearchOutput[userResultInput - 1]) #Lists the media of the series they are trying to watch.
    for x in userEpisodes:
        print("{0}| {1}".format(x.episode_number, x.name)) #Prints the available list of episodes.
    episodeNumberInput = input("What episode number do you want to watch?: ")
    episodeNameInput = input("If there are two episodes with the same number that you are trying to watch, please input their name: ")

    if episodeName == "":
        ep = [e for e in userEpisodes if e.episode_number == episodeNumber][0] #Simple list comprehension, returns the actual episode the user is trying to view.
        episodeURL = ep.url
    else:
        ep = [e for e in userEpisodes if e.episode_number == episodeNumber and e.name == episodeName][0] #Simple list comprehension, returns the actual episode the user is trying to view.
        episodeURL = ep.url

    theURLForTheStream = episodeURL
    ydl_opts = {
        "simulate" : simulateDownloadBoolean,
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
