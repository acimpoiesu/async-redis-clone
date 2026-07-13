import unittest
from app.server import handle_command
from app.store import db

class TestCommandRouter(unittest.TestCase):
    """Test suite for RESP command routing engine"""

    def setUp(self) -> None:
        """Clears global datastore to ensure isolation"""
        db._store.clear()

    def test_ping_command(self):
        """Verifies PING returns PONG and deals with case insensitivity"""
        self.assertEqual(handle_command(["PING"]), b"+PONG\r\n")
        self.assertEqual(handle_command(["ping"]), b"+PONG\r\n")

    def test_command_docs(self):
        """Makes sure the COMMAND returns an empty array"""
        self.assertEqual(handle_command(["Command", "DOCS"]), b"*0\r\n")

    def test_set_valid(self):
        """Verifies SET correctly stores data and returns OK"""
        response = handle_command(["SET", "color", "blue"])
        self.assertEqual(response, b"+OK\r\n")
        self.assertEqual(db.get("color"), "blue")

    def test_get_valid(self):
        """Checks if GET correctly retrieves data"""
        db.set("color", "blue")
        self.assertEqual(handle_command(["GET", "color"]), b"$4\r\nblue\r\n")

    def test_get_invalid_key(self):
        """Checks if GET on an unknown key returns a RESP Null bulk string"""
        self.assertEqual(handle_command(["GET", "red"]), b"$-1\r\n")

    def test_argument_boundaries(self):
        """Verifies commands reject invalid arg counts"""
        self.assertEqual(
            handle_command(["SET", "key"]), b"-ERR ERR wrong number of args for set command\r\n"
        )
        self.assertEqual(
            handle_command(["GET", "key1", "key2"]), b"-ERR ERR wrong number of args for get command\r\n"
        )
    
    def test_unknown_command(self):
        """Verifies unknown command returns a standard error"""
        self.assertEqual(handle_command(["SUPER_SET"]), b"-ERR ERR unknown command SUPER_SET\r\n")

if __name__ == "__main__":
    unittest.main()