import unittest
from os import getcwd
from pathlib import Path

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.drive_IO import Drive_IO

class TestComparison(unittest.TestCase):
    # Needs to connect to a Google Drive account to test.

    def check_environment(self):
        # For these integration tests, we need a temporary folders locally and in the cloud.
        # They will be deleted during clean-up.

        CLOUD_TEMP_DIR = "cloud_tests"
        has_folder = self.drive.get_folder(CLOUD_TEMP_DIR)
        if (has_folder):
            raise RuntimeError(f"The cloud environment already has a '{CLOUD_TEMP_DIR}' folder. Delete it and try again.")
        self.drive.create_folder(CLOUD_TEMP_DIR, True)
        

        LOCAL_TEMP_DIR = "local_tests"
        new_dir = Path(getcwd()) / LOCAL_TEMP_DIR
        if (new_dir.exists()):
            raise RuntimeError(f"The local environment already has a '{LOCAL_TEMP_DIR}' folder. Delete it and try again.")

    @classmethod
    def setUpClass(cls):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        cls.drive = Drive_IO(GoogleDrive(gauth))
        cls.environment_checked = False

    @classmethod
    def setUp(self):
        if (self.environment_checked):
            return
        self.environment_checked = True
        self.check_environment(self)
     

    @classmethod
    def tearDownClass(cls):
        pass
        # TODO: delete both folders created for testing.

    def test_comparison(self):
        self.assertEqual(1, 1)

    def test_something(self):
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()