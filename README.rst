====
Docc
====

Docc stands for Digital Ocean Command Center and provides library
and scripts to manipulate Digital Ocean droplets, ssh keys, etc. 
via their provided API.

Typical usage often looks like this::

    #!/usr/bin/env python

    from docc import location
    from towelstuff import utils

    if utils.has_towel():
        print "Your towel is located:", location.where_is_my_towel()

(Note the double-colon and 4-space indent formatting above.)
