from distutils.core import setup

setup(
    name='Docc',
    version='0.0.1',
    packages=['docc','docc/test'],
    description='Digital Ocean Command Center',
    scripts=['bin/config.py'],
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    url='https://github.com/dsegonds/Docc',
    author='David Segonds',
    author_email='david@segonds.org',
)
