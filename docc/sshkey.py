# coding=utf-8


class SSHKey(object):
    """Size encapsulate information for a Digital Ocean droplet size"""

    def __init__(self, identifier, name, public_key=None):
        self.id = identifier
        self.name = name
        self.public = public_key

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

    def destroy(self, service):
        """Destroy this key

        :param service: The service object for the Digital Ocean account
        that holds the keys
        """
        response = service.get("ssh_keys/%s/destroy" % self.id)
        status = response['status']
        return status == 'OK'

    def details(self):
        return "Id: %s\nName: %s\nPublic key: %s" % (
            self.id,
            self.name,
            self.public
        )

    @staticmethod
    def get(service, identifier):
        """Return the Image given an identifier and None if not found.

        :param identifier: the identifier for the key we want to retrieve
        :param service: The service object for the Digital Ocean account
        that holds the keys
        """
        response = service.get('ssh_keys/%s' % identifier)
        encoded_image = response['ssh_key']
        i = SSHKey(
            encoded_image['id'],
            encoded_image['name'],
            encoded_image['ssh_pub_key']
        )

        return i

    @staticmethod
    def create(service, name, public):
        params = {
            'name': name,
            'ssh_pub_key': public,
        }
        response = service.get('ssh_keys/new', params)
        status = response['status']
        if status == 'OK':
            droplet_id = response['ssh_key']['id']
            return SSHKey.get(service, droplet_id)
        return None

    @staticmethod
    def keys(service):
        """Return the a list containing all the available SSH keys.

        :param service: The service object for the Digital Ocean account that
        holds the keys
        """
        response = service.get("ssh_keys")
        encoded_sizes = response['ssh_keys']
        result = []
        for encoded_size in encoded_sizes:
            s = SSHKey(encoded_size['id'], encoded_size['name'])
            result.append(s)
        return result
