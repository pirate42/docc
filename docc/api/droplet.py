# coding=utf-8

from docc.api.enum import enum
import docc.api.region
import docc.api.size
import docc.api.image

Statuses = enum(NEW='new', ACTIVE='active')


class Droplet(object):
    """A droplet encapsulates meta-information for a given droplet back at Digital Ocean"""

    def __init__(self, status, droplet_id, name, size, image, ip_address, region, backups):
        self.status = status
        self.id = droplet_id
        self.name = name
        self.size = size
        self.image = image
        self.ip_address = ip_address
        self.region = region
        self.backups = backups

    def __repr__(self):
        return "<%s: %s, %s, %s>" % (self.id, self.name, self.status, self.ip_address)

    def __str__(self):
        return "%s: %s, %s, %s" % (self.id, self.name, self.status, self.ip_address)


    @staticmethod
    def droplets(service):
        """Put all the droplets for the given account in a list

        :param service: The service instance for the Digital Ocean account that holds the droplets
        """
        response = service.get("droplets")
        encoded_droplets = response['droplets']
        result = []
        for encoded_droplet in encoded_droplets:
            size = docc.api.size.get(service, encoded_droplet['size_id'])
            image = docc.api.image.get(service, encoded_droplet['image_id'])
            region = docc.api.region.get(service, encoded_droplet['region_id'])
            backups = encoded_droplet['backups_active'] is not None
            status = Statuses.reverse_mapping[encoded_droplet['status']],

            droplet = Droplet(
                status=status,
                droplet_id=encoded_droplet['id'],
                name=encoded_droplet['name'],
                size=size,
                image=image,
                ip_address=encoded_droplet['ip_address'],
                region=region,
                backups=backups
            )
            result.append(droplet)
        return result