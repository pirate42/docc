# coding=utf-8

import requests
from requests.exceptions import ConnectionError


import docc.api.exceptions

class FakeService(object):
    def __init__(self,credentials):
        self.credentials = credentials

    def get(self, endpoint, parameters=None):
        raise docc.api.exceptions.ConnectionError("Connection to Digital Ocean failed.")
