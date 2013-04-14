# coding=utf-8

from docc.api.region import Region
from docc.api.size import Size
from docc.api.image import Image


class Status(object):
    """A status represents the current status for a given droplet"""
    NEW = "new"
    ACTIVE = "active"
    OFF = "off"


class Droplet(object):
    """A droplet encapsulates meta-information for a given droplet.
    """

    def __init__(self, status, droplet_id, name, size, image, ip_address,
                 region, backups):
        self.status = status
        self.id = droplet_id
        self.name = name
        self.size = size
        self.image = image
        self.ip_address = ip_address
        self.region = region
        self.backups = backups

    def __repr__(self):
        return "<%s: %s, %s, %s>" % (
            self.id, self.name, self.status, self.ip_address)

    def __str__(self):
        return "%s: %s, %s, %s" % (
            self.id, self.name, self.status, self.ip_address)


    @staticmethod
    def get(service, droplet_id):
        """Return the Droplet given an identifier and None if not found.

        :param droplet_id: The identifier for the droplet you want to retrieve
        :param service: The service object for the Digital Ocean account
        that holds the droplets
        """
        response = service.get('droplets/%s' % droplet_id)
        encoded_droplet = response['droplet']
        return Droplet.__from_encoded(service, encoded_droplet)


    @staticmethod
    def __from_encoded(service, encoded_droplet):
        size = Size.get(service, encoded_droplet['size_id'])
        image = Image.get(service, encoded_droplet['image_id'])
        region = Region.get(service, encoded_droplet['region_id'])
        backups = encoded_droplet['backups_active'] is not None
        status = encoded_droplet['status']

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
        return droplet

    @staticmethod
    def droplets(service):
        """Put all the droplets for the given account in a list

        :param service: The service object for the Digital Ocean account
        that holds the droplets
        """
        response = service.get("droplets")
        encoded_droplets = response['droplets']
        result = []
        for encoded_droplet in encoded_droplets:
            droplet = Droplet.__from_encoded(service, encoded_droplet)
            result.append(droplet)
        return result

    def shutdown(self, service):
        """Shutdown this droplet"""
        response = service.get("droplets/%s/shutdown" % self.id)
        status = response['status']
        return status == 'OK'

    def reboot(self, service):
        """Reboot this droplet"""
        response = service.get("droplets/%s/reboot" % self.id)
        status = response['status']
        return status == 'OK'

    def power_cycle(self, service):
        """Power-cycle this droplet"""
        response = service.get("droplets/%s/power_cycle" % self.id)
        status = response['status']
        return status == 'OK'

    def power_on(self, service):
        """Power on this droplet"""
        response = service.get("droplets/%s/power_on" % self.id)
        status = response['status']
        return status == 'OK'

    def power_off(self, service):
        """Power off this droplet"""
        response = service.get("droplets/%s/power_off" % self.id)
        status = response['status']
        return status == 'OK'