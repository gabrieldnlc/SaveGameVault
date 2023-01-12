def GetFolderList(drive, parent_id = 'root') -> list :
    query = "'{}' in parents and mimeType='application/vnd.google-apps.folder'".format(parent_id)
    file_list = drive.ListFile({'q': query }).GetList()
    return file_list

def PrintFolderList(drive, parent_id = 'root') -> None:
    list = GetFolderList(drive, parent_id)
    for folder in list:
        print('title: %s, id: %s' % (folder['title'], folder['id']))

def CreateFolder(drive, folder_name, parent_id = 'root') -> bool:
    try:
        folder = drive.CreateFile({'title': folder_name, 
        "parents":  [{"id": parent_id}], 
        "mimeType": "application/vnd.google-apps.folder"})
        folder.Upload()
        return True
    except: # TODO extend error catching
        return False

def FolderExists(drive, folder_name, parent_id = 'root') -> bool:
    list = GetFolderList(drive, parent_id)

    found = False
    for folder in list:
        if (folder['title'] == folder_name):
            found = True
            break
    return found

