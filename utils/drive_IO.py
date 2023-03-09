from datetime import datetime, timezone, timedelta
from pathlib import Path

from pydrive2.drive import GoogleDrive, GoogleDriveFile
from pydrive2.files import ApiRequestError

from .consts import *
from .local_files import LocalFile, LocalFolder



class Drive_IO():
    """Class that deals with all Google Drive related interactions.\n
    Enforces a "no two files with same filename" rule, instead of the ID based system from Google."""
    def __init__(self, drive : GoogleDrive):
        self.drive = drive
        self._f_id = ""
        self.go_to_root()

    # SUBCLASSES START # TODO use ABC to create an abstract class and reuse code here
    class CloudFile:
        """An encapsulation of a GoogleDriveFile for readability and ease of use."""
        def __init__(self, drive_file : GoogleDriveFile):
            self._file = drive_file

        @property
        def title(self):
            return self._file['title']
        @property
        def id(self):
            return self._file['id']
        @property
        def mime(self):
            return self._file['mimeType']
        @property
        def modified_on(self) -> str:
            """Last modified time, in ISO format."""
            return self._file['modifiedDate']
        @property
        def modified_on_iso(self) -> str:
            """Last modified time, in ISO format.
            An alias of modified_on()."""
            return self.modified_on
        @property
        def modified_on_datetime(self) -> datetime:
            """Last modified time, wrapped in a datetime instance."""
            return datetime.fromisoformat(self.modified_on_iso)
            
        def __repr__(self):
            return f"{self.title} (id: {self.id})"

    class CloudFolder:
        """An encapsulation of a GoogleDriveFile (as a folder) for readability and ease of use."""

        def __init__(self, IO: 'Drive_IO', drive_folder : GoogleDriveFile):
            self._folder = drive_folder
            self.files = [] # to be filled by factory method.   
            files = IO.go_to_folder_and_list(drive_folder['id'])
            if (files):
                for file in files:
                    self.files.append(IO._create_indexed_instance(file))
                # Making the folders come first:
                self.files.sort(key=lambda e : e.mime, reverse=True)
                

        @property
        def title(self):
            return self._folder['title']
        @property
        def id(self):
            return self._folder['id']
        @property
        def mime(self):
            return self._folder['mimeType']
            
        def __repr__(self):
            return f"{self.title}\ (id: {self.id})"
    # SUBCLASSES END

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
            folder = self.CloudFolder(self, folder)

        if (isinstance(folder, self.CloudFolder)):
            self._f_id = folder.id
            print (f"Current folder: {folder.title} (id: '{folder.id}').")
            return
        raise LookupError("Cannot change current folder: invalid string (try 'root' or passing a CloudFolder instance).")
    
    def drive_file_from_id(self, id : str) -> GoogleDriveFile | bool:
        """Returns an instance of GoogleDriveFile pointing to the ID.\n
        Returns False if file or folder does not exist."""
        try:
            return self.drive.CreateFile({'id': id})
        except ApiRequestError:
            return False
    
    def _create_indexed_instance(self, drive_file : GoogleDriveFile) -> CloudFile | CloudFolder:
        mime = drive_file['mimeType']

        if (mime != MIME_FOLDER):
            return self.CloudFile(drive_file)
        
        return self.CloudFolder(self, drive_file)

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

    def create_folder(self, folder_name : str, enter_after = False) -> GoogleDriveFile | bool:
        """Creates (and returns) a 'folder_name' folder inside of current working directory.\n
        If enter_after == True, working directory will be changed to the newly created folder."""

        if (self.get_folder(folder_name)):
            raise FileExistsError(f"There is already a folder named '{folder_name}'.")

        folder = self.drive.CreateFile({
        'title': folder_name, 
        "parents":  [{"id": self.current_folder}], 
        "mimeType": MIME_FOLDER
        })
        folder.Upload()
        print(f"Created '{folder_name}' folder in '{self.current_folder}'.")

        if (enter_after):
            self.go_down_a_level(folder_name)

        return folder
        
    def go_down_a_level(self, child_folder : str) -> bool:
        """Moves one directory down, into 'child_folder' of current working directory.\n
        Returns True if success, False if folder does not exist."""
        new_dir = self.get_folder(child_folder)
        if (not new_dir):
            return False
        self.current_folder = new_dir
        return True

    def get_folder(self, folder_name : str) -> GoogleDriveFile | bool:
        """Searches for (and returns) 'folder_name' inside of current folder.\n
          Returns a GoogleDriveFile instance or False if folder does not exist."""
        list = self.list_folders()
        for folder in list:
            if (folder['title'] == folder_name):
                return folder
        return False
    
    def search_in_folder(self, title : str) -> list[GoogleDriveFile] | bool:
        """Returns a list of files inside current folder that match 'title'.\n
        Returns an empty list if no files are found."""
        query = f"'{self.current_folder}' in parents and title='{title}' and trashed=false"
        file_list = self.drive.ListFile({'q': query }).GetList()
        return file_list
    
    def go_to_folder_and_list(self, folder_id : str, list_files = True, list_folders = True) -> list | bool:
        """Lists files and folders inside 'folder_id'.\n
        Uses boolean flags to switch query type: everything, files only or folders only.\n
        Returns a list or False, if there were no hits."""
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
    
    def create_file(self, title : str, content : str, overwrite_ok = False) -> CloudFile:
        """Creates a file on the current working folder with content specified.\n
        If overwrite_ok == False, will raise if there is already a file with the specified name."""

        exists = self.search_in_folder(title)
        if (exists):
            if (not overwrite_ok):
                raise FileExistsError(f"A file named '{title}' already exists in the working folder.")
            for f in exists:
                self.delete_file(f)

        now_isoformat = datetime.now(timezone.utc).isoformat()
        
        metadata = {
        "title" : title,
        "parents" : [{"id" : self.current_folder}],
        "createdDate" : now_isoformat,
        "modifiedDate" : now_isoformat,
        }
        file = self.drive.CreateFile(metadata)
        file.SetContentString(content)               
        file.Upload()
        return self.CloudFile(file)

    def upload_file(self, file : str | Path| LocalFile, overwrite_ok = False) -> CloudFile:
        """Uploads a local file to the current working folder.\n
        If overwrite_ok == False and there is a file with the same name, will throw FileExistsError.\n
        Returns a CloudFile instance."""
        if (not isinstance(file, LocalFile)):
            f = LocalFile(file)
            return self.upload_file(f, overwrite_ok)        

        exists = self.search_in_folder(file.title)
        if (exists):
            if (not overwrite_ok):
                raise FileExistsError(f"A file named '{file.title}' already exists in the working folder.")
            for f in exists:
                self.delete_file(f)
        
        stat = file.stat
        modified_on = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
 
        print(f"Uploading {file.title}...", end=" ")

        metadata = {
        "title" : file.title,
        "parents" : [{"id" : self.current_folder}],
        "modifiedDate" : modified_on,
        "createdDate" : modified_on,
        }
        d_file = self.drive.CreateFile(metadata)
        d_file.SetContentFile(file._file)                
        d_file.Upload()
        
        print(f"Done.")
        return Drive_IO.CloudFile(d_file)

    def trash_file(self, file : GoogleDriveFile | CloudFile, to_delete = False):
        """Sends to trash or deletes given file, according to 'to_delete'."""
        if (isinstance(file, self.CloudFile)):
            file = file._file

        if to_delete:
            return file.Delete()
        return file.Trash()

    def delete_file(self, file : GoogleDriveFile | CloudFile):
        """Deletes given file.\n
        Syntactic sugar for trash_file(file, True)"""
        return self.trash_file(file, True)
    
    def upload_folder(self, folder : str | LocalFolder) -> CloudFolder:
        """Uploads a local folder in its entirety to the current working folder.
         Returns a Drive_IO.CloudFolder instance."""
        # TODO time elapsed during upload
        if (not isinstance(folder, LocalFolder)):
            f = LocalFolder(folder)
            return self.upload_folder(f)
        
        working_folder = self._f_id
        exists = self.get_folder(folder.title)
        if (exists):
            raise ApiRequestError(f"Folder '{folder.title}' already exists on current working folder.")
        
        cloud_folder = self.create_folder(folder.title, True)
        for file in folder.file_list:
            self.upload_file(file)

        for subfolder in folder.subfolder_list:
            self.upload_folder(subfolder)


        self._f_id = working_folder 
        # Returns Drive_IO to the previous working directory after any possible recursions.

        return Drive_IO.CloudFolder(cloud_folder)
        
    def trash_folder(self, folder : GoogleDriveFile | CloudFolder, to_delete = False):
        """Sends to trash or deletes given folder (including children files and folders), according to 'to_delete'."""
        if (isinstance(folder, Drive_IO.CloudFolder)):
            folder = folder._folder

        if (to_delete):
            return folder.Delete()
        return folder.Trash()
    
    def delete_folder(self, folder : GoogleDriveFile | CloudFolder):
        """Deletes given folder and children.\n
        Syntactic sugar for trash_folder(folder, True)"""
        return self.trash_folder(folder, True)

    @staticmethod
    def compare_files(file1 : str | LocalFile | CloudFile, file2: str | LocalFile | CloudFile) -> int:
        """Returns:\n
        -1 = files are different.\n
        0 = files are exactly the same.\n
        1 = file1 is a newer version of file2.\n
        2 = file2 is newer version of file1.
            
        Note that the comparison is based on name and date of modification only."""

        if (isinstance(file1, (str, Path))):
            file1 = LocalFile(file1)
        elif (isinstance(file1, GoogleDriveFile)):
            file1 = Drive_IO.CloudFile(file1)

        if (isinstance(file2, (str, Path))):
            file2 = LocalFile(file2)
        elif (isinstance(file2, GoogleDriveFile)):
            file2 = Drive_IO.CloudFile(file2)

        if (file1.title != file2.title):
            return -1
                    
        file1_modified = file1.modified_on_datetime
        file2_modified = file2.modified_on_datetime

        if (file1_modified == file2_modified):
            return 0
        
        ACCEPTABLE_DIFFERENCE = timedelta(microseconds = 2000)
        """Google Drive shaves off a few microseconds of the modified on date during upload."""
        diff = abs(file1_modified - file2_modified)
        if (diff <= ACCEPTABLE_DIFFERENCE):
            return 0

        if (file1_modified > file2_modified):
            return 1
        return 2


        



        

