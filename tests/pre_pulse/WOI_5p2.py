# -*- coding: utf-8 -*-
"""
WOI 5.5 :
POWER INJECTION
LHCD Plasma Operation


WOI V4 (22/11/2018)
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import pre_pulse_test
import numpy as np
import logging
logger = logging.getLogger(__name__)


# TODO : use global settings
LH1_MAX_POWER = 4  # MW, FAM launcher
LH2_MAX_POWER = 2.7  # MW, PAM launcher

# LHCD waveforms name
wf_names = {'LH1': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref',
            'LH2': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref'}

LH_MAX_POWER_vs_TIME = {
    'LH1': np.array([[1, 4],
                     [5, 3],
                     [20, 2],
                     [30, 1.87],
                     [60, 1.6]]),
    'LH2': np.array([[0, 2],
                     [0.5, 2],
                     [1, 2],
                     [1.5, 2],
                     [2, 2],
                     [2, 1.8],
                     [2, 1.5],
                     [2, 1.4],
                     [2, 0.8],
                     [2, 0.8],
                     [5, 0.515],
                     [20, 0.294],
                     [30, 0.25]])}


@pre_pulse_test
def check_WOI_5p2_antenna_max_powers(is_online=False, waveforms=None):
    """
    Check the max LH power
    """
    CHECK_NAME = 'WOI 5.2: LHCD Antenna max powers'
    # retrieve LHCD waveforms
    wfs = []
    for (antenna, wf_name) in wf_names.items():
        wfs.append(get_waveform(wf_name, waveforms))

    # Check max antenna power
    LH1_max_power = np.amax(wfs[0].values)/1e6
    LH2_max_power = np.amax(wfs[1].values)/1e6

    if (LH1_max_power < LH1_MAX_POWER) and (LH2_max_power < LH2_MAX_POWER):
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'Max LH powers: LH1:{LH1_max_power:.1f} MW, LH2:{LH2_max_power:.1f} MW')
    elif (LH1_max_power >= LH1_MAX_POWER) and (LH2_max_power < LH2_MAX_POWER):
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'Max LH powers: LH1:{LH1_max_power:.1f} MW > {LH1_MAX_POWER} MW (LH2 OK:{LH2_max_power:.1f} MW)')
    elif (LH1_max_power < LH1_MAX_POWER) and (LH2_max_power >= LH2_MAX_POWER):
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'Max LH powers: LH2:{LH2_max_power:.1f} MW > {LH2_MAX_POWER} MW (LH1 OK:{LH1_max_power:.1f} MW)')
    else:
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'Max LH powers: LH1:{LH1_max_power:.1f} MW > {LH1_MAX_POWER} MW and LH2 {LH2_max_power:.1f} MW > {LH2_MAX_POWER} MW')

def check_WOI_5p2_antenna_power_waveform_LH1(is_online=False, waveforms=None):
    """
    Check the LH1 power waveforms if always below the authorized values
    """
    CHECK_NAME = 'WOI 5.2: LHCD Antenna: LH1 power waveforms'


    res = _is_waveform_below_limit(waveforms, 'LH1')

    if res is np.True_:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text='LH1 power waveform under the WOI limit')
    elif res is np.False_:
        return Result(name=CHECK_NAME, code=Result.WARNING,
                      text='LH1 power waveform above the WOI limit! Check with LHO.')
    elif res is None:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text=f'No LH1 power waveform')
    else:  # we shouldn't be here!
        return Result(name=CHECK_NAME, code=Result.BROKEN,
                      text='Hu ho... ')


def check_WOI_5p2_antenna_power_waveform_LH2(is_online=False, waveforms=None):
    """
    Check the LH2 power waveforms if always below the authorized values
    """
    CHECK_NAME = 'WOI 5.2: LHCD Antenna: LH2 power waveforms'

    res = _is_waveform_below_limit(waveforms, 'LH2')

    if res is np.True_:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text='LH2 power waveform under the WOI limit')
    elif res is np.False_:
        return Result(name=CHECK_NAME, code=Result.WARNING,
                      text='LH2 power waveform above the WOI limit! Check with LHO.')
    elif res is None:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text=f'No LH2 power waveform')
    else:  # we shouldn't be here!
        return Result(name=CHECK_NAME, code=Result.BROKEN,
                      text='Hu ho... ')
            

def _is_waveform_below_limit(waveforms, antenna):
    """ 
    Return True is the power waveform is above the limit for all times. 
    Return False is not, of 
    """
    t, Plh, Plh_lim = _get_power_waveforms(waveforms, antenna)
    if np.any(np.isnan(t)):
        return None
    else:
        # test if all the points in the waveform are below the limit
        return np.all(Plh < Plh_lim)


def _get_power_waveforms(waveforms, antenna, dt=0.1):
    """
    Return the LH antenna power waveform and its associated waveform limit
    in an interpolated (more refined) time base (dt=0.1s)
    """
    wf = get_waveform(wf_names[antenna], waveforms)
    idx_lh = wf.values.nonzero()
    if np.any(idx_lh):  # if LH not zero
        Plh = wf.values[idx_lh]/1e6 # in MW
        tlh = wf.times[idx_lh] - np.min(wf.times[idx_lh])  # rel. time
    
        # create a precise time base used for interpolations
        t_ = np.arange(start=0, stop=np.max(tlh), step=dt)
        Plh_ = np.interp(t_, tlh, Plh)
        Plh_lim = np.interp(t_, LH_MAX_POWER_vs_TIME[antenna][:,0],
                            LH_MAX_POWER_vs_TIME[antenna][:,1])
        return t_, Plh_, Plh_lim
    else:
        return np.nan, np.nan, np.nan

# For debug and testing purpose
if __name__ == '__main__':
    from pppat.libpulse.waveform import get_waveform
    from pppat.libpulse.pulse_settings import PulseSettings
    import matplotlib.pyplot as plt
   
    # test all possible cases. 
    # should give UNAV & UNAV, OK & OK, OK & WAR, WAR & OK, and WAR & WAR
    pulses = [53799,  # no LH
              53804,  # both waveforms below limits
              53814,  # only LH2 waveform limit exceed
              53817,  # only LH1 waveform limit exceed
              53841]  # both waveform limit exceed!

    for pulse in pulses:
         # get pulse settings
        ps = PulseSettings(pulse) 
        print(check_WOI_5p2_antenna_power_waveform_LH1(waveforms=ps.waveforms))
        print(check_WOI_5p2_antenna_power_waveform_LH2(waveforms=ps.waveforms))
    
        fig, ax = plt.subplots(2,1)
        t, Plh, Plh_lim = _get_power_waveforms(ps.waveforms, 'LH1')
        ax[0].plot(t, Plh, t, Plh_lim)
        t, Plh, Plh_lim = _get_power_waveforms(ps.waveforms, 'LH2')
        ax[1].plot(t, Plh, t, Plh_lim)
        fig.show()
    
