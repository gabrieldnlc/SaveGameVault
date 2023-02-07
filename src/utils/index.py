# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive, GoogleDriveFile
from pydrive2.files import FileNotUploadedError, FileNotDownloadableError

from .consts import *
from .saveunit import *
from .drive_IO import FileManager

class MainIndex:
    """An object representing the Drive folders for the UI""" 
     
    # SUBCLASSES START
    class IndexedCloudFile:
        """An encapsulation of a GoogleDriveFile for readability and ease of use."""
        def __init__(self, drive_file : GoogleDriveFile):
            self.file = drive_file

        @property
        def title(self):
            return self.file['title']
        @property
        def id(self):
            return self.file['id']
        @property
        def mime(self):
            return self.file['mimeType']
        
        def __repr__(self):
            return f"{self.title} (id: {self.id})"

    class IndexedCloudFolder:
        """An encapsulation of a GoogleDriveFile (as a folder) for readability and ease of use."""

        def __init__(self, drive_folder : GoogleDriveFile):
            self.folder = drive_folder
            self.files = [] # to be filled by factory method.       

        @property
        def title(self):
            return self.folder['title']
        @property
        def id(self):
            return self.folder['id']
        @property
        def mime(self):
            return self.folder['mimeType']
        
        def __repr__(self):
            return f"{self.title}\ (id: {self.id})"
    # SUBCLASSES END


    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.file_manager = FileManager(drive)
        self._first_run()
    
    def _create_indexed_instance(self, drive_file : GoogleDriveFile) -> IndexedCloudFile | IndexedCloudFolder:
        mime = drive_file['mimeType']
        if (mime != MIME_FOLDER):
            return self.IndexedCloudFile(drive_file)
        else:
            folder = self.IndexedCloudFolder(drive_file)
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
            print(f"Creating folder '{VAULT_FOLDER_NAME} in ID '{self.file_manager.curr_folder_id}'.")
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
            
            
        

    
        
            


        
    
        
    
