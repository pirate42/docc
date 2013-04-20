# coding=utf-8

import requests
from requests.exceptions import ConnectionError
import exceptions

URLBASE = 'api.digitalocean.com'


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
            raise exceptions.ConnectionError(
                "Connection to Digital Ocean failed.")

        if not r.ok:
            raise exceptions.APIError(
                "Status: %s, Reason: %s" % (
                    r.status_code,
                    r.reason
                )
            )

        content = r.json()
        status = content['status']
        if status != 'OK':
            if 'description' in content:
                description = content["description"]
                if "Unable to verify credentials" in description:
                    raise exceptions.CredentialsError(
                        "Status: %s, Message: %s" %
                        (status, description)
                    )

                raise exceptions.APIError(
                    "Status: %s, Message: %s" %
                    (status, description)
                )
            error_message = content['error_message']
            raise exceptions.APIError(
                "Status: %s, Message: %s" %
                (status, error_message)
            )

        return content