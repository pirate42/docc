# coding=utf-8


class ConnectionError(Exception):
    """This exception is raised whenever when are unable to connect to the
    Digital Ocean service API
    """
    pass


class APIError(Exception):
    """This is the general exception used when api call is unsuccessful"""
    pass


class CredentialsError(APIError):
    """This exception is raised when improper credentials are used"""
    pass