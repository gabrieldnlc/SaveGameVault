
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import ApiRequestError

from utils.index import MainIndex

if __name__ == "__main__":

    
    # FLOW: 
    # - Check if the target folder exists. If not, create it.
    # - Create an index object, loading information from each folder's metadata
    # - Display information from index file on screen

    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth) # TODO: check for AuthenticationError, Timeout
        index = MainIndex(drive)
    
    except ApiRequestError as err:
        print(f"API error: {err.GetField('message')}.")
    except Exception as err:
        print(f"Error: {''.join(err.args)}.")
    


