from crunchyroll.apis.meta import MetaApi
api = MetaApi()

CRUsername = input("Crunchyroll Username: ")
CRPassword = input("Crunchyroll Password: ")
crunchyLoginOutput = api.login(username=CRUsername, password=CRPassword)

if crunchyLoginOutput == "True":
    print("Login Successful")
else:
    print("Login Failed")
