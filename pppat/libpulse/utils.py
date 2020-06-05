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
from pywed import PyWEDException, tsmat

from sys import exc_info  # for debug
import linecache  # for debug 
import logging  # pour ajouter des informations au log de PPPPAT
import sys, os   
logger = logging.getLogger(__name__)

# Top parameters
AUTORISATION_LHCD = 'EXP=T=S;Autorisation;ChocLHCD'  # 1 or 0
AUTORISATION_ICRH = 'EXP=T=S;Autorisation;ChocICRH'  # 1 or 0

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


class HiddenPrints:
    """
    Hide temporarly the standard output ('print()' commands but not logs)
    
    From example given in 
    https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python

    To be use with a with statement:
    
    Example
    -------
    with HiddenPrints():
        print('this print is not visible')
    print('this print is visible')
    
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


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
                    logger.error(str(e))
                except PyWEDException as e:
                    # problem to get the data from database (not our fault!)
                    args[0].text = str(e)
                    args[0].code = Result.UNAVAILABLE
                    test = args[0]
                    logger.error(str(e))
                except Exception as e:
                    # any other problem 
                    args[0].text = str(e)
                    args[0].code = Result.UNAVAILABLE
                    test = args[0]     
                    logger.error(str(e))
            else:
                args[0].text = 'Cannot access WEST database.'
                args[0].code = Result.UNAVAILABLE
                test = args[0]
                logger.error(args[0].text)
            return test
    return wrapper

def pre_pulse_test(test_func):
    '''
    Decorator for Pre-Pulse tests.

    This decorator should be used as a convenient way to avoid error detection
    code in pre test functions.

    This decorator returns a Result object with all the possible errors 
    into the test object.
    '''
    def wrapper(*args, **kwargs):
        # change the GUI cursor to show the user that something is going on...
        with wait_cursor():
            try:
                # perform the test
                test = test_func(*args, **kwargs)
            except ValueError as e:
                # problem with manipulating the data (our fault!)
                test = Result(text = str(e), code = Result.BROKEN)
                logger.error(str(e))
                # Adding additional information concerning the problem
                exc_type, exc_obj, tb = exc_info()
                f = tb.tb_frame
                lineno = tb.tb_lineno
                filename = f.f_code.co_filename
                linecache.checkcache(filename)
                line = linecache.getline(filename, lineno, f.f_globals)
                debug_msg = f'EXCEPTION IN ({filename}, LINE {lineno} "{line.strip()}"): {exc_obj}'
                logger.error(debug_msg)
                
            except PyWEDException as e:
                # problem to get the data from database (not our fault!)
                test = Result(text = str(e), code = Result.UNAVAILABLE)
                logger.error(str(e))
            except Exception as e:
                # any other problem 
                test = Result(text = str(e), code = Result.UNAVAILABLE)
                logger.error(str(e))

            return test
    return wrapper



def is_LHCD_on_pulse(pulse=0):
    """
    Test if LHCD was set 'on pulse' for the specified pulse number

    Parameters
    ----------
    pulse : int, optional
        Pulse number. The default is 0 (next pulse).

    Returns
    -------
    res : bool
        True or False

    """
    return bool(tsmat(pulse, AUTORISATION_LHCD))

def is_ICRH_on_pulse(pulse=0):
    """
    Test if ICRH was set 'on pulse' for the specified pulse number

    Parameters
    ----------
    pulse : int, optional
        Pulse number. The default is 0 (next pulse).

    Returns
    -------
    res : bool
        True or False

    """
    return bool(tsmat(pulse, AUTORISATION_ICRH))