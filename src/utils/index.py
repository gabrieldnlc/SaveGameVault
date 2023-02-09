# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive, GoogleDriveFile

from .consts import *
from .saveunit import *
from .drive_IO import FileManager, CloudFile, CloudFolder



class MainIndex:
    """An object representing the Drive folders for the UI""" 

    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.file_manager = FileManager(drive)
        self._first_run()
        
        
    
    def _create_indexed_instance(self, drive_file : GoogleDriveFile) -> CloudFile | CloudFolder:
        mime = drive_file['mimeType']
        if (mime != MIME_FOLDER):
            return CloudFile(drive_file)
        else:
            folder = CloudFolder(drive_file)
            files = self.file_manager.go_to_folder_and_list(folder.id)
            if (files):
                for file in files:
                    folder.files.append(self._create_indexed_instance(file))
                # Making the folders come first:
                folder.files.sort(key=lambda e : e.mime, reverse=True)

            return folder
            
    def _first_run(self) -> bool :
        """First run configurations. 
        Checks for (and creates, if necessary)
        the SaveGameVault folder, setting it as the working directory."""

        vault_folder = self.file_manager.get_folder(VAULT_FOLDER_NAME)
        if (not vault_folder):
            print(f"Creating folder '{VAULT_FOLDER_NAME} in ID '{self.file_manager.current_folder}'.")
            vault_folder = self.file_manager.create_folder(VAULT_FOLDER_NAME)
            if (not vault_folder):
                # TODO more expressive error
                raise RuntimeError(f"Could not create '{VAULT_FOLDER_NAME}' folder.")
        
        moved = self.file_manager.go_down_a_level(VAULT_FOLDER_NAME)
        if (not moved):
            raise RuntimeError(f"Could not access '{VAULT_FOLDER_NAME}' folder.")
        
        # POPULATING THE GAMES INDEX:
        self.games = {}
        game_folders = self.file_manager.list_folders()
        for game in game_folders:
            self.games[game['title']] = self._create_indexed_instance(game)
            
            
        

    
        
            


        
    
        
    
