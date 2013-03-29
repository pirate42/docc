# coding=utf-8



class Size(object):
    """Size encapsulate information for a Digital Ocean droplet size"""
    def __init__(self):
        self.id = None
        self.name = None


def get(service,identifier):
    """Return the Size given an identifier and None if not found.

    :param credentials: The credentials for the Digital Ocean account
    :param identifier: The identifier for the size you are looking for
    """
    s = sizes(service)
    for size in s:
        if size.id == identifier:
            return size
    return None


def sizes(service):
    """Return the a list containing all the available droplet sizes.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    response = service.get("sizes")
    encoded_sizes = response['sizes']
    result = []
    for encoded_size in encoded_sizes:
        s = Size()
        s.name = encoded_size['name']
        s.id = encoded_size['id']
        result.append(s)
    return result

