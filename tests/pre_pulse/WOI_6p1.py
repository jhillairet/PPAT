# -*- coding: utf-8 -*-
"""
WOI 6.1 : lower divertor PFUs
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils_west import continuous_signal_from_time
import datetime
import numpy as np
import logging
logger = logging.getLogger(__name__)


def check_WOI_6p1_initial_temperature(is_online=True, waveforms=None):
    """
    Check the max temperature on the lower divertor during the last 10 min.

    The temperature should be below 200°C in order to start a new pulse.
    """
    CHECK_NAME = 'WOI 6.1: lower PFUs. Initial temperature.'
    T_ERROR = 200  # °C
    T_WARNING = 150  # °C

    # get the current time and deduce the time 10 minutes before
    now = datetime.datetime.now()
    date = now.strftime('%d/%m/%y')
    time_now = now.strftime('%H:%M:%S')
    time_ten_min_before = (now - datetime.timedelta(minutes=10)).strftime('%H:%M:%S')

    # get the max temperature from Lower Divertor Thermocouples
    sig_TCs_divertor = ['GETC_ISP_6A',  # TC inner strike point Q6A
                        'GETC_OSP_6A',  # TC outer strike point Q6A
                        'GETC_OSP_1A',  # TC outer strike point Q1A
                        'GETC_RIPL_6A']  # TC toroidaux Q6A
    max_temp = []
    for sig in sig_TCs_divertor:
        T, t = continuous_signal_from_time(sig, date,
                                     t_start=time_ten_min_before,
                                     t_stop=time_now)
        # keep only realist temperatures (>10°C)
        T2 = np.where(T > 10, T, -1)
        max_temp.append(np.amax(T2))  # max of the signal

    max_max_temp = np.amax(max_temp)  # max of the max

    if max_max_temp > T_ERROR:
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'Max Temp Lower Divertor during last 10min: {max_max_temp:.0f}°C > {T_ERROR}')
    elif max_max_temp > T_WARNING:
        return Result(name=CHECK_NAME, code=Result.WARNING,
                      text=f'Max Temp Lower Divertor during last 10min: {max_max_temp:.0f}°C > {T_WARNING}')
    else:  # I guess it is OK then
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'Max Temp Lower Divertor during last 10min: {max_max_temp:.0f}°C')


#def check_WOI_6p1_Xpoint_duration(is_online=False, waveforms=None):
#    """ Check the duration of the X-point phase """
#    CHECK_NAME = 'WOI 6.1: lower PFUs'
#    MAXIMUM_XPOINT_DURATION = 10  # s
#
#    waveform_name = 'rts:WEST_PCS/Actuators/Poloidal/IXb/waveform.ref'
#    waveform = get_waveform(waveform_name, waveforms)
#
#    if not waveform:
#        raise(ValueError(f'waveform {waveform_name} not found!?'))
#    else:
#        IXb = waveform.values
#        t_IXb = waveform.times
#        nonzero_idx = np.argwhere(IXb != 0)
#
#        logger.info(np.array(np.where(IXb != 0)).squeeze() )
#        logger.info(t_IXb[nonzero_idx].squeeze() )
#
#        # TODO : the following fails.
#        if len(nonzero_idx) > 0:
#            #FirstNonZero_index = nonzero_idx[0]
#            #LastZero_index = FirstNonZero_index - 1
#            TimeXpointStart = np.interp(0.0, IXb[nonzero_idx], t_IXb[nonzero_idx])
#            LastNonZero_indexes = np.where(IXb > 0)[0]
#            LastNonZero_index = LastNonZero_indexes[-1]
#            FinalZero_index = LastNonZero_index + 1
#            TimeXpointStop = np.interp(0.0,IXb[LastNonZero_index:FinalZero_index],t_IXb[LastNonZero_index:FinalZero_index])
#            duration_Xpoint = TimeXpointStop - TimeXpointStart
#
#        else:
#            duration_Xpoint = 0.0
#
#        if duration_Xpoint > MAXIMUM_XPOINT_DURATION:
#            return Result(name=CHECK_NAME, code=Result.ERROR,
#                          text='Lower X-point phase too long: Lower divertor coils ON during')
#        else:
#            return Result(name=CHECK_NAME, code=Result.OK,
#                          text='Lower X-point phase duration OK')


if __name__ == '__main__':
    res=check_WOI_6p1_initial_temperature()