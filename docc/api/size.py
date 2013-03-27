# coding=utf-8

from docc.api.service import Service

class Region(object):
    def __init__(self,identifier,description):
        self.id = identifier
        self.description = description


    @staticmethod
    def get(credentials,identifier):
        """Return the Region given an identifier and None if not found.

        :param credentials: The credentials for the Digital Ocean account that holds the droplets
        """
        regions = self.regions(credentials)
        for region in regions:
            if region.id == identifier:
                return region

        return None

    @staticmethod
    def regions(credentials):
        """Return the a list containing all the regions.

        :param credentials: The credentials for the Digital Ocean account that holds the droplets
        """
        service = Service(credentials)
        response = service.get("regions")
        print response
        encoded_regions = response['regions']
        print encoded_regions

