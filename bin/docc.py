# coding=utf-8

import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from docc.config import Configuration
import argparse


def main():
    """This is the main script for Docc"""
    parser = argparse.ArgumentParser(description='Interact with Digital Ocean.')

config = Configuration()

if __name__ == "__main__":
    main()