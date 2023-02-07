# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive, GoogleDriveFile
from pydrive2.files import FileNotUploadedError, FileNotDownloadableError

from .consts import *
from .saveunit import *
from .drive_IO import FileManager

class MainIndex:
    """An object representing the Drive folders for the UI""" 
     
    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.file_manager = FileManager(drive)
        self._first_run()
  
    def _first_run(self) -> bool :
        """First run configurations. 
        Checks for (and creates, if necessary)
        the SaveGameVault folder, setting it as the working directory."""

        vault_folder = self.file_manager.get_folder(vault_folder_name)
        if (not vault_folder):
            print(f"Creating folder '{vault_folder_name} in ID '{self.file_manager.curr_folder_id}'.")
            vault_folder = self.file_manager.create_folder(vault_folder_name)
            if (not vault_folder):
                # TODO more expressive error
                raise RuntimeError(f"Could not create '{vault_folder_name}' folder.")
        
        moved = self.file_manager.go_down_a_level(vault_folder_name)
        if (not moved):
            raise RuntimeError(f"Could not access '{vault_folder_name}' folder.")
        
        # POPULATING THE GAMES INDEX:
        self.games = {}
        game_folders = self.file_manager.list_folders()
        for game in game_folders:
            self.games[game['title']] = self.IndexedGame(game)
        "baba booey"
        
    
    class IndexedGame:
        def __init__(self, drive_folder : GoogleDriveFile):
            self.folder = drive_folder

        @property
        def name(self):
            return self.folder['title']
        @property
        def id(self):
            return self.folder['id']
        
            


        
    
        
    
