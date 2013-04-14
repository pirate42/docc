# coding=utf-8

"""This script allows you to interact with Digital Ocean API via command line.
"""

import argparse
import sys

from docc.configuration import Configuration
from docc.api.credentials import Credentials
from docc.api.service import Service
from docc.api.droplet import Droplet
from docc.api.size import Size
from docc.api.region import Region
from docc.api.image import Image
from docc.api.sshkey import SSHKey
from docc.api.exceptions import CredentialsError, APIError


def main():
    """Main function for the whole thing. Parse parameters and calls the
    appropriate command
    """

    print "Docc -- Digital Ocean Command Center\n"

    params = parse_arguments()
    try:
        if params.command == 'init':
            init_command()
        elif params.command == 'list':
            list_command(params)
        elif params.command == 'destroy':
            destroy_command(params)
        elif (  params.command == 'shutdown' or
                        params.command == 'power_off' or
                        params.command == 'power_on' or
                        params.command == 'power_cycle' or
                        params.command == 'reboot' ):
            droplet_operation(params)
        else:
            raise Exception(
                "Unknown command line command: '%s'" % params.command)
    except CredentialsError as e:
        print "Error: %s." % e
    except APIError as e:
        print "Error: %s." % e


def parse_arguments():
    """Create the argument parser and parse the command line parameters"""

    # Create the top-level parser
    main_parser = argparse.ArgumentParser(
        description="This script lets you interact with Digital Ocean "
                    "droplets and associated objects."
    )
    command_parsers = main_parser.add_subparsers(
        help='commands:', dest='command'
    )

    # Create a parser for the 'init' command
    command_parsers.add_parser(
        'init', help='a configuration file with credentials'
    )

    # Create a parser for the 'list' command
    parser_list = command_parsers.add_parser(
        'list',
        help='different Digital Ocean objects'
    )
    list_command_parsers = parser_list.add_subparsers(
        dest='type'
    )
    for object_type, description in [
        ('droplets', 'droplets'),
        ('regions', 'regions'),
        ('sizes', 'sizes'),
        ('images', 'all images'),
        ('my_images', 'my images'),
        ('global_images', 'global images'),
        ('keys', 'SSH keys')
    ]:
        list_command_parsers.add_parser(
            object_type,
            help="list %s" % description
        )

    # Parsers for different operations on droplets
    for operation in [
        'shutdown',
        'power_cycle',
        'power_off',
        'power_on',
        'reboot'
    ]:
        local_parser = command_parsers.add_parser(
            operation,
            help='one or more droplets given identifiers'
        )
        local_parser.add_argument('ids', metavar='ID', type=int, nargs='+')

    # Create a parser for the 'destroy' command
    parser_destroy = command_parsers.add_parser(
        'destroy',
        help='different Digital Ocean objects'
    )
    destroy_command_parsers = parser_destroy.add_subparsers(
        dest='type'
    )
    for object_type, description in [
        ('droplet', 'droplets'),
        ('image', 'images'),
        ('key', 'keys')
    ]:
        local_parser = destroy_command_parsers.add_parser(
            object_type,
            help='destroy %s given list of identifiers' % description
        )
        local_parser.add_argument('ids', metavar='ID', type=int, nargs="+")

    return main_parser.parse_args()


def get_service():
    """Return a valid service

    Return a valid service initialized with credentials contained in the
    configuration file.
    """
    try:
        config = Configuration()
        credentials = Credentials(config['client_id'], config['api_key'])
        return Service(credentials)
    except KeyError:
        print "Unable to retrieve credentials. Did you use 'init' command?"
        sys.exit(1)


def init_command():
    """Process the 'init' command that let use set credentials
    """
    configuration = Configuration()
    print "Retrieve 'Client Key' and 'API Key' from " \
          "https://www.digitalocean.com/api_access and enter them below." \
          " They will be stored in %s\n" % configuration._location
    client_id = raw_input("Client Key: ")
    api_key = raw_input("API Key: ")

    # Verify configuration
    credentials = Credentials(client_id, api_key)
    service = Service(credentials)
    try:
        service.get('droplets')
        configuration['client_id'] = client_id
        configuration['api_key'] = api_key
    except APIError:
        print "Unable to connect to Digital Ocean. Not storing credentials."
        sys.exit(1)


def list_command(parameters):
    service = get_service()

    def list_objects(p):
        (my_callable, title) = p
        print title + ":"
        objects = my_callable(service)
        if not objects:
            print "  None found"
        for one_object in objects:
            print "  - %s" % one_object

    list_objects(
        {
            'droplets': (Droplet.droplets, "Droplets"),
            'sizes': (Size.sizes, "Sizes"),
            'regions': (Region.regions, "Regions"),
            'keys': (SSHKey.keys, "SSH Keys"),
            'images': (Image.images, "All Images"),
            'my_images': (Image.my_images, "My Images"),
            'global_images': (Image.global_images, "Global Images"),
        }[parameters.type]
    )


def droplet_operation(parameters):
    service = get_service()
    operation = parameters.command
    for droplet_id in parameters.ids:
        droplet = Droplet.get(service, droplet_id)
        method_to_call = getattr(droplet, operation)
        result = method_to_call(service)
        if result:
            print "'%s' operation on droplet %s was successful" % \
                  (operation, droplet_id)
        else:
            print "'%s' operation on droplet %s failed" % \
                  (operation, droplet_id)


def destroy_command(parameters):
    """Process the 'destroy' command for different objects and identifiers"""
    service = get_service()
    identifiers = parameters.ids

    def destroy_objects(p):
        (my_callable, title) = p
        for i in identifiers:
            my_object = my_callable.get(service, i)
            result = my_object.destroy(service)
            if result:
                print "%s %s destroyed" % \
                      (title, i)
            else:
                print "%s %s NOT destroyed" % \
                      (title, i)

    destroy_objects(
        {
            'droplet': (Droplet, "Droplet"),
            'image': (Image, "Image"),
            'key': ( SSHKey, "SSH Key"),
        }[parameters.type]
    )


if __name__ == "__main__":
    main()
