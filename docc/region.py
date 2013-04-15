# coding=utf-8


class Region(object):
    """Region corresponds to a Digital Ocean data center"""

    def __init__(self, identifier, name):
        self.id = identifier
        self.name = name

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.name)

    def __str__(self):
        return "%s: %s" % (self.id, self.name)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self.__eq__(other)


    @staticmethod
    def get(service, identifier):
        """Return the Region given an identifier and None if not found.

        :param identifier: The identifier for the region you would like to
        retrieve
        :param service: The service object for the Digital Ocean account
        that holds the regions
        """
        r = Region.regions(service)
        for region in r:
            if region.id == identifier:
                return region

        return None

    @staticmethod
    def regions(service):
        """Return the a list containing all the regions.

        :param service: The service object for the Digital Ocean account
        that holds the regions
        """
        response = service.get("regions")
        encoded_regions = response['regions']
        result = []
        for encoded_region in encoded_regions:
            r = Region(encoded_region['id'], encoded_region['name'])
            result.append(r)
        return result
