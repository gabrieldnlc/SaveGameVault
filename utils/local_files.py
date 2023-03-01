from pathlib import Path

from datetime import datetime, timezone

class LocalFile():
    """An encapsulation of a pathlib.Path, for efficiency and readability. Specialized to deal with files."""

    def __init__(self, path : str | Path):
        self.path = Path(path)

        if (self.path.is_dir()):
            raise IsADirectoryError(f"'{path}' is not a file, but a folder.")

        if (not self.path.exists()):
            raise FileNotFoundError(f"'{path}' does not exist.")

    def __eq__(self, other):
        if not isinstance(other, LocalFile):
            return False
        
        return (self.title == other.title) and (self.size == other.size) and (self.modified_on == other.modified_on)

    @property
    def stat(self):
        return self.path.stat()
    @property
    def title(self):
        return self.path.name
    @property
    def size(self):
        return self.stat.st_size
    @property
    def modified_on(self):
        """Last modified time, in seconds."""
        return self.stat.st_mtime
    @property
    def modified_on_iso(self):
        """Last modified time, in ISO format."""
        return datetime.fromtimestamp(self.modified_on, timezone.utc).isoformat()
    @property
    def modified_on_datetime(self) -> datetime:
        """Last modified time, wrapped in a datetime instance."""
        return datetime.fromisoformat(self.modified_on_iso)

    def __str__(self):
        return f"LocalFile: {self.__repr__()}"
    def __repr__(self):
        return self.path.__str__()

class LocalFolder():
    """An encapsulation of a pathlib.Path, for efficiency and readability. 
    Specialized to deal with folders."""
    
    def __init__(self, path : str | Path):
        self.path = Path(path)        

        if (self.path.is_file()):
            raise NotADirectoryError(f"'{path}' is not a folder, but a file.")

        if (not self.path.exists()):
            raise FileNotFoundError(f"'{path} is not a valid folder.'")
        
        self.subfolder_list = []
        self.file_list = []
        for x in self.path.iterdir():
            if (x.is_dir()):
                self.subfolder_list.append(LocalFolder(x))
            else:
                self.file_list.append(LocalFile(x))
        
    @property
    def index(self):
        """Subfolders come first, then files."""
        return self.subfolder_list + self.file_list
    @property
    def stat(self):
        return self.path.stat()
    @property
    def size(self):
        return self.stat.st_size
    @property
    def title(self):
        return self.path.name

    def __str__(self):
        return f"LocalFolder: {self.__repr__()}"
    def __repr__(self):
        return self.path.__str__()
    def simple_repr(self) -> list:
        """Returns a simple representation of the folder: a list with names (including subfolders)."""
        l = []
        for file in self.index:
            l.append(file.name)
        return l
