from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.funcs import *

def CreateTargetFolder(drive : GoogleDrive, target_folder : str):
    print("Target folder '{}' does not exist.".format(target_folder))
    print("Creating folder.")
    created = CreateFolder(drive, target_folder)
    if not created:
        print("Could not create folder.")
        print("Exiting.")
        exit()

    print("Folder created successfully.")

if __name__ == "__main__":

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # FLOW: 
    # - Check if the target folder exists. If not, create it.
    # - Check for the index file on target folder. If does not exist, create a default (blank) file.
    # - Display information from index file on screen

    target_folder = "Save Game Vault"
    target_exists = FolderExists(drive, target_folder)

    if not target_exists:
        CreateTargetFolder(drive, target_folder)
    else:
        print("Found '{}' folder. Starting the parse.".format(target_folder))
    
    PrintFolderList(drive)


