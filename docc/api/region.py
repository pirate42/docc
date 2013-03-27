# coding=utf-8

from docc.api.service import Service
from docc.api.cache import region


class Region(object):
    """Region corresponds to a Digital Ocean data center"""
    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.name)

    def __str__(self):
        return "%s: %s" % (self.id, self.name)


@region.cache_on_arguments()
def get(credentials, identifier):
    """Return the Region given an identifier and None if not found.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    r = regions(credentials)
    for region in r:
        if region.id == identifier:
            return region

    return None

@region.cache_on_arguments()
def regions(credentials):
    """Return the a list containing all the regions.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    service = Service(credentials)
    response = service.get("regions")
    encoded_regions = response['regions']
    result = []
    for encoded_region in encoded_regions:
        r = Region()
        r.name = encoded_region['name']
        r.id = encoded_region['id']
        result.append(r)
    return result
