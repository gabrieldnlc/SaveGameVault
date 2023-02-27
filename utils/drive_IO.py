from datetime import datetime, timezone

from pydrive2.drive import GoogleDrive, GoogleDriveFile
from pydrive2.files import ApiRequestError

from .consts import *
from .local_files import LocalFile, LocalFolder



class Drive_IO():
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
        def modified_on(self):
            """Last modified time, in ISO format."""
            return self._file['modifiedDate']
        @property
        def modified_on_iso(self):
            """Last modified time, in ISO format.
            An alias of modified_on()."""
            return self.modified_on()
            
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
        """Returns an instance of GoogleDriveFile pointing to the ID.
        Returns False if file or folder does not exist."""
        try:
            return self.drive.CreateFile({'id': id})
        except ApiRequestError:
            return False
    
    def _create_indexed_instance(self, drive_file : GoogleDriveFile) -> CloudFile | CloudFolder:
        mime = drive_file['mimeType']
        if (mime != MIME_FOLDER):
            return self.CloudFile(drive_file)
        else:
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
        """Creates (and returns) a 'folder_name' folder inside of current working directory.
        If enter_after == True, working directory will be changed to the newly created folder."""

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
        """Moves one directory down, into 'child_folder' of current working directory. 
        Returns True if success, False if folder does not exist."""
        new_dir = self.get_folder(child_folder)
        if (not new_dir):
            return False
        self.current_folder = new_dir
        return True

    def get_folder(self, folder_name : str) -> GoogleDriveFile | bool:
        """Searches for (and returns) 'folder_name' inside of current folder.
          Returns a GoogleDriveFile instance or False if folder does not exist."""
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

    def upload_file(self, file : str | LocalFile) -> bool:
        """Uploads a local file to the current working folder.
        Returns a GoogleDriveFile instance or False on fail."""
        if (isinstance(file, str)):
            f = LocalFile(file)
            return self.upload_file(f)
        
        if not (isinstance(file, LocalFile)):
            raise FileNotFoundError(f"Could not find '{file}'")
        

        stat = file.stat
        modified_on = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()

        metadata = {
            "title" : file.name,
            "parents" : [{"id" : self.current_folder}],
            "modifiedDate" : modified_on
            }
        d_file = self.drive.CreateFile(metadata)
        d_file.SetContentFile(file.path)
        print(f"Uploading {file.name}...", end=" ")
        d_file.Upload()
        print(f"Done.")
        return d_file

    def upload_folder(self, folder : str | LocalFolder) -> bool:
        """Uploads a local folder in its entirety to the current working folder.
         Returns a GoogleDriveFile instance or False on fail."""
        # TODO time elapsed during upload
        if (isinstance(folder, str)):
            f = LocalFolder(folder)
            return self.upload_folder(f)
        
        if not (isinstance(folder, LocalFolder)):
            return False # TODO create an error class for this situation
        
        working_folder = self._f_id
        exists = self.get_folder(folder.name)
        if (exists):
            raise ApiRequestError(f"Folder '{folder.name}' already exists on current working folder.")
        
        new_folder = self.create_folder(folder.name, True)
        for file in folder.file_list:
            self.upload_file(file)

        for subfolder in folder.subfolder_list:
            self.upload_folder(subfolder)


        self._f_id = working_folder 
        # Returns Drive_IO to the previous working directory after any possible recursions.
        
    
def compare_files(file1 : LocalFile | Drive_IO.CloudFile, file2: LocalFile | Drive_IO.CloudFile) -> int:
    """Returns:\n
    -1 = files are different.\n
    0 = files are exactly the same.\n
    1 = file1 is a newer version of file2.\n
    2 = file2 is newer version of file1.
        
    Note that the comparison is based on name and date of modification only."""

    if (file1.name != file2.name):
        return -1
    if (file1.modified_on_iso == file2.modified_on_iso):
        return 0
        
    file1_modified = datetime.fromisoformat(file1.modified_on_iso)
    file2_modified = datetime.fromisoformat(file2.modified_on_iso)

    if (file1_modified > file2_modified):
        return 1
    return 2


        



        

