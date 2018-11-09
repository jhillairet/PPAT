# -*- coding: utf-8 -*-
"""
Various utility functions for PPPAT

"""
import socket
from contextlib import contextmanager
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QCursor
from qtpy.QtCore import Qt
from IRFMtb import tsdernier_choc

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


@contextmanager
def wait_cursor():
    """
    Change the mouse cursor into a waiting cursor during a task.

    This context manager should like : "with wait_cursor():"
    """
    try:
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        yield
    finally:
        QApplication.restoreOverrideCursor()


def last_pulse_nb():
    """ Return the latest WEST pulse number """
    if is_online():
        return tsdernier_choc()
    else:
        return -1