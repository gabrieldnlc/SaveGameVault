from pathlib import Path

class LocalFile():

    def __init__(self, path : str | Path):
        try:
            self.path = Path(path)
            stat = self.path.stat()

            if (self.path.is_dir()):
                raise IsADirectoryError(f"'{path}' is not a file, but a folder.")
            self.filename = self.path.name
            self.size = stat.st_size
            self.last_modified = stat.st_mtime

        except FileNotFoundError:
            raise FileNotFoundError(f"'{path}' does not exist.") # defaulting to an English message instead of the OS language
         
class LocalFolder():
    def __init__(self, path : str | Path):
        try:
            self.path = Path(path)
            stat = self.path.stat()

            if (self.path.is_file()):
                raise NotADirectoryError(f"'{path}' is not a folder, but a file.")
            self.path = path
            self.size = stat.st_size

        except FileNotFoundError:
            raise FileNotFoundError(f"'{path}' is not a valid folder.")   