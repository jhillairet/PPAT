# -*- coding: utf-8 -*-
"""
Various utility functions for PPPAT

"""
from contextlib import contextmanager
from qtpy.QtWidgets import QApplication
from qtpy.QtGui import QCursor
from qtpy.QtCore import Qt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils_west import is_online
from pywed import PyWEDException

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
                except PyWEDException as e:
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
