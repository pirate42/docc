# coding=utf-8
"""This file contains the Configuration class that is used to pulled information stored on disk between invocations.
"""
import os
import ConfigParser


class Configuration(object):
    """To load and use configuration file."""
    _config = None
    _location = None
    _section = "global"  # Right now, there is only one section in the configuration file.

    def __init__(self, location=None):
        """Initialize the Configuration class

        :type self: object
        :param location: The configuration file location. If None is used, then $HOME/.docc will be used.
        """

        if location is None:
            self._location = os.path.expanduser("~/.docc")
        else:
            self._location = location

        self._config = ConfigParser.RawConfigParser()
        self._config.read(self._location)

    def __getitem__(self, key):
        """Returns the value for the given key"""
        return self._config.get(self._section,key)

    def __setitem__(self, key, value):
        """Set the key, value pair in the configuration and save to disk.

        Authorized keys are api_key, client_id
        """
        valid_values = ['api_key', 'client_id']
        if key not in valid_values:
            raise ValueError("Given key '%s' is not in %s" % (key,valid_values))
        self._config.set(self._section,key,value)
        with open(self._location,"w") as f:
            self._config.write(f)
