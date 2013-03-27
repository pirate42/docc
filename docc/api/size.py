# coding=utf-8

from docc.api.service import Service
from docc.api.cache import region


class Size(object):
    """Size encapsulate information for a Digital Ocean droplet size"""
    def __init__(self):
        self.id = None
        self.name = None


@region.cache_on_arguments()
def get(credentials,identifier):
    """Return the Size given an identifier and None if not found.

    :param credentials: The credentials for the Digital Ocean account
    :param identifier: The identifier for the size you are looking for
    """
    s = sizes(credentials)
    for size in s:
        if size.id == identifier:
            return size
    return None


def sizes(credentials):
    """Return the a list containing all the available droplet sizes.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    service = Service(credentials)
    response = service.get("sizes")
    encoded_sizes = response['sizes']
    result = []
    for encoded_size in encoded_sizes:
        s = Size()
        s.name = encoded_size['name']
        s.id = encoded_size['id']
        result.append(s)
    return result

