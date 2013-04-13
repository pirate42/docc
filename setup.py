# coding=utf-8
from setuptools import setup

setup(
    name='Docc',
    version='0.0.1',
    packages=['docc', 'tests'],
    description='Digital Ocean Command Center',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    url='https://github.com/dsegonds/Docc',
    author='David Segonds',
    author_email='david@segonds.org',
    install_requires=['requests'],
    tests_require=['mock']
)
