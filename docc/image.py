# coding=utf-8

from docc.exceptions import APIError


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

    def destroy(self, service):
        """Destroy this image"""
        response = service.get("images/%s/destroy" % self.id)
        status = response['status']
        return status == 'OK'

    @staticmethod
    def get(service, identifier):
        """Return the Image given an identifier and None if not found.

        :param identifier: TODO
        :param service: The service object for the Digital Ocean account
        that holds the images
        """
        try:
            response = service.get('images/%s' % identifier)
        except APIError as e:
            return None

        encoded_image = response['image']
        i = Image(encoded_image['id'],
                  encoded_image['name'],
                  encoded_image['distribution']
        )

        return i


    @staticmethod
    def __images(service, my_filter=None):
        """Return the a list containing all the know images.

        :param service: The service object for the Digital Ocean account that
        holds the images
        :param my_filter: Should be absent, 'my_images', 'global'. If 'all'
        this will return all the images you have access to. 'my_images' will
        return the images you stored and 'global' the images available to all
        customers.
        """
        if my_filter is None:
            response = service.get("images")
        else:
            response = service.get("images", {'filter': my_filter})

        encoded_images = response['images']

        result = []
        for encoded_image in encoded_images:
            i = Image(encoded_image['id'], encoded_image['name'],
                      encoded_image['distribution'])
            result.append(i)
        return result

    @staticmethod
    def images(service):
        """Return all the known images included mine"""
        return Image.__images(service)

    @staticmethod
    def my_images(service):
        """Return my images"""
        return Image.__images(service, 'my_images')

    @staticmethod
    def global_images(service):
        """Return globally available images"""
        return Image.__images(service, 'global')