# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive

from .consts import *
from .saveunit import *
from .drive_IO import Drive_IO



class MainIndex:
    """An object representing the Drive folders for the UI""" 

    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.file_manager = Drive_IO(drive)
        self._first_run()
                    
    def _first_run(self) -> bool :
        """First run configurations. 
        Checks for (and creates, if necessary)
        the SaveGameVault folder, setting it as the working directory."""

        vault_folder = self.file_manager.get_folder(VAULT_FOLDER_NAME)
        if (not vault_folder):
            print(f"Creating folder '{VAULT_FOLDER_NAME} in ID '{self.file_manager.current_folder}'.")
            vault_folder = self.file_manager.create_folder(VAULT_FOLDER_NAME)
            if (not vault_folder):
                # TODO a more expressive error
                raise RuntimeError(f"Could not create '{VAULT_FOLDER_NAME}' folder.")
        
        moved = self.file_manager.go_down_a_level(VAULT_FOLDER_NAME)
        if (not moved):
            raise RuntimeError(f"Could not access '{VAULT_FOLDER_NAME}' folder.")
        
        # POPULATING THE GAMES INDEX:
        self.games = {}
        game_folders = self.file_manager.list_folders()
        for game in game_folders:
            self.games[game['title']] = self.file_manager._create_indexed_instance(game)
            
            
        

    
        
            


        
    
        
    
