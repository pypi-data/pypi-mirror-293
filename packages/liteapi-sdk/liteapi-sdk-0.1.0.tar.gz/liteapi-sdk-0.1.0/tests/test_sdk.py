# tests/test_sdk.py
import unittest
from liteapi.sdk import LiteApi

class TestLiteApi(unittest.TestCase):

    def setUp(self):
        self.api_key = "dummy_api_key"
        self.api = LiteApi(self.api_key)

    def test_initialization(self):
        self.assertEqual(self.api.api_key, self.api_key)

    def test_get_full_rates(self):
        # Mock the requests.post method
        # to return a predetermined response
        pass  # Replace with actual test code

if __name__ == '__main__':
    unittest.main()