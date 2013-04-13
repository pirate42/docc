# coding=utf-8

import requests
from requests.exceptions import ConnectionError
from docc.api.exceptions import APIError

URLBASE = 'api.digitalocean.com'

import docc.api.exceptions


class Service(object):
    def __init__(self, credentials):
        self.credentials = credentials

    def __url(self, endpoint):
        return "https://%s/%s" % (URLBASE, endpoint)

    def get(self, endpoint, parameters=None):
        params = {}
        if parameters is not None:
            params = parameters
        params['client_id'] = self.credentials.client_id
        params['api_key'] = self.credentials.api_key

        try:
            r = requests.get(self.__url(endpoint), params=params)
        except ConnectionError:
            raise docc.api.exceptions.ConnectionError("Connection to Digital Ocean failed.")

        content = r.json()
        if content['status'] != 'OK':
            raise APIError("Status: %s, Message: %s" % (content["status"], content["description"]))
        return content