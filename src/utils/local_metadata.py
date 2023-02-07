import jsons

from utils.local_files import LocalFile, LocalFolder

class FolderMetadata:
    """The collection of files' metadata from a local folder. 
    Meant to be written to a metadata (text) file, inside a Drive folder.
    Drive changes some of the file's metadata on upload, making this a necessity."""
    def __init__(self, folder : LocalFolder):
        self.files = {}
        for file in folder.index:
            if (isinstance(file, LocalFile)):
                self.files[file.name] = {'local_lastmodified' : file.last_modified, 'comment' : ''}
            
            
def metadata_to_json(metadata : LocalFolder) -> str:
    return jsons.dumps(metadata)

def json_to_metadata(json : str) -> FolderMetadata:
    return jsons.load(json, FolderMetadata)
