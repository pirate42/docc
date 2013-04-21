====
Docc
====

Docc stands for Digital Ocean Command Center and provides library
and scripts to manipulate Digital Ocean droplets, ssh keys, etc. 
via the provided API.

Typical usage of the API often looks like this::

    #!/usr/bin/env python

    from docc.credentials import Credentials
    from docc.service import Service
    from docc.droplet import Droplet

    client_id = '<put your client id here>'
    api_key = '<put your api key here>'

    credentials = Credentials(client_id, api_key)
    service = Service(credentials)

    droplet = Droplet.get(service, 152746)
    droplet.shutdown(service)

Typical usage of the script looks like::

    docc list droplets

    Docc -- Digital Ocean Command Center

    Droplets:
      - 152746: TestA, off, 198.199.73.143

Here is the result for 'docc --help' showing the commands available::

    usage: docc [-h] <command> ...
    
    This script lets you interact with Digital Ocean droplets and associated
    objects.
    
    optional arguments:
      -h, --help      show this help message and exit
    
    subcommands:
      Valid commands
    
      <command>       description
        init          a configuration file with credentials
        list          droplets, keys, regions, images, or sizes
        show          details for droplets, or SSH keys
        create        a new droplet, or a new SSH key
        shutdown      one or more droplets
        power_cycle   one or more droplets
        power_off     one or more droplets
        power_on      one or more droplets
        reboot        one or more droplets
        password_reset
                      one or more droplets
        resize        a given droplet
        snapshot      a given droplet
        restore       a droplet with the given snapshot
        rebuild       a droplet with the given default image
        backups       change backups status on a given droplet
        edit          existing SSH keys
        destroy       droplets, images, or SSH keys
    
