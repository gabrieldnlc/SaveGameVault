from pydrive2.drive import GoogleDrive, GoogleDriveFile

from .consts import *

def GetFolderList(drive: GoogleDrive, parent_id: str = 'root') -> list :
    query = f"'{parent_id}' in parents and mimeType='{mime_folder}' and trashed=false"
    file_list = drive.ListFile({'q': query }).GetList()
    return file_list

def PrintFolderList(folder_list: list) -> None:
    for folder in folder_list:
        print('Title: %s, id: %s' % (folder['title'], folder['id']))

def CreateFolder(drive: GoogleDrive, folder_name: str, parent_id: str = 'root') -> GoogleDriveFile | bool:
    try:
        folder = drive.CreateFile({'title': folder_name, 
        "parents":  [{"id": parent_id}], 
        "mimeType": mime_folder})
        folder.Upload()
        return folder
    except: # TODO extend error catching
        return False

def GetFolder(drive: GoogleDrive, folder_name: str, parent_id: str = 'root') -> GoogleDriveFile | bool: 
    list = GetFolderList(drive, parent_id)
    for folder in list:
        if (folder['title'] == folder_name):
            return folder
    return False

def GetFileMatches(drive: GoogleDrive, title: str, parent_id: str = 'root') -> list | bool:
    query = f"'{parent_id}' in parents and title='{title}' and trashed=false"
    file_list = drive.ListFile({'q': query }).GetList()
    if (len(file_list) == 0):
        return False
    return file_list
        