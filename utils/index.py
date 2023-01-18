# reminder: set the remove_bom parameter in GetContentString()

from pydrive2.drive import GoogleDrive

from .funcs import *

class MainIndex: 
    # An object representing the Drive folders for the UI
    def __init__(self, drive : GoogleDrive):
        self.games = {}
        self.drive = drive
        self.Update()

        
    def PopulateIndexedGames(self, folder : GoogleDriveFile):
        self.games = {}
        folder_list = GetFolderList(self.drive, folder['id'])
        for game in folder_list:
            g = self.IndexedGame(self.drive, game)
            self.games.append(g)
            

    def Update(self, target_folder : GoogleDriveFile = None) -> bool :
        if (target_folder == None):
            target_folder = FolderExists(self.drive, vault_folder)
            if (not target_folder):
                target_folder = CreateFolder(self.drive, vault_folder)
        self.PopulateIndexedGames(target_folder)
        

    class IndexedGame():
        # An object representing one of the Save Game folders. MainIndex holds a list of these.
        def __init__(self, drive : GoogleDrive, folder : GoogleDriveFile):
            if (folder['mimeType'] != 'application/vnd.google-apps.folder'):
                raise Exception("Cannot create an Index based on a single file.") # TODO: better exception
            self.meta = {}
            self.saves = {}
            self.title = folder['title']
            folders = GetFolderList(drive, folder['id'])

        
    
        
    
