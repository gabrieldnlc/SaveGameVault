# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive

from .funcs import *

class MainIndex:
    def __init__(self, drive : GoogleDrive):
        self.update(drive)

    def update(self, drive : GoogleDrive, target_folder : GoogleDriveFile = None) -> bool :
        if (target_folder == None):
            target_folder = FolderExists(drive, vault_folder)
            if (not target_folder):
                target_folder = CreateFolder(drive, vault_folder)
        games_list = GetFolderList(drive, target_folder['id'])
        

    
        
    
