import unittest
import asyncio
from app.store import DataStore

class TestEvictionDaemon(unittest.IsolatedAsyncioTestCase):
    """Test suite for eviction loop"""

    async def asyncSetUp(self) -> None:
        """Creates a fresh db instance for each test"""
        self.db = DataStore()

    async def test_eviction(self):
        """Checks daemon purges expired keys in background"""
        self.db.set("temp_key", "value", px=50)

        daemon_task = asyncio.create_task(self.db.eviction_loop())
        await asyncio.sleep(0.1)
        daemon_task.cancel()

        self.assertFalse(self.db.exists("temp_key"))
        self.assertEqual(len(self.db._expiry_heap), 0)

    async def test_ttl_override_skips_eviction(self):
        """Makes sure overriding a TTL prevents a premature eviction"""
        self.db.set("sticky_key", "value", px=50)
        
        self.db.set("sticky_key", "new_value", px=500)
        
        daemon_task = asyncio.create_task(self.db.eviction_loop())

        await asyncio.sleep(0.1)
        daemon_task.cancel()
        
        self.assertTrue(self.db.exists("sticky_key"))
        self.assertEqual(self.db.get("sticky_key"), "new_value")

if __name__ == "__main__":
    unittest.main()