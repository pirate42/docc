# coding=utf-8

"""This script allows you to interact with Digital Ocean API via the commaand line.
"""

from docc.config import Configuration
import argparse


def main():
    """Main function for the whole thing. Parse parameters and calls the appropriate command"""

    print "Docc -- Digital Ocean Command Center\n"

    params = parse_arguments()
    try:
        if params.command == 'config':
            config_command(params)
        else:
            raise Exception("Unknown command line command: '%s'" % params.command)
    except Exception as e:
        print "Error: %s" % e

def parse_arguments():
    """Create the argument parser and parse the command line parameters"""

    # Create the top-level parser
    parser = argparse.ArgumentParser(description="This script lets you interact with Digital Ocean")
    #parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='You need to use one of those commands', dest='command')

    # Create a parser for the config command
    parser_config = subparsers.add_parser('config', help='config let you modify your configuration file')
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

    return parser.parse_args()


def config_command(parameters):
    """Processes the config command that let the user set and retrieve configuration information"""
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
        assert False, "Something went wrong when parsing the parameters, I did not find any."

if __name__ == "__main__":
    main()
