import unittest
from app.protocol import parse_response

class TestProtocolParser(unittest.TestCase):
    """
    Test suite for RESP deserialization engine
    """

    def test_parse_valid_response_array(self):
        """Verifies a RESP array is parsed correctly"""
        raw_data = b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$4\r\nAlex\r\n"
        elements, consumed = parse_response(raw_data)

        self.assertEqual(elements, ["SET", "name", "Alex"])
        self.assertEqual(consumed, len(raw_data))

    def test_parse_incomplete_buffer(self):
        """ Checks if fragmented TCP returns empty data without crashing """
        fragmented_data = b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$4\r\nAle" # removed x and CRLF
        elements, consumed = parse_response(fragmented_data)

        self.assertEqual(elements, [])
        self.assertEqual(consumed, 0)

    def test_invalid_header_error(self):
        """ Tests if invalid header (doesn't start with '*') returns a ValueError """
        invalid_data = b"+PONG\r\n"

        with self.assertRaises(ValueError) as error_catch:
            parse_response(invalid_data) 
        self.assertIn("Expected RESP array", str(error_catch.exception))
    
    def test_malformed_integer_error(self):
        """ Verifies corrputed length raises a ValueError"""
        corrupted_data = b"*XYZ\r\n$3\r\nSET\r\n"

        with self.assertRaises(ValueError) as error_catch:
            parse_response(corrupted_data)
        self.assertIn("Invalid array length", str(error_catch.exception))

    def test_missing_str_terminator(self):
        bad_terminator_data = b"*1\r\n$4\r\nAlex\t\n" # made \r -> \t

        with self.assertRaises(ValueError) as error_catch:
            parse_response(bad_terminator_data)
        self.assertIn("not terminated by CRLF", str(error_catch.exception))
    
if __name__ == "__main__":
    unittest.main()