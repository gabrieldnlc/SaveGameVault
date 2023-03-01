import unittest
from os import getcwd
from pathlib import Path
from shutil import rmtree
from datetime import timedelta

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.drive_IO import Drive_IO
from utils.local_files import LocalFile

class TestComparison(unittest.TestCase):
    # Needs to connect to a Google Drive account to test.

    def prepare_environment(self):
        # For these integration tests, we need a temporary folders locally and in the cloud.
        # They will be deleted during clean-up.

        cloud_folder_already = self.drive.get_folder(self.CLOUD_TEMP_DIR)
        if cloud_folder_already:
            raise RuntimeError(f"The cloud environment already has a '{self.CLOUD_TEMP_DIR}' folder. Delete it and try again.")
        self.cloud_folder = self.drive.create_folder(self.CLOUD_TEMP_DIR, True)
        self.created_cloud_folder = True
        
        self.local_folder = Path(getcwd()) / self.LOCAL_TEMP_DIR
        self.local_folder.mkdir(exist_ok = False)
        self.created_local_folder = True
        


    @classmethod
    def setUpClass(cls):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        cls.drive = Drive_IO(GoogleDrive(gauth))
        cls.environment_prepared = False

        cls.CLOUD_TEMP_DIR = "cloud_tests"
        cls.cloud_folder = None
        cls.created_cloud_folder = False
        
        cls.LOCAL_TEMP_DIR = "local_tests"
        cls.local_folder = None
        cls.created_local_folder = False
        

    @classmethod
    def setUp(self):
        if (self.environment_prepared):
            return
        self.environment_prepared = True
        self.prepare_environment(self)
     

    @classmethod
    def tearDownClass(cls):
        if not cls.environment_prepared:
            return
        cls.drive.go_to_root()
        
        
        if (cls.cloud_folder != None and cls.created_cloud_folder):
            cls.cloud_folder.Delete()

        if (cls.local_folder != None and cls.created_local_folder):
            rmtree(cls.local_folder)

    def test_comparison(self):
        test_text = (
        "Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit.\n" 
        "Nunc sit amet luctus sem, ut scelerisque sem.\n"
        "Maecenas quis elit nulla.\n"
        "Donec ut nisl eget leo consectetur rhoncus vel imperdiet nisl.\n"
        "Vestibulum eu ante a ligula rutrum rhoncus."
        )

        test_file = self.local_folder / "test_file.txt"
        test_file.touch(exist_ok = False)
        test_file.write_text(test_text)

        local = LocalFile(test_file)
        uploaded = Drive_IO.CloudFile(self.drive.upload_file(test_file))

        comparison = self.drive.compare_files(local, uploaded)
        self.assertEqual(comparison, 0)

        
        

        

        



if __name__ == "__main__":
    unittest.main()