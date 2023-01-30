from pydrive2.drive import GoogleDrive, GoogleDriveFile

from .consts import *

def get_folder_list(drive: GoogleDrive, parent_id: str = 'root') -> list :
    query = f"'{parent_id}' in parents and mimeType='{mime_folder}' and trashed=false"
    file_list = drive.ListFile({'q': query }).GetList()
    return file_list

def print_folder_list(folder_list: list) -> None:
    for folder in folder_list:
        print('Title: %s, id: %s' % (folder['title'], folder['id']))

def create_folder(drive: GoogleDrive, folder_name: str, parent_id: str = 'root') -> GoogleDriveFile | bool:
    try:
        folder = drive.CreateFile({'title': folder_name, 
        "parents":  [{"id": parent_id}], 
        "mimeType": mime_folder})
        folder.Upload()
        return folder
    except: # TODO extend error catching
        return False

def get_folder(drive: GoogleDrive, folder_name: str, parent_id: str = 'root') -> GoogleDriveFile | bool: 
    list = get_folder_list(drive, parent_id)
    for folder in list:
        if (folder['title'] == folder_name):
            return folder
    return False

def get_file_matches(drive: GoogleDrive, title: str, parent_id: str = 'root') -> list | bool:
    query = f"'{parent_id}' in parents and title='{title}' and trashed=false"
    file_list = drive.ListFile({'q': query }).GetList()
    if (len(file_list) == 0):
        return False
    return file_list
        