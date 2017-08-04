#Created on 04/08/2017. All the background stuff is here.
from crunchyroll.apis.meta import MetaApi
api = MetaApi()

#The main code.

CRUsername = input("Crunchyroll Username: ") #Asks the user to enter their username.
CRPassword = input("Crunchyroll Password: ") #Asks the user to enter their password.
crunchyLoginOutput = api.login(username=CRUsername, password=CRPassword) # Logs into Crunchyroll

if crunchyLoginOutput == "True": #If the crunchyLoginOutput returns True, it'll print that is successful.
    print("Login Successful")
else:
    print("Login Failed")
