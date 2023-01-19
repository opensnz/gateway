
from database import *
import secrets

import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        print("\nSetup....")
        return super().setUp()

    def tearDown(self) -> None:
        print("TearDown...")
        return super().tearDown()

    def test_insert_device(self):
        db.open()
        size = 10
        for i in range(size):
            DevEUI = secrets.token_hex(8)
            AppKey = secrets.token_hex(16)
            AppEUI = secrets.token_hex(8)
            status = db.insert_device(DevEUI=DevEUI, AppEUI=AppEUI, AppKey=AppKey)
            self.assertTrue(status, "Device with DevEUI = " + DevEUI + " is not inserted!!!")
        devices = db.get_devices()
        if len(devices) == size:
            print(str(size) + " devices inserted successfully")
            for device in devices:
                #db.delete_device(device["DevEUI"])
                #device = db.get_device(device["DevEUI"])
                print(device)
        devices = db.get_devices()
        print(devices)


if __name__ == "__main__":
    import os 
    if os.path.exists(SQLITE_DATABASE_PATH):
        os.remove(SQLITE_DATABASE_PATH)
    db = Database()
    db.open()
    db.create_tables()
    unittest.main()
    devices = db.get_devices()
    db.close()
    for device in devices:
        print(device)