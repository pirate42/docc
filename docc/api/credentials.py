# coding=utf-8

"""Holds classes dealing with Digital Ocean account credentials"""


class Credentials(object):
    """This class holds the credentials (client_id, api_key) for a given Digital Ocean account"""
    def __init__(self,client_id,api_key):
        self.client_id = client_id
        self.api_key = api_key