import unittest
from .validator import is_valid_ip


class TestIpAddress(unittest.TestCase):
    def test_valid_ip_address(self):
        self.assertTrue(is_valid_ip("192.167.1.14:5555"))

    def test_invalid_subnet(self):
        # Range must be between 0 and 255
        self.assertFalse(is_valid_ip("256.0.0.0:5555"))

    def test_invalid_format(self):
        # Must have 4-decimal numbers
        self.assertFalse(is_valid_ip("128.0.0:8000"))
