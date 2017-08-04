#Created on 04/08/2017. All the background stuff is here.
from crunchyroll.apis.meta import MetaApi
api = MetaApi()

#The main code.

<<<<<<< HEAD
print(crunchyLoginOutput)
if crunchyLoginOutput == "True":
=======
CRUsername = input("Crunchyroll Username: ") #Asks the user to enter their username.
CRPassword = input("Crunchyroll Password: ") #Asks the user to enter their password.
crunchyLoginOutput = api.login(username=CRUsername, password=CRPassword) # Logs into Crunchyroll

if crunchyLoginOutput == "True": #If the crunchyLoginOutput returns True, it'll print that is successful.
>>>>>>> 4a3ff4990caa0c9f23c3e5df87b595582a5a9960
    print("Login Successful")
else:
    print("Login Failed")
