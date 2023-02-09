from pydrive2.drive import GoogleDrive, GoogleDriveFile

from .consts import *
from .local_files import LocalFile, LocalFolder

# SUBCLASSES START
class CloudFile:
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

class CloudFolder:
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

class FileManager():
    def __init__(self, drive : GoogleDrive):
        self.drive = drive
        self._f_id = ""
        self.go_to_root()

    @property
    def current_folder(self):
        return self._f_id
    
    @current_folder.setter
    def current_folder(self, folder : str | CloudFolder | GoogleDriveFile ):
        if (folder == 'root'):
            self._f_id = 'root'
            print("Current folder: root.")
            return
        if (isinstance(folder, GoogleDriveFile)):
            folder = CloudFolder(folder)

        if (isinstance(folder, CloudFolder)):
            self._f_id = folder.id
            print (f"Current folder: {folder.title} (id: '{folder.id}').")
            return
        raise LookupError("Cannot change current folder: invalid string (try 'root' or passing a CloudFolder instance).")
    
    def go_to_root(self):
        self.current_folder = "root"

    def list_all(self) -> list:
        query = f"'{self.current_folder}' in parents and trashed=false"
        return self.drive.ListFile({'q': query }).GetList()
    
    def list_files(self) -> list:
        query = f"'{self.current_folder}' in parents and mimeType !='{MIME_FOLDER}' and trashed=false"
        return self.drive.ListFile({'q': query }).GetList()

    def list_folders(self) -> list:
        query = f"'{self.current_folder}' in parents and mimeType='{MIME_FOLDER}' and trashed=false"
        return self.drive.ListFile({'q': query }).GetList()
    
    def print_list_folders(self):
        for folder in self.list_folders():
            print('Title: %s, id: %s' % (folder['title'], folder['id']))

    def create_folder(self, folder_name : str) -> GoogleDriveFile | bool:
        """Creates (and returns) a 'folder_name' inside of current folder.
        Returns False if operation was not successful."""
        try:
            folder = self.drive.CreateFile({
            'title': folder_name, 
            "parents":  [{"id": self.current_folder}], 
            "mimeType": MIME_FOLDER
            })
            folder.Upload()
            return folder
        except: # TODO extend error catching
            return False
        
    def go_down_a_level(self, child_folder : str) -> bool:
        """Moves one directory down, into 'child_folder' of current working directory. 
        Returns True if success, False if folder does not exist."""
        new_dir = self.get_folder(child_folder)
        if (not new_dir):
            return False
        self.current_folder = new_dir
        return True

    def get_folder(self, folder_name : str) -> GoogleDriveFile | bool:
        """Searches for (and returns) 'folder_name' inside of current folder.
          Returns False if folder does not exist."""
        list = self.list_folders()
        for folder in list:
            if (folder['title'] == folder_name):
                return folder
        return False
    
    def search_files_in_folder(self, title : str) -> list | bool:
        """Returns a list of files inside current folder that match 'title'. 
        Returns False if no matches are found."""
        query = f"'{self.current_folder}' in parents and title='{title}' and trashed=false"
        file_list = self.drive.ListFile({'q': query }).GetList()
        if (len(file_list) == 0):
            return False
        return file_list
    
    def go_to_folder_and_list(self, folder_id : str, list_files = True, list_folders = True) -> list | bool:
        """Lists files and folders inside 'folder_id'.
        Uses boolean flags to switch query type: everything, files only or folders only.
        Returns a list or False if there were no hits."""
        query = f"'{folder_id}' in parents and trashed=false"
        if not (list_files and list_folders):
            if not list_files:
                query += f"and mimeType='{MIME_FOLDER}'"
            else:
                query += f"and mimeType!='{MIME_FOLDER}'"

        file_list = self.drive.ListFile({'q': query }).GetList()
        if (len(file_list) == 0):
            return False
        return file_list

    def upload_file(self, file : LocalFile) -> bool:
        """Uploads a file to the current working folder.
        Returns True on success."""
