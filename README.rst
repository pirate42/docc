====
Docc
====

Docc stands for Digital Ocean Command Center and provides library
and scripts to manipulate Digital Ocean droplets, ssh keys, etc. 
via the provided API.

Typical usage of the often looks like this::

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

Typical usage of the script looks like:

    docc list droplets

    Docc -- Digital Ocean Command Center

    Droplets:
      - 152746: TestA, off, 198.199.73.143, 512MB

