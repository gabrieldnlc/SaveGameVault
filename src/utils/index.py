# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError, FileNotDownloadableError

from utils.helpers import *
from utils.consts import *
from utils.saveunit import *

class MainIndex:
    """An object representing the Drive folders for the UI""" 
     
    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.drive = drive
        self._update()

        
    def _populate_indexed_games(self, folder : GoogleDriveFile):
        self.games = {}
        folder_list = get_folder_list(self.drive, folder['id'])
        for game in folder_list:
            self.games[game['title']] = self.IndexedGame(self.drive, game)
            

    def _update(self, target_folder : GoogleDriveFile = None) -> bool :
        if (target_folder == None):
            target_folder = get_folder(self.drive, vault_folder)
            if (not target_folder):
                target_folder = create_folder(self.drive, vault_folder)
        self._populate_indexed_games(target_folder)
        

    class IndexedGame():
        """An object representing one of the Save Game folders. MainIndex holds a list of these."""

        @staticmethod
        def get_metadata(drive: GoogleDrive, parent_id: str) -> GoogleDriveFile:
            file = get_file_matches(drive, title_metadata, parent_id)
            if (not file):
                raise FileNotUploadedError("Metadata file does not exist.")
            if (len(file) > 1):
                raise FileNotDownloadableError("There is more than one metadata file.")
            return file[0]

        def __init__(self, drive: GoogleDrive, folder: GoogleDriveFile):
            if (folder['mimeType'] != mime_folder):
                raise Exception("Index can only be created based on a folder.") # TODO: better exception
            self.meta = {}
            self.title = folder['title']
            self.folders = get_folder_list(drive, folder['id'])
            
            # does it have the .metadata file?
            try:
                metadata = self.get_metadata(drive, folder['id'])
                print(f"Found metadata file for {self.title}.")
                self.meta = json_to_unit(metadata.GetContentString(remove_bom=True), SaveUnit)
            except FileNotUploadedError as err:
                print(f"Could not find metadata for {self.title}.")
                # TODO creating the .metadata file
            except FileNotDownloadableError as err:
                print(f"{self.title} has more than one metadata file. Needs human input.")
                # TODO the human input

        
            


        
    
        
    
