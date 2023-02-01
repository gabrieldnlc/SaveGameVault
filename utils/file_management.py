from pathlib import Path

class LocalFile():

    def __init__(self, path : str | Path):
        self.path = Path(path)

        if (self.path.is_dir()):
            raise IsADirectoryError(f"'{path}' is not a file, but a folder.")

        if (not self.path.exists()):
            raise FileNotFoundError(f"'{path}' does not exist.")

    @property
    def stat(self):
        return self.path.stat()
    @property
    def filename(self):
        return self.path.name
    @property
    def size(self):
        return self.stat.st_size
    @property
    def last_modified(self):
        return self.stat.st_mtime

class LocalFolder():
    def __init__(self, path : str | Path):
        self.path = Path(path)

        if (self.path.is_file()):
            raise NotADirectoryError(f"'{path}' is not a folder, but a file.")

        if (not self.path.exists()):
            raise FileNotFoundError(f"'{path} is not a valid folder.'")

    @property
    def stat(self):
        return self.path.stat()
    @property
    def size(self):
        return self.stat.st_size