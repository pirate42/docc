# coding=utf-8


class Image(object):
    """Represent an Image object (name and distribution information)"""

    def __init__(self, identifier, name, distribution):
        self.id = identifier
        self.name = name
        self.distribution = distribution

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.name)

    def __str__(self):
        return "%s: %s, %s" % (self.id, self.name, self.distribution)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def get(service, identifier):
        """Return the Image given an identifier and None if not found.

        :param identifier: TODO
        :param service: The service object for the Digital Ocean account that holds the images
        """
        response = service.get('images/%s' % identifier)
        encoded_image = response['image']
        i = Image(encoded_image['id'],
                  encoded_image['name'],
                  encoded_image['distribution']
        )

        return i


    @staticmethod
    def images(service, filter):
        """Return the a list containing all the know images.

        :param service: The service object for the Digital Ocean account that
        holds the images
        :param filter: Should be one of 'all', 'my_images', 'global'. If 'all'
        this will return all the images you have access to. 'my_images' will
        return the images you stored and 'global' the images available to all
        customers.
        """
        params = {}
        allowed_values = ['all', 'my_images', 'global']
        if filter not in allowed_values:
            raise ValueError("my_filter should be one of %s" % allowed_values)
        if filter != 'all':
            params = {'filter': filter}

        response = service.get("images", params)
        encoded_images = response['images']

        result = []
        for encoded_image in encoded_images:
            i = Image(encoded_image['id'], encoded_image['name'], encoded_image['distribution'])
            result.append(i)
        return result

