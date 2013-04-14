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
        elif params.command == 'config':
            config_command(params)
        elif params.command == 'droplet':
            droplet_command(params)
        elif params.command == 'size':
            size_command(params)
        elif params.command == 'region':
            region_command(params)
        elif params.command == 'image':
            image_command(params)
        elif params.command == 'sshkey':
            sshkey_command(params)
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
    parser = argparse.ArgumentParser(
        description="This script lets you interact with Digital Ocean"
    )
    subparsers = parser.add_subparsers(
        help='You need to use one of those commands', dest='command'
    )

    # Create a parser for the 'init' command
    subparsers.add_parser(
        'init', help='init let you create a configuration file and initialize'
                     ' credentials'
    )

    # Create a parser for the 'config' command
    parser_config = subparsers.add_parser(
        'config', help='config let you modify your configuration file'
    )
    group = parser_config.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--set",
        help='set a key, value pair in the configuration file',
        nargs=2,
        metavar=('KEY', 'VALUE')
    )
    group.add_argument(
        '--get',
        help='get a value given a key from the configuration file',
        nargs=1,
        metavar='KEY'
    )

    # Create a parser for the 'droplet' command
    parser_droplet = subparsers.add_parser(
        'droplet',
        help='droplet let you manage your droplets'
    )
    group = parser_droplet.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--list',
        help='list all your droplets',
        action='store_true',
    )
    group.add_argument(
        '--shutdown',
        help='shutdown the droplet corresponding to the given id',
        metavar='ID'
    )
    group.add_argument(
        '--reboot',
        help='reboot the droplet corresponding to the given id',
        metavar='ID'
    )
    group.add_argument(
        '--on',
        help='power on the droplet corresponding to the given id',
        metavar='ID'
    )
    group.add_argument(
        '--off',
        help='power off the droplet corresponding to the given id',
        metavar='ID'
    )
    group.add_argument(
        '--destroy',
        help='destroy the droplet corresponding to the given id',
        metavar='ID'
    )

    # Create a parser for the 'size' command
    parser_size = subparsers.add_parser(
        'size',
        help='size let you manage Droplet Ocean sizes'
    )
    group = parser_size.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--list',
        help='list all available sizes',
        action='store_true'
    )

    # Create a parser for the 'image' command
    parser_image = subparsers.add_parser(
        'image',
        help='image let you manage Droplet Ocean images'
    )
    group = parser_image.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--list',
        help="list available images using filter 'all', "
             "'my_images', or 'global')",
        choices=['all', 'my_images', 'global'],
        metavar="FILTER",
    )

    # Create a parser for the 'region' command
    parser_region = subparsers.add_parser(
        'region',
        help='region let you manage Droplet Ocean regions'
    )
    group = parser_region.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--list',
        help='list all available regions',
        action='store_true'
    )

    # Create a parser for the 'sshkey' command
    parser_ssh_keys = subparsers.add_parser(
        'sshkey',
        help='sshkey let you manage Droplet Ocean SSH keys'
    )
    group = parser_ssh_keys.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--list',
        help='list all available SSH keys',
        action='store_true'
    )

    return parser.parse_args()


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


def config_command(parameters):
    """Process the 'config' command that let user set and retrieve
    configuration information

    :param parameters: TODO
    """
    config = Configuration()

    if parameters.get is not None:
        key = parameters.get[0]
        value = config[key]
        print "%s: %s" % (key, value)
    elif parameters.set is not None:
        key = parameters.set[0]
        value = parameters.set[1]
        config[key] = value
        print "%s: %s" % (key, config[key])
    else:
        assert False, \
            "Something went wrong when parsing the parameters, " \
            "I did not find any."


def droplet_command(parameters):
    """Process the 'droplet' command that let the user interact with its
    droplets

    :param parameters:TODO
    """

    if parameters.list:
        service = get_service()
        droplets = Droplet.droplets(service)
        print "Droplets:"
        for droplet in droplets:
            print "  - %s" % droplet
    elif parameters.shutdown:
        droplet_id = parameters.shutdown
        service = get_service()
        droplet = Droplet.get(service, droplet_id)
        result = droplet.shutdown(service)
        if result:
            print "Shutdown of droplet %s was successful" % droplet_id
        else:
            print "Unable to shutdown droplet %s" % droplet_id
    elif parameters.reboot:
        droplet_id = parameters.reboot
        service = get_service()
        droplet = Droplet.get(service, droplet_id)
        result = droplet.reboot(service)
        if result:
            print "Reboot of droplet %s was successful" % droplet_id
        else:
            print "Unable to reboot droplet %s" % droplet_id
    elif parameters.on:
        droplet_id = parameters.on
        service = get_service()
        droplet = Droplet.get(service, droplet_id)
        result = droplet.power_on(service)
        if result:
            print "Power on of droplet %s was successful" % droplet_id
        else:
            print "Unable to power on droplet %s" % droplet_id
    elif parameters.off:
        droplet_id = parameters.off
        service = get_service()
        droplet = Droplet.get(service, droplet_id)
        result = droplet.power_off(service)
        if result:
            print "Power off of droplet %s was successful" % droplet_id
        else:
            print "Unable to power off droplet %s" % droplet_id
    elif parameters.destroy:
        droplet_id = parameters.destroy
        service = get_service()
        droplet = Droplet.get(service, droplet_id)
        result = droplet.destroy(service)
        if result:
            print "Droplet %s was successful destroyed" % droplet_id
        else:
            print "Unable to destroy droplet %s" % droplet_id
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


def size_command(parameters):
    """Process the 'size' command that let the user interact with available
    sizes
    :param parameters: TODO
    """

    if parameters.list:
        service = get_service()
        sizes = Size.sizes(service)
        print "Sizes:"
        for size in sizes:
            print "  - %s" % size
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


def region_command(parameters):
    """Process the 'region' command that let the user interact with available
    regions
    :param parameters: TODO
    """

    if parameters.list:
        service = get_service()
        regions = Region.regions(service)
        print "Regions:"
        for region in regions:
            print "  - %s" % region
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


def sshkey_command(parameters):
    """Process the 'sshkey' command that let the user interact with available
    SSH keys
    :param parameters: TODO
    """

    if parameters.list:
        service = get_service()
        keys = SSHKey.keys(service)
        print "SSH Keys:"
        for key in keys:
            print "  - %s" % key
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


def image_command(parameters):
    """Process the 'image' command that let the user interact with available
    images
    :param parameters: TODO
    """

    if parameters.list:
        service = get_service()
        images = Image.images(service, parameters.list)

        print "Images:"
        for image in images:
            print "  - %s" % image
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


if __name__ == "__main__":
    main()
