from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.funcs import *

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

print("Testing the existence of folders:")
print("Does the Testing folder exist?")
print (FolderExists(drive, "Testing"))
print("Does a bogus folder exist?")
print(FolderExists(drive, "bogus"))
print("What if we create the bogus folder?")
CreateFolder(drive, "bogus")
print(FolderExists(drive, "bogus"))
