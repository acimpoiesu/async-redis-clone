import unittest
from unittest.mock import AsyncMock, MagicMock
from app.server import connection_handler

class TestTransportLayer(unittest.IsolatedAsyncioTestCase):
    """ Test suite for the raw TCP transport layer and socket handling  """

    async def test_connection_handler_ping_pong(self):
        """
        Simulates a client sending the raw bytes and verifies
        server reads bytes and writes a PONG back before closing.
        """

        # (Arrange) create fake async sockets
        mock_reader = AsyncMock()
        mock_reader.read.side_effect = [b"*1\r\n$4\r\nPING\r\n", b""]

        mock_writer = MagicMock()
        # fake ip addr extraction so print statements don't crash
        mock_writer.get_extra_info.return_value = "127.0.0.1:55555"
        mock_writer.drain = AsyncMock()
        mock_writer.wait_closed = AsyncMock()

        # (Act) run handler with fake sockets
        await connection_handler(mock_reader, mock_writer)

        # (Assert) verify engine attempted to write the pong
        mock_writer.write.assert_called_with(b"+PONG\r\n")
        mock_writer.drain.assert_awaited()
        # verify sockets shut down cleanly
        mock_writer.close.assert_called_once()
        mock_writer.wait_closed.assert_called_once()

if __name__ == "__main__":
    unittest.main()