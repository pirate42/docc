# coding=utf-8

from docc.api.service import Service
from docc.api.enum import enum
from docc.api.cache import region


class Image(object):
    """Represent an Image object (name and distribution information)"""
    def __init__(self):
        self.id = None
        self.name = None
        self.distribution = None

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.name)

    def __str__(self):
        return "%s: %s, %s" % (self.id, self.name, self.distribution)


@region.cache_on_arguments()
def get(credentials,identifier):
    """Return the Image given an identifier and None if not found.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    """
    service = Service(credentials)
    response = service.get('images/%s' % identifier)
    encoded_image = response['image']
    i = Image()
    i.name = encoded_image['name']
    i.id = encoded_image['id']
    i.distribution = encoded_image['distribution']

    return i


@region.cache_on_arguments()
def images(credentials, filter):
    """Return the a list containing all the know images.

    :param credentials: The credentials for the Digital Ocean account that holds the droplets
    :param only_my_images: If set to True, the method will only return owned images otherwise all images
    """
    service = Service(credentials)
    params = {'filter': filter}
    if filter == 'mine':
        params = {'filter': 'my_images'}

    if filter == 'all':
        return images(credentials, 'global') + images(credentials, 'mine')

    response = service.get("images",params)
    encoded_images = response['images']

    result = []
    for encoded_image in encoded_images:
        i = Image()
        i.name = encoded_image['name']
        i.id = encoded_image['id']
        i.distribution = encoded_image['distribution']
        result.append(i)
    return result

