# coding=utf-8

from region import Region
from size import Size
from image import Image


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

    def details(self):
        fields = [
            ("Id", self.id),
            ("Name", self.name),
            ("Size", self.size),
            ("Image", self.image),
            ("IP Address", self.ip_address),
            ("Region", self.region),
            ("Backups", self.backups),
            ("Status", self.status)
        ]
        result = ""
        sep = ""
        for i in fields:
            result = result + sep + "%s: %s" % i
            sep = "\n"
        return result

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
    def create(service, name, size_id, image_id, region_id, keys=None):
        params = {
            'name': name,
            'size_id': size_id,
            'image_id': image_id,
            'region_id': region_id,
        }
        if keys is not None and keys:
            params['ssh_key_ids'] = \
                reduce(lambda x, y: str(x) + ',' + str(y), keys)
        response = service.get('droplets/new', params)
        status = response['status']
        if status == 'OK':
            droplet_id = response['droplet']['id']
            return Droplet.get(service, droplet_id)
        return None


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

    def password_reset(self, service):
        """Reset root password on this droplet"""
        response = service.get("droplets/%s/password_reset" % self.id)
        status = response['status']
        return status == 'OK'

    def resize(self, service, size_id):
        """Resize this droplet

        :param size_id: is the id for the size object you want to use
        """
        params = {
            'size_id': size_id,
        }
        response = service.get("droplets/%s/resize" % self.id, params)
        status = response['status']
        return status == 'OK'

    def restore(self, service, image_id):
        """Restore this droplet to the given image

        :param image_id: is the id for the image object you want to use
        """
        params = {
            'image_id': image_id,
        }
        response = service.get("droplets/%s/restore" % self.id, params)
        status = response['status']
        return status == 'OK'


    def set_backups(self, service, state):
        """Enable or disable backups on a this droplet

        :param state: The boolean use to set the backups state
        """
        verb = 'disable'
        if state:
            verb = 'enable'
        response = service.get("droplets/%s/%s_backups" % (self.id, verb))
        status = response['status']
        return status == 'OK'


    def rebuild(self, service, image_id):
        """Rebuild this droplet with the given image

        :param image_id: is the id for the image object you want to use
        """
        params = {
            'image_id': image_id,
        }
        response = service.get("droplets/%s/rebuild" % self.id, params)
        status = response['status']
        return status == 'OK'

    def snapshot(self, service, name=None):
        """Take a snapshot image of this droplet

        :param name: is an optional name for the snapshot
        """
        params = {}
        if name is not None:
            params = {
                'name': name
            }
        response = service.get("droplets/%s/snapshot" % self.id, params)
        status = response['status']
        return status == 'OK'

    def destroy(self, service):
        """Destroy this droplet"""
        response = service.get("droplets/%s/destroy" % self.id)
        status = response['status']
        return status == 'OK'
