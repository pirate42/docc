# coding=utf-8



class Size(object):
    """Size encapsulate information for a Digital Ocean droplet size"""

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
        """Return the Size given an identifier and None if not found.

        :param service: The service object for the Digital Ocean account that holds the sizes
        :param identifier: The identifier for the size you are looking for
        """
        s = Size.sizes(service)
        for size in s:
            if size.id == identifier:
                return size
        return None


    @staticmethod
    def sizes(service):
        """Return the a list containing all the available droplet sizes.

        :param service: The service object for the Digital Ocean account that holds the sizes
        """
        response = service.get("sizes")
        encoded_sizes = response['sizes']
        result = []
        for encoded_size in encoded_sizes:
            s = Size(encoded_size['id'], encoded_size['name'])
            result.append(s)
        return result

