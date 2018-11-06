# -*- coding: utf-8 -*-
"""
Various utility functions for PPPAT

"""
import socket


def is_online():
    """
    Return the online status (True or False).

    Returns
    -------
    status: Boolean
            The online status True is the IRFM database can be
            reached on the network. False if not ('offline' mode).
    """
    host = '10.8.86.1'  # deneb address
    port = 5880
    # create a dummy connection to test the server reachability
    try:
        s = socket.create_connection((host, port), timeout=2)
        return True
    except socket.error:
        return False
   