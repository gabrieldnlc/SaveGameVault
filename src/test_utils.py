import unittest
from os import getcwd
from utils.file_management import *

class TestFileManagement(unittest.TestCase):

    def test_exceptions(self):
        curr_folder = Path(getcwd()) # We can only be certain that it is a folder, but that's enough for the testing at hand.
        not_folder = curr_folder / "not"
        
        this_file = Path(__file__)
        self.assertTrue(this_file.exists(), "Could not create a valid Path instance via the __file__ variable")
        
        """You can only create a LocalFolder instance with a valid existing folder, not files."""
        LocalFolder(curr_folder) # Should not raise any errors
        self.assertRaises(FileNotFoundError, LocalFolder, not_folder)
        self.assertRaises(NotADirectoryError, LocalFolder, this_file)        

        """Similarly, a LocalFile instance can only be created with a valid existing file, not folders."""
        LocalFile(this_file)
        self.assertRaises(FileNotFoundError, LocalFile, __file__ + "not")
        self.assertRaises(IsADirectoryError, LocalFile, curr_folder)

if __name__ == "__main__":
    unittest.main()