# coding=utf-8
import ez_setup

ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name='docc',
    version='0.0.2',
    packages=find_packages(),
    description='Digital Ocean Command Center',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    url='https://github.com/dsegonds/Docc',
    author='David Segonds',
    author_email='david@segonds.org',
    install_requires=['requests'],
    tests_require=['mock'],
    test_suite="tests"
)
