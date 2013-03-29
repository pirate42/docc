# coding=utf-8



class Region(object):
    """Region corresponds to a Digital Ocean data center"""
    def __init__(self):
        self.id = None
        self.name = None

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.name)

    def __str__(self):
        return "%s: %s" % (self.id, self.name)


def get(service, identifier):
    """Return the Region given an identifier and None if not found.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    r = regions(service)
    for region in r:
        if region.id == identifier:
            return region

    return None

def regions(service):
    """Return the a list containing all the regions.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    response = service.get("regions")
    encoded_regions = response['regions']
    result = []
    for encoded_region in encoded_regions:
        r = Region()
        r.name = encoded_region['name']
        r.id = encoded_region['id']
        result.append(r)
    return result
