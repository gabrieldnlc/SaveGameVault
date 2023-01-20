# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError, ApiRequestError

from .funcs import *
from .consts import *

class MainIndex: 
    # An object representing the Drive folders for the UI
    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.drive = drive
        self.Update()

        
    def PopulateIndexedGames(self, folder : GoogleDriveFile):
        self.games = {}
        folder_list = GetFolderList(self.drive, folder['id'])
        for game in folder_list:
            self.games[game['title']] = self.IndexedGame(self.drive, game)
            

    def Update(self, target_folder : GoogleDriveFile = None) -> bool :
        if (target_folder == None):
            target_folder = GetFolder(self.drive, vault_folder)
            if (not target_folder):
                target_folder = CreateFolder(self.drive, vault_folder)
        self.PopulateIndexedGames(target_folder)
        
        

    class IndexedGame():
        """An object representing one of the Save Game folders. MainIndex holds a list of these."""

        @staticmethod
        def GetMetadata(drive: GoogleDrive, parent_id: str) -> GoogleDriveFile:
            file = GetFileMatches(drive, title_metadata, parent_id)
            if (not file):
                raise FileNotUploadedError("Metadata file does not exist.")
            if (len(file) > 1):
                raise ApiRequestError("There is more than one metadata file.")
            return file

        def __init__(self, drive: GoogleDrive, folder: GoogleDriveFile):
            if (folder['mimeType'] != mime_folder):
                raise Exception("Cannot create an Index based on a single file.") # TODO: better exception
            self.meta = {}
            self.title = folder['title']
            self.folders = GetFolderList(drive, folder['id'])
            
            # does it have the .metadata file?
            try:
                metadata = self.GetMetadata(drive, folder['id'])
                print(f"Found metadata file for {folder['title']}")
            except Exception as err: # TODO: better exception handling
                print(f"Error: {''.join(err.args)}")

        
            


        
    
        
    
