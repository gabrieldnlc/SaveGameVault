import unittest
from os import getcwd
from pathlib import Path
from shutil import rmtree
from time import sleep

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
            if (self.gentle_prepare):
                raise RuntimeError(f"The cloud environment already has a '{self.CLOUD_TEMP_DIR}' folder and gentle_prepare == True. Delete it and try again.")
            self.drive.delete_folder(cloud_folder_already)

        self.cloud_folder = self.drive.create_folder(self.CLOUD_TEMP_DIR, True)
        self.created_cloud_folder = True
        
        self.local_folder = Path(getcwd()) / self.LOCAL_TEMP_DIR
        if (self.local_folder.exists()):
            if (self.gentle_prepare):
                raise FileExistsError(f"The local environment already has a '{self.LOCAL_TEMP_DIR}' folder and gentle_prepare == True. Delete it and try again.")
            rmtree(self.local_folder)

        self.local_folder.mkdir(exist_ok = False)
        self.created_local_folder = True
        
    @classmethod
    def setUpClass(cls):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        cls.drive = Drive_IO(GoogleDrive(gauth))
        cls.environment_prepared = False
        cls.gentle_prepare = False

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


    def _create_and_fill(self, filename : str, content : str, exist_ok = False) -> Path:
        file = self.local_folder / filename
        file.touch(exist_ok = exist_ok)
        file.write_text(content)
        return file
    
    def test_upload(self):
        test_text = "Just a simple test. A unittest, even."
        first_local = LocalFile(self._create_and_fill("upload_test.txt", test_text))

        # Uploading a file.
        first_cloud = self.drive.upload_file(first_local, overwrite_ok = False)
        comparison = self.drive.compare_files(first_local, first_cloud)
        self.assertEqual(comparison, 0)

        # Trying to upload a file that already exists with exists_ok == False.
        self.assertRaises(FileExistsError, self.drive.upload_file, first_local, False)
        
        # Trying to upload a file that already exists with exists_ok == True.
        first_local._file.write_text(test_text * 2)

        first_cloud = self.drive.upload_file(first_local, overwrite_ok = True)

        files = self.drive.search_in_folder("upload_test.txt")
        self.assertEqual(len(files), 1)

        
        

    def test_comparison(self):
        test_text = (
        "Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit.\n" 
        "Nunc sit amet luctus sem, ut scelerisque sem.\n"
        "Maecenas quis elit nulla.\n"
        "Donec ut nisl eget leo consectetur rhoncus vel imperdiet nisl.\n"
        "Vestibulum eu ante a ligula rutrum rhoncus."
        )

        comparison_test = self._create_and_fill("comparison_test.txt", test_text, False)

        local = LocalFile(comparison_test)
        uploaded = self.drive.upload_file(comparison_test)

        # Same file, but on different environments.
        self.assertEqual(self.drive.compare_files(local, uploaded), 0)
        # Same file on the same environment.
        self.assertEqual(self.drive.compare_files(local, local), 0)
        self.assertEqual(self.drive.compare_files(uploaded, uploaded), 0)

        comparison_test2 = self._create_and_fill("comparison_test2.txt", test_text.upper(), False)

        local2 = LocalFile(comparison_test2)
        uploaded2 = self.drive.upload_file(comparison_test2)
        
        # Same file, but on different environments.
        self.assertEqual(self.drive.compare_files(local2, uploaded2), 0)
        # Different files on the same environment.
        self.assertEqual(self.drive.compare_files(uploaded2, uploaded), -1)
        self.assertEqual(self.drive.compare_files(local2, local), -1)
        # Different files on different environments.
        self.assertEqual(self.drive.compare_files(uploaded2, local), -1)
        self.assertEqual(self.drive.compare_files(local2, uploaded), -1)

        # Same file, but first file is newer
        compare = "Just a comparison."
        comparing_cloud = self.drive.create_file("comparing_date.txt", compare)
        sleep(2)
        comparing_local = LocalFile(self._create_and_fill("comparing_date.txt", compare))
        comparison = self.drive.compare_files(comparing_local, comparing_cloud)
        self.assertEqual(comparison, 1)
        
        # Same file, but second file is newer
        comparing_local_2 = LocalFile(self._create_and_fill("comparing_date_2.txt", compare))
        sleep(2)
        comparing_cloud_2 = self.drive.create_file("comparing_date_2.txt", compare)
        comparison = self.drive.compare_files(comparing_local_2, comparing_cloud_2)
        self.assertEqual(comparison, 2)

        

        



if __name__ == "__main__":
    unittest.main()