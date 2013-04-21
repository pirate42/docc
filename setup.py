#!/usr/bin/env python
# coding=utf-8
from setuptools import setup
from docc import __version__

setup(
    name='docc',
    version=__version__,
    packages=['docc'],
    scripts=['bin/docc'],
    description='Digital Ocean Command Center',
    keywords='digital ocean droplet',
    long_description=open('README.rst').read(),
    license=open('LICENSE.txt').read(),
    url='https://github.com/dsegonds/docc',
    download_url='https://pypi.python.org/packages/source/d/docc/docc-%s.tar'
                 '.gz' % __version__,
    author='David Segonds',
    author_email='"David Segonds" <david@segonds.org>',
    install_requires=['requests'],
    tests_require=['mock'],
    test_suite="tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration'
    ],
)
