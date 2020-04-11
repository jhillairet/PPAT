# -*- coding: utf-8 -*-
"""
Check all waveforms time array to detect any inconsitencies, such as a:
    - values "back in time" 
    - negative times
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import pre_pulse_test 
from pywed import tsmat
import numpy as np
import logging
logger = logging.getLogger(__name__)


@pre_pulse_test
def check_back_in_time_values(is_online=True, waveforms=None):
    """
    Check that all waveform time array are 'progessive' in time, that is
    there are no "back in time values" (happened for Gas/valve16 in #55856)
    """
    CHECK_NAME = 'Back In Time Values'

    if not is_online:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text='WEST database is not available')
    else:       
        for waveform in waveforms:
            wf = get_waveform(waveform.name, waveforms)
            if wf: # if not empty waveform            
                dt = np.diff(wf.times)
                # check that time values are progressive (no back in time)
                if np.any(dt < 0):
                    return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=f'Some time value increments are negative in {waveform.name}')
        # if we are here, means it is allright for all waveforms
        return Result(name=CHECK_NAME, code=Result.OK,
                         text='All time values increment are positive')       


@pre_pulse_test
def check_negative_time_values(is_online=True, waveforms=None):
    """
    Check that all waveform time array are positives
    """
    CHECK_NAME = 'Negative Time Values'

    if not is_online:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text='WEST database is not available')
    else:       
        for waveform in waveforms:
            wf = get_waveform(waveform.name, waveforms)
            if wf: # if not empty waveform            
                if np.any(wf.times < 0):
                    return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=f'Some time value are negative in {waveform.name}')
        # if we are here, means it is allright for all waveforms
        return Result(name=CHECK_NAME, code=Result.OK,
                         text='All time values are positive')   

if __name__ == '__main__':
    from pppat.libpulse.pulse_settings import PulseSettings
    # Back in time problem with Gas/valve16 
    ps = PulseSettings(55856)
    print(check_back_in_time_values(waveforms=ps.waveforms))
    print(check_negative_time_values(waveforms=ps.waveforms))
    
    # The problem has been corrected in the following shot
    ps = PulseSettings(55857)
    print(check_back_in_time_values(waveforms=ps.waveforms))
    print(check_negative_time_values(waveforms=ps.waveforms))


    
