# coding=utf-8

"""Holds classes dealing with Digital Ocean account credentials"""


class Credentials(object):
    """This class holds the credentials (client_id, api_key) for a given Digital Ocean account"""

    def __init__(self, client_id, api_key):
        """Initialize the credentials by passing the Digital Ocean client_id and api_key

        :param client_id:
        :param api_key:
        """
        self.client_id = client_id
        self.api_key = api_key