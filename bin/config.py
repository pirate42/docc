# coding=utf-8

"""This script allows you to modify the default configuration for docc
"""

import sys
import os
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from docc.config import Configuration
import argparse


def main():
    """Main function for this script"""
    parser = argparse.ArgumentParser(description='Interact with docc configuration file.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--set",
        help='set a key, value pair in the configuration file',
        nargs=2,
        metavar=('key', 'value')
    )
    group.add_argument(
        '--get',
        help='get a value given a key from the configuration file',
        nargs=1,
        metavar='key'
    )
    group.add_argument(
        '--get-all',
        help='returns all the know key, value pair in the configuration file'
    )

    parameters = parser.parse_args()
    print parameters
    config = Configuration()

    if parameters.get is not None:
        key = parameters.get[0]
        value = config[key]
        print "%s: %s" % (key, value)
    elif parameters.get_all is not None:
        pass
    elif parameters.set is not None:
        key = parameters.set[0]
        value = parameters.set[1]
        config[key] = value
        pass
    else:
        assert False, "Something went wrong when parsing the parameters, I did not find any."

    key_valid_values = ['client_id', 'api_key']


if __name__ == "__main__":
    main()