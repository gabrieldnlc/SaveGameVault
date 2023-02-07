from pydrive2.drive import GoogleDrive, GoogleDriveFile

from .consts import *

class FileManager():
    def __init__(self, drive : GoogleDrive):
        self.drive = drive
        self.curr_folder_id = 'root'

    def list_all(self) -> list:
        query = f"'{self.curr_folder_id}' in parents and trashed=false"
        return self.drive.ListFile({'q': query }).GetList()
    
    def list_files(self) -> list:
        query = f"'{self.curr_folder_id}' in parents and mimeType !='{mime_folder}' and trashed=false"
        return self.drive.ListFile({'q': query }).GetList()

    def list_folders(self) -> list:
        query = f"'{self.curr_folder_id}' in parents and mimeType='{mime_folder}' and trashed=false"
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
            "parents":  [{"id": self.curr_folder_id}], 
            "mimeType": mime_folder
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
        self.curr_folder_id = new_dir['id']
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
        query = f"'{self.curr_folder_id}' in parents and title='{title}' and trashed=false"
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
                query += f"and mimeType='{mime_folder}'"
            else:
                query += f"and mimeType!='{mime_folder}'"

        file_list = self.drive.ListFile({'q': query }).GetList()
        if (len(file_list) == 0):
            return False
        return file_list
