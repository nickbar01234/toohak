import unittest
import serializer as s

class TestSerializer(unittest.TestCase):
    def test_encode_decode_connection(self):
        self.assertTrue(s.decode_connect(s.encode_connect_success()))

    def test_encode_decode_name(self):
        name = "Fredkin"
        self.assertEqual(name, s.decode_name(s.encode_name(name)))
    
    def test_encode_decode_connection_response(self):
        self.assertTrue(s.decode_response(s.encode_connect_success(), 'connect'))

if __name__ == '__main__':
    unittest.main()