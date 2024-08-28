# tests/test_core.py

import unittest
from obfusguard.core import encode, decode

class TestCore(unittest.TestCase):

    def test_encode_decode(self):
        message = "hi"
        encoded = encode(message)
        decoded = decode(encoded)
        self.assertEqual(message, decoded)

if __name__ == '__main__':
    unittest.main()