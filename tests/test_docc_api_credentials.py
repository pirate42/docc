# coding=utf-8
import unittest
from docc.api.credentials import Credentials

class TestCredentials(unittest.TestCase):
    def test___init__(self):
        client_id = "abc"
        api_key = "def"
        credentials = Credentials(client_id, api_key)
        assert credentials.client_id==client_id
        assert credentials.api_key==api_key


if __name__ == '__main__':
    unittest.main()