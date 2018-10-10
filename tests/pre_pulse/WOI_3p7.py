# -*- coding: utf-8 -*-
"""
WOI 3.7 : plasma current
"""
from pppat.libpulse.check_result import CheckResult as Result
import numpy as np

import logging
logger = logging.getLogger(__name__)


def check_WOI_3p7_plasma_current(is_online=False, waveforms=None):
    """ Check the expected plasma current values """
    check_name = 'WOI 3.7: plasma current'


    # retrieve the Ip waveform
    waveform_name = 'rts:WEST_PCS/Plasma/Ip/waveform.ref'
    
    waveform_ip = None
    for waveform in waveforms:
        if waveform.name == waveform_name:
            waveform_ip = waveform
            logger.info('-----------> found it!!')
    if waveform_ip:  # found it      
        logger.info(waveform_ip.values)
        # check the max Ip
        Ip_max = np.amax(waveform_ip.values)
        logger.info(f'Ip_max = {Ip_max}')

        if Ip_max > 1e6:
            return Result(name=check_name, code=Result.ERROR, 
                          text='Plasma current above maximum limit')
        else:
            return Result(name=check_name, code=Result.OK,
                          text='Plasma current OK')    

    else:
        raise(ValueError('waveform not found?'))
#    check_result_array = np.array([],dtype='object')
#    check_result_array = np.append(check_result_array,check_result.check_result())
#
#    #Max Ip test
#
#    Ip_limit = 1e6
#
#    signal_array = np.array([])
#    signal_array = np.append(signal_array,'rts:WEST_PCS/Plasma/Ip/waveform.ref')
#    wform = waveformBuilder(segmentTrajectory,signal_array,infile)
#    t_Ip = wform[0].times
#    t_Ip_rel = wform[0].reltimes
#    Ip = wform[0].values
#    segments = wform[0].segments
#
#
#    fail_indexes = np.where(Ip>Ip_limit)
#
#    fail_times = t_Ip[fail_indexes]
#    fail_reltimes = t_Ip_rel[fail_indexes]
#    fail_values = Ip[fail_indexes]
#    fail_segments = segments[fail_indexes]
#
#
#    check_result_array[0].check_fail_values_unit = 'A'
#    check_result_array[0].check_fail_limit = Ip_limit
#    check_result_array[0].check_name = 'A - Plasma Current'
#
#    if fail_indexes[0].size==0:
#        check_result_array[0].check_result_code = 3
#        check_result_array[0].check_result_text = 'OK'
#        check_result_array[0].check_fail_abs_times = np.array([])
#        check_result_array[0].check_fail_values =  np.array([])
#        check_result_array[0].check_fail_rel_times = np.array([])
#        check_result_array[0].check_fail_segments = np.array([])
#
#
#    else:
#        check_result_array[0].check_result_code = 0
#        check_result_array[0].check_result_text = 'Maximum plasma current exceeded'
#        check_result_array[0].check_fail_abs_times = fail_times
#        check_result_array[0].check_fail_values = fail_values
#        check_result_array[0].check_fail_rel_times = fail_reltimes
#        check_result_array[0].check_fail_segments = fail_segments
#
#
#    return check_result_array


if __name__ == '__main__':
    """ Testing purpose """
    DP_file = '../../resources/pulse_setup_examples/52865/DP.xml'
    Sup_file = '../../resources/pulse_setup_examples/52865/Sup.xml'
    signal_list = ['rts:WEST_PCS/Plasma/Ip/waveform.ref']

    DCS = DCSSettings(Sup_file)
    ns = DCS.nominal_scenario

    wf = waveformBuilder(DCS.nominal_scenario, signal_list, DP_file)
