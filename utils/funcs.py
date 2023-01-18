from pydrive2.drive import GoogleDrive, GoogleDriveFile

vault_folder = "Save Game Vault"

def GetFolderList(drive : GoogleDrive, parent_id : str = 'root') -> list :
    query = "'{}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false".format(parent_id)
    file_list = drive.ListFile({'q': query }).GetList()
    return file_list

def PrintFolderList(folder_list : list) -> None:
    for folder in folder_list:
        print('Title: %s, id: %s' % (folder['title'], folder['id']))

def CreateFolder(drive : GoogleDrive, folder_name : str, parent_id : str = 'root') -> GoogleDriveFile | bool:
    try:
        folder = drive.CreateFile({'title': folder_name, 
        "parents":  [{"id": parent_id}], 
        "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        return folder
    except: # TODO extend error catching
        return False

def FolderExists(drive: GoogleDrive, folder_name : str, parent_id : str = 'root') -> GoogleDriveFile | bool: 
    list = GetFolderList(drive, parent_id)

    for folder in list:
        if (folder['title'] == folder_name):
            return folder
            break
        
    return False


    
