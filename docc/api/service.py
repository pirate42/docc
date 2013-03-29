# coding=utf-8

import requests
from requests.exceptions import ConnectionError

URLBASE = 'api.digitalocean.com'

import docc.api.exceptions

class Service(object):
    def __init__(self,credentials):
        self.credentials = credentials

    def url(self,endpoint):
        """Returns the Digital Ocean URL for a given endpoint

        :param endpoint: The Digital Ocean API endpoint
        :raise docc.api.exceptions.ConnectionError if connection cannot be established.
        """
        return "https://%s/%s" % (URLBASE,endpoint)

    def get(self,endpoint,parameters=None):
        params = {}
        if parameters is not None:
            params = parameters
        params['client_id'] = self.credentials.client_id
        params['api_key'] = self.credentials.api_key

        try:
            r = requests.get(self.url(endpoint), params=params)
        except ConnectionError as e:
            raise docc.api.exceptions.ConnectionError("Connection to Digital Ocean failed.")

        content = r.json()
        if content['status'] != 'OK':
            raise docc.api.exceptions.APIError("Status: %s, Message: %s" % (content["status"], content["description"]))
        return content