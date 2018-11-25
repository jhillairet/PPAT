# -*- coding: utf-8 -*-
"""
WOI Pre-pulse test

"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import pre_pulse_test
import numpy as np
import logging
logger = logging.getLogger(__name__)


@pre_pulse_test  # do not remove
def check_pre_pulse_super_test(is_online=False, waveforms=None):
    """ 
    Description ici
    """
    CHECK_NAME = 'Name of the pre pulse test'

    # Do a test 

    # return the result of the test
    if some_condition:
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text='explanation here')
    else:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text='explanation here')
