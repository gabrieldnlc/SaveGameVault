
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.helpers import *
from utils.index import MainIndex
from utils.ui import UI_List

if __name__ == "__main__":

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth) # TODO: check for AuthenticationError

    # FLOW: 
    # - Check if the target folder exists. If not, create it.
    # - Create an index object, loading information from each folder's metadata
    # - Display information from index file on screen

    try:
        index = MainIndex(drive)
        list = UI_List(index.games.keys())
    except Exception as err:
        print(f"Error: {''.join(err.args)}")
    


