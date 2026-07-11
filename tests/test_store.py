import unittest
from app.store import DataStore

class TestDataStore(unittest.TestCase):
    """ Test suite for in memory key value engine """

    def setUp(self) -> None:
        """Creates fresh instance"""
        self.db = DataStore()

    def test_set_and_get(self):
        """ Verifies data can be stored and retrieved """
        self.db.set("framework", "flask")
        self.assertEqual(self.db.get("framework"), "flask")

    def test_get_nonexistent_key(self):
        """ Verifies a missing key returns None """
        self.assertIsNone(self.db.get("nonexistent_key"))

    def test_exists(self):
        """ Verifies exists method identifies keys existence correctly """
        self.db.set("name", "Alex")
        self.assertTrue(self.db.exists("name"))
        self.assertFalse(self.db.exists("Jimmy"))

if __name__ == "__main__":
    unittest.main()