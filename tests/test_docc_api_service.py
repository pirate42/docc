# coding=utf-8
import unittest

from mock import MagicMock
import requests

from docc.credentials import Credentials
from docc.service import Service
from docc.exceptions import APIError, ConnectionError


class TestService(unittest.TestCase):
    def test___init__(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        self.assertEquals(service.credentials, credentials)


    def test_get(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)

        class Response(object):
            def __init__(self, response):
                self.response = response

            def json(self):
                return self.response

        # Test where requests.get returns something with status: OK
        response = {'status': 'OK'}
        mock = MagicMock(return_value=Response(response))
        requests.get = mock
        self.assertEquals(service.get("test"), response)

        # Test where requests.get returns something with status: OK
        response = {
            "status": "ERROR",
            "description": "Unable to verify credentials. #414LB"
        }
        mock = MagicMock(return_value=Response(response))
        requests.get = mock
        with self.assertRaises(APIError):
            service.get("test")

        # Test where requests.get cannot connect
        mock = MagicMock(side_effect=requests.ConnectionError)
        requests.get = mock
        with self.assertRaises(ConnectionError):
            service.get("test")

        # Test where requests.get returns something different from status: OK
        response = {
            "status": "ERROR",
            "description": "Unable to verify credentials. #414LB"
        }
        mock = MagicMock(return_value=Response(response))
        requests.get = mock
        with self.assertRaises(APIError):
            service.get("test")


if __name__ == '__main__':
    unittest.main()
