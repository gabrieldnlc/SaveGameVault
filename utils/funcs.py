from pydrive2.drive import GoogleDrive

def GetFolderList(drive : GoogleDrive, parent_id : str = 'root') -> list :
    query = "'{}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false".format(parent_id)
    file_list = drive.ListFile({'q': query }).GetList()
    return file_list

def PrintFolderList(drive : GoogleDrive, parent_id : str = 'root') -> None:
    list = GetFolderList(drive, parent_id)
    for folder in list:
        print('Title: %s, id: %s' % (folder['title'], folder['id']))

def CreateFolder(drive : GoogleDrive, folder_name : str, parent_id : str = 'root') -> bool:
    try:
        folder = drive.CreateFile({'title': folder_name, 
        "parents":  [{"id": parent_id}], 
        "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        return True
    except: # TODO extend error catching
        return False

def FolderExists(drive: GoogleDrive, folder_name : str, parent_id : str = 'root') -> bool | GoogleDrive: 
    list = GetFolderList(drive, parent_id)

    for folder in list:
        if (folder['title'] == folder_name):
            return folder
            break
        
    return False

