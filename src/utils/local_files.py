from pathlib import Path

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
        
        return (self.name == other.name) and (self.size == other.size) and (self.last_modified == other.last_modified)

    @property
    def stat(self):
        return self.path.stat()
    @property
    def name(self):
        return self.path.name
    @property
    def size(self):
        return self.stat.st_size
    @property
    def last_modified(self):
        return self.stat.st_mtime

    def __str__(self):
        return f"LocalFile: {self.__repr__()}"
    def __repr__(self):
        return self.path.__str__()

class LocalFolder():
    """An encapsulation of a pathlib.Path, for efficiency and readability. Specialized to deal with folders."""
    
    def __init__(self, path : str | Path):
        self.path = Path(path)        

        if (self.path.is_file()):
            raise NotADirectoryError(f"'{path}' is not a folder, but a file.")

        if (not self.path.exists()):
            raise FileNotFoundError(f"'{path} is not a valid folder.'")
        
        list_folders = []
        list_files = []
        for x in self.path.iterdir():
            if (x.is_dir()):
                list_folders.append(LocalFolder(x))
            else:
                list_files.append(LocalFile(x))

        self.index = list_folders + list_files
        """Folders come first, then files. If looking for folders only, stop the search at first file."""
            
    @property
    def stat(self):
        return self.path.stat()
    @property
    def size(self):
        return self.stat.st_size
    @property
    def name(self):
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
