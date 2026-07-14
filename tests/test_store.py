import unittest
import time
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

    def test_passive_expiration_on_get(self):
        """Checks that get returns None and deletes key is TTL passed"""
        self.db.set("temp_key", "10", px=10)
        time.sleep(0.02)

        self.assertIsNone(self.db.get("temp_key"))
        self.assertNotIn("temp_key", self.db._store)

    def test_passive_expiration_on_exists(self):
        """Checks that exists() triggers eviction of stale keys"""
        self.db.set("temp_key", "10", px=10)
        time.sleep(0.02)

        self.assertFalse(self.db.exists("temp_key"))

    def test_overwrite_clear_ttl(self):
        """Checks if overwriting a key without a px clears TTL"""
        self.db.set("temp_key", "10", px=10)
        self.db.set("temp_key", "troll")

        time.sleep(0.02)

        self.assertEqual(self.db.get("temp_key"), "troll")

if __name__ == "__main__":
    unittest.main()