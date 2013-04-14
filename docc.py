# coding=utf-8

"""This script allows you to interact with Digital Ocean API via command line.
"""

import argparse

from docc.configuration import Configuration
from docc.api.credentials import Credentials
from docc.api.service import Service
from docc.api.droplet import Droplet
from docc.api.size import Size
from docc.api.region import Region
from docc.api.image import Image
from docc.api.exceptions import APIError


def main():
    """Main function for the whole thing. Parse parameters and calls the
    appropriate command
    """

    print "Docc -- Digital Ocean Command Center\n"

    params = parse_arguments()
    #try:
    if params.command == 'init':
        init_command(params)
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
    else:
        raise Exception("Unknown command line command: '%s'" % params.command)
        #except Exception as e:
        #    print "Error: %s" % e


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
    group.add_argument(
        '--get-all',
        help='get all key, value pairs from the configuration file',
        action='store_true'
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
        help='size let you manage Droplet Ocean images'
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

    return parser.parse_args()


def init_command(parameters):
    """Process the 'init' command that let use set credentials"""
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
    elif parameters.get_all:
        raise NotImplementedError("--get-all: Not yet implemented")
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
        config = Configuration()
        credentials = Credentials(config['client_id'], config['api_key'])
        service = Service(credentials)
        droplets = Droplet.droplets(service)
        print "Droplets:"
        for droplet in droplets:
            print "  - %s" % droplet
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


def size_command(parameters):
    """Process the 'size' command that let the user interact with available
    sizes
    :param parameters: TODO
    """

    if parameters.list:
        config = Configuration()
        credentials = Credentials(config['client_id'], config['api_key'])
        service = Service(credentials)
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
        config = Configuration()
        credentials = Credentials(config['client_id'], config['api_key'])
        service = Service(credentials)
        regions = Region.regions(service)
        print "Regions:"
        for region in regions:
            print "  - %s" % region
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


def image_command(parameters):
    """Process the 'image' command that let the user interact with available
    images
    :param parameters: TODO
    """

    if parameters.list:
        config = Configuration()
        credentials = Credentials(config['client_id'], config['api_key'])
        service = Service(credentials)
        images = Image.images(service, parameters.list)

        print "Images:"
        for image in images:
            print "  - %s" % image
    else:
        assert False, "Something went wrong when parsing the parameters, " \
                      "I did not find any."


if __name__ == "__main__":
    main()
