# coding=utf-8



class SSHKey(object):
    """Size encapsulate information for a Digital Ocean droplet size"""

    def __init__(self, identifier, name, public_key=None):
        self.id = identifier
        self.name = name
        self.public_key = public_key

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

