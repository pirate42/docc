# coding=utf-8
"""This file contains the Configuration class that is used to pull
information stored on disk between invocations.
"""
import os
from ConfigParser import RawConfigParser, NoOptionError


class Configuration(object):
    """To load and use configuration file."""
    _config = None
    _location = None
    _section = "global"  # Right now, this is the only section

    def __init__(self, location=None):
        """Initialize the Configuration class

        :type self: object
        :param location: The configuration file location. If None is used,
        then $HOME/.docc will be used.
        """

        if location is None:
            self._location = os.path.expanduser("~/.docc")
        else:
            self._location = location

        self._config = RawConfigParser()
        self._config.read(self._location)

    def __getitem__(self, key):
        """Returns the value for the given key"""
        if not self._config.has_section(self._section):
            self._config.add_section(self._section)
        try:
            return self._config.get(self._section, key)
        except NoOptionError:
            raise KeyError(
                "%s is not a valid key in the configuration file" %
                key
            )

    def __setitem__(self, key, value):
        """Set the key, value pair in the configuration and save to disk.

        Authorized keys are api_key, client_id
        """

        # Create the default section if it is missing.
        if not self._config.has_section(self._section):
            self._config.add_section(self._section)
        self._config.set(self._section, key, value)

        # If the file exists, don't touch it as the user
        # may have decided on a different set of permissions
        set_permission = False
        location = self._location
        if os.path.exists(location):
            set_permission = True

        with open(location, "w") as f:
            self._config.write(f)

        if set_permission:
            os.chmod(location, 0600)