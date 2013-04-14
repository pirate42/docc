# coding=utf-8

class ConnectionError(Exception):
    pass


class APIError(Exception):
    """This is the general exception used when api call is unsuccessful"""
    pass


class CredentialsError(APIError):
    """This exception is raised when improper credentials are used"""
    pass