import unittest

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from utils.drive_IO import Drive_IO

class TestComparison(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        cls.drive = Drive_IO(GoogleDrive(gauth))

        # For these integration tests, we need a temporary folders locally and in the cloud.
        # They will be deleted during clean-up.

        CLOUD_TEMP_DIR = "tests_temporary"

        cls.assertFalse(
            cls.drive.get_folder(CLOUD_TEMP_DIR),
            f"There is already a {CLOUD_TEMP_DIR} folder on the root of Drive.")
        
        LOCAL_TEMP_DIR = "tests_temporary"

    @classmethod
    def tearDownClass(cls):
        # TODO delete both cloud and local temporary folders.
        raise NotImplementedError()

    def test_comparison(self):
        raise NotImplementedError()

    def test_something(self):
        raise NotImplementedError()

if __name__ == "__main__":
    unittest.main()