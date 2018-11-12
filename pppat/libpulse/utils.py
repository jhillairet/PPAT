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

from pppat.libpulse.check_result import CheckResult as Result
import pywed as pw

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


def post_pulse_test(test_func):
    '''
    Decorator for Post-Pulse tests.

    This decorator should be used as a convenient way to avoid error detection
    code in post test functions.

    This decorator change the GUI cursor to indicate the user that work
    is going on under the hood.
    Then, it runs the test function only if the database is accessible.
    Finally, it return all the possible errors into the test object.
    '''
    def wrapper(*args, **kwargs):
        # change the GUI cursor to show the user that something is going on...
        with wait_cursor():
            # only perform the test if we have access to the database
            if is_online():
                try:
                    # perform the test
                    test = test_func(*args, **kwargs)
                except ValueError as e:
                    # problem with manipulating the data (our fault!)
                    args[0].text = str(e)
                    args[0].code = Result.BROKEN
                    test = args[0]
                except pw.PyWEDException as e:
                    # problem to get the data from database (not our fault!)
                    args[0].text = str(e)
                    args[0].code = Result.UNAVAILABLE
                    test = args[0]
            else:
                args[0].text = 'Cannot access WEST database.'
                args[0].code = Result.UNAVAILABLE
                test = args[0]
            return test
    return wrapper
