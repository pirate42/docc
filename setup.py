#!/usr/bin/env python
# coding=utf-8
from setuptools import setup

VERSION = "0.0.2"

setup(
    name='docc',
    version=VERSION,
    packages=['docc'],
    scripts=['bin/docc'],
    description='Digital Ocean Command Center',
    keywords='digital ocean droplet',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    url='https://github.com/dsegonds/Docc',
    author='David Segonds',
    author_email='david@segonds.org',
    install_requires=['requests'],
    tests_require=['mock'],
    test_suite="tests",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public '
        'License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing'
    ],
)
