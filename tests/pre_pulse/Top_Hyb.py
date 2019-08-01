# -*- coding: utf-8 -*-
"""
Top HYB verifications.

Check that the (F)TOPHYB defined in DP.xml are consistent with LH waveforms,
ie:
    - TOPHYB should not start after the expected start of LH power
    - FTOPHYB should not start before the expected end of LH power
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import pre_pulse_test
from pppat.libpulse.pulse_settings import PulseSettings  # for tests

import numpy as np
import logging
logger = logging.getLogger(__name__)

# Name of the waveforms used in this test
WF_NAMES = {'LH1': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref',
            'LH2': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref',
            'Timing': 'rts:WEST_PCS/TimingSystem/Code2Send.ref'}

# LH start and stop codes as defined in PCS
CODES = {'TOPHYB1': 144, 'FTOPHYB1': 145,
         'TOPHYB2': 146, 'FTOPHYB2': 147}


def _get_times_values_waveform(waveforms, name):
    """
    convenience function to return times and values of a given waveform name.
    Return nan if values not defined.
    Only get nominal segments (not segments >900)
    """
    wf = get_waveform(WF_NAMES[name], waveforms).nominal
    idx = wf.values.nonzero()
    if np.any(idx): # if no codes emittited (strange case, but just in case...)
        codes = wf.values[idx]
        times = wf.times[idx] - np.min(wf.times)
        return times, codes
    else:
        return np.nan, np.nan

def _get_LH(waveforms, name='LH1'):
    """
    Interpolate LH waveform on a finer time basis in order to not miss case of 
    relatively long power ramp-up or ramp-down
    """
    wf = get_waveform(WF_NAMES[name], waveforms)
    times = wf.times - np.min(wf.times)
    power = wf.values
    # interpolating waveform
    dt = 0.1  # s
    _t = np.arange(np.amin(times), np.amax(times), dt)
    _power = np.interp(_t, times, power)
    return _power, _t

@pre_pulse_test
def check_TOPHYB1(is_online=False, waveforms=None):
    """Check that the TOPHYB for LH1 is correctly set wrt to power waveform."""
    return _TOPHYB(waveforms=waveforms, antenna='LH1')


@pre_pulse_test
def check_TOPHYB2(is_online=False, waveforms=None):
    """Check that the TOPHYB for LH2 is correctly set wrt to power waveform."""
    return _TOPHYB(waveforms=waveforms, antenna='LH2')


@pre_pulse_test
def check_FTOPHYB1(is_online=False, waveforms=None):
    """Check that the FTOPHYB for LH1 is correctly set wrt to power waveform."""
    return _FTOPHYB(waveforms=waveforms, antenna='LH1')


@pre_pulse_test
def check_FTOPHYB2(is_online=False, waveforms=None):
    """Check that the FTOPHYB for LH2 is correctly set wrt to power waveform."""
    return _FTOPHYB(waveforms=waveforms, antenna='LH2')

def _FTOPHYB(waveforms=None, antenna='LH1'):
    """Check that the FTOPHYB if not before the expected LH power waveform end."""
    # retrieve timing and LH waveforms
    t_codes, codes = _get_times_values_waveform(waveforms, 'Timing')

    if antenna == 'LH1':
        CHECK_NAME = 'FTOPHYB1 (LH1)'
        FTOPHYB = CODES['FTOPHYB1']
        P_LH, t_LH = _get_LH(waveforms, name='LH1')
    elif antenna == 'LH2':
        CHECK_NAME = 'FTOPHYB2 (LH2)'
        FTOPHYB = CODES['FTOPHYB2']
        P_LH, t_LH = _get_LH(waveforms, name='LH2')
    else:  # just in case
        return Result(name='FTOPHYB', code=Result.UNAVAILABLE,
                      text=f'ValueError: bad antenna name!. Check the code')

    if np.any(np.isnan(t_LH)):  # no LH Power expected
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'No LH power set on {antenna}')
    # find the nearest time 
    # FTOPHYB corresponding to the antenna
    ts_FTOPHYB = t_codes[codes == FTOPHYB]
    # keep only the first one
    t_FTOPHYB = np.amin(ts_FTOPHYB)
    # integrate the LH power from 0 to t_TOPHYB
    # if OK, result should be negligible (<1kJ), otherwise -> error
    idx_t_FTOPHYB = np.argmin(np.abs(t_LH - t_FTOPHYB))
    energy = np.trapz(P_LH[idx_t_FTOPHYB:], t_LH[idx_t_FTOPHYB:])
    
    if energy > 1e3:
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'A FTOPHYB{antenna[-1]} is set at {t_FTOPHYB:.3f} before {antenna} should end. Ask the SL.')
    else:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'All FTOPHYB{antenna[-1]} are set after {antenna} should end (OK)')


def _TOPHYB(waveforms=None, antenna='LH1'):
    """Check that the TOPHYB if not after the expected LH power waveform start."""
    # retrieve timing and LH waveforms
    t_codes, codes = _get_times_values_waveform(waveforms, 'Timing')
    # interpolated power waveform
    P_LH, t_LH = _get_LH(waveforms, name=antenna)
        
    if antenna == 'LH1':
        CHECK_NAME = 'TOPHYB1 (LH1)'
        TOPHYB = CODES['TOPHYB1']
    elif antenna == 'LH2':
        CHECK_NAME = 'TOPHYB2 (LH2)'
        TOPHYB = CODES['TOPHYB2']
    else:  # just in case
        return Result(name='TOPHYB', code=Result.UNAVAILABLE,
                      text=f'ValueError: bad antenna name!. Check the code')

    if np.any(np.isnan(t_LH)):  # no LH Power expected
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'No LH power set on {antenna}')
        
    # find the nearest time 
    # TOPHYB corresponding to the antenna
    ts_TOPHYB = t_codes[codes == TOPHYB]

    # keep only the last one
    t_TOPHYB = np.amax(ts_TOPHYB)
    # integrate the LH power from 0 to t_TOPHYB
    # if OK, result should be negligible (<1kJ), otherwise -> error
    idx_t_TOPHYB = np.argmin(np.abs(t_LH - t_TOPHYB))
    energy = np.trapz(P_LH[0:idx_t_TOPHYB], t_LH[0:idx_t_TOPHYB])

    if energy > 1e3:
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'A TOPHYB{antenna[-1]} is set at {t_TOPHYB:.3f} after {antenna} should start. Ask the SL.')
    else:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'All TOPHYB{antenna[-1]} are set before {antenna} should start (OK)')        
    
    
    
# For debug and testing purpose
if __name__ == '__main__':
    # A TOPHYB located after KLH pulse (SL shoud clean the mess...)
    ps = PulseSettings(54529)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))

    # all TOPHYB and FTOPHYB fail
    ps = PulseSettings(54527)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))

    # One failure of FTOPHYB2
    ps = PulseSettings(54528)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))

    # case of no LH at all
    # should result all OK
    ps = PulseSettings(54456)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))

    # case of LH in 54669: TOPHYB arrive after the beginning 
    # should results an error
    ps = PulseSettings(54669)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))
    
    #%% affichage
    import matplotlib.pyplot as plt
    pulse = 54529
    ps = PulseSettings(pulse)
    
    P_LH1, t_LH1 = _get_LH(ps.waveforms, name='LH1')
    P_LH2, t_LH2 = _get_LH(ps.waveforms, name='LH2')
    
    t_codes, codes = _get_times_values_waveform(ps.waveforms, 'Timing')
    #%% affichage
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].set_title(f'#{pulse}')
    ax[0].plot(t_LH1, P_LH1, label='LH1')
    t_TOPHYB1 = t_codes[codes == CODES['TOPHYB1']]
    for t in t_TOPHYB1:
        ax[0].axvline(t, color='g')
    t_FTOPHYB1 = t_codes[codes == CODES['FTOPHYB1']]
    for t in t_FTOPHYB1:
        ax[0].axvline(t, color='r')
    
    ax[1].plot(t_LH2, P_LH2, label='LH2')
    t_TOPHYB2 = t_codes[codes == CODES['TOPHYB2']]
    for t in t_TOPHYB2:
        ax[1].axvline(t, color='g')
    t_FTOPHYB2 = t_codes[codes == CODES['FTOPHYB2']]
    for t in t_FTOPHYB2:
        ax[1].axvline(t, color='r')
    
    ax[0].set_title('LH1')
    ax[1].set_title('LH2')
