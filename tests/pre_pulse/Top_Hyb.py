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
    """
    wf = get_waveform(WF_NAMES[name], waveforms)
    idx = wf.values.nonzero()
    if np.any(idx): # if no codes emittited (strange case, but just in case...)
        codes = wf.values[idx]
        times = wf.times[idx] - np.min(wf.times)
        return times, codes
    else:
        return np.nan, np.nan


@pre_pulse_test
def check_TOPHYB1(is_online=False, waveforms=None, antenna='LH1'):
    """Check that the TOPHYB for LH1 is correctly set wrt to power waveform."""
    return _TOPHYB(waveforms=waveforms, antenna=antenna)


@pre_pulse_test
def check_TOPHYB2(is_online=False, waveforms=None, antenna='LH2'):
    """Check that the TOPHYB for LH2 is correctly set wrt to power waveform."""
    return _TOPHYB(waveforms=waveforms, antenna=antenna)


@pre_pulse_test
def check_FTOPHYB1(is_online=False, waveforms=None, antenna='LH1'):
    """Check that the FTOPHYB for LH1 is correctly set wrt to power waveform."""
    return _FTOPHYB(waveforms=waveforms, antenna=antenna)


@pre_pulse_test
def check_FTOPHYB2(is_online=False, waveforms=None, antenna='LH2'):
    """Check that the FTOPHYB for LH2 is correctly set wrt to power waveform."""
    return _FTOPHYB(waveforms=waveforms, antenna=antenna)


def _TOPHYB(waveforms=None, antenna='LH1'):
    """Check that the TOPHYB if not after the expected LH power waveform start."""
    # retrieve timing and LH waveforms
    t_codes, codes = _get_times_values_waveform(waveforms, 'Timing')

    if antenna == 'LH1':
        CHECK_NAME = 'TOPHYB1 (LH1)'
        t_LH, P_LH = _get_times_values_waveform(waveforms, 'LH1')
        TOPHYB = CODES['TOPHYB1']
    elif antenna == 'LH2':
        CHECK_NAME = 'TOPHYB2 (LH2)'
        t_LH, P_LH = _get_times_values_waveform(waveforms, 'LH2')
        TOPHYB = CODES['TOPHYB2']
    else:  # just in case
        return Result(name='FTOPHYB', code=Result.UNAVAILABLE,
                      text=f'ValueError: bad antenna name!. Check the code')

    if np.any(np.isnan(t_LH)):  # no LH Power expected
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'No LH power set on {antenna}')

    # si le code de début LH est situé après le début du creneau LH -> erreur
    # NB: il peut y'avoir des début LH après la fin du creneau LH. --> ignorés
    t_TOPHYB = t_codes[codes == TOPHYB]
    for _t in t_TOPHYB:
        if np.any((_t > t_LH[0]) & (_t < t_LH[-1]) ):
            # return ERROR at first error detected
            return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'A TOPHYB{antenna[-1]} is set at {_t:.3f}, after {antenna} should start ({t_LH[0]:.3f}). Ask the SL.')
    # if here, everything is OK
    return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'All TOPHYB{antenna[-1]} are set before {antenna} should start (OK)')


def _FTOPHYB(waveforms=None, antenna='LH1'):
    """Check that the FTOPHYB if not before the expected LH power waveform end."""
    # retrieve timing and LH waveforms
    t_codes, codes = _get_times_values_waveform(waveforms, 'Timing')

    if antenna == 'LH1':
        CHECK_NAME = 'FTOPHYB1 (LH1)'
        FTOPHYB = CODES['FTOPHYB1']
        t_LH, P_LH = _get_times_values_waveform(waveforms, 'LH1')
    elif antenna == 'LH2':
        CHECK_NAME = 'FTOPHYB2 (LH2)'
        FTOPHYB = CODES['FTOPHYB2']
        t_LH, P_LH = _get_times_values_waveform(waveforms, 'LH2')
    else:  # just in case
        return Result(name='FTOPHYB', code=Result.UNAVAILABLE,
                      text=f'ValueError: bad antenna name!. Check the code')

    if np.any(np.isnan(t_LH)):  # no LH Power expected
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'No LH power set on {antenna}')

    # si le code de fin LH est situé avant la fin du creneau LH -> erreur
    # NB: il peut y'avoir des fin LH après la fin du creneau LH. --> ignorés
    t_FTOPHYB = t_codes[codes == FTOPHYB]
    for _t in t_FTOPHYB:
        if (_t > t_LH[0]) & (_t < t_LH[-1]):
            # return ERROR at first error detected
            return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'A FTOPHYB{antenna[-1]} is set at {_t:.3f} before {antenna} should end ({t_LH[-1]:.3f}). Ask the SL.')
    # if here, everything is OK
    return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'All FTOPHYB{antenna[-1]} are set after {antenna} should end (OK)')


# For debug and testing purpose
if __name__ == '__main__':
    from pppat.libpulse.waveform import get_waveform
    from pppat.libpulse.pulse_settings import PulseSettings

    # ok situation
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

    # One failure of FTOPHYB1
    ps = PulseSettings(54528)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))

    # case of no LH at all
    ps = PulseSettings(54456)
    print(check_TOPHYB1(waveforms=ps.waveforms))
    print(check_FTOPHYB1(waveforms=ps.waveforms))
    print(check_TOPHYB2(waveforms=ps.waveforms))
    print(check_FTOPHYB2(waveforms=ps.waveforms))

    # #%% affichage
    # import matplotlib.pyplot as plt
    # pulse = 54568
    # ps = PulseSettings(pulse)
    # t_LH, P_LH = _get_times_values_waveform(ps.waveforms, 'LH1')
    # t_codes, codes = _get_times_values_waveform(ps.waveforms, 'Timing')
    # fig, ax = plt.subplots(2, 1, sharex=True)
    # ax[0].set_title(f'#{pulse}')
    # ax[0].plot(t_LH, P_LH)
    # ax[1].stem(t_codes, codes)
    # ax[1].axhline(CODES['TOPHYB1'], color='green')
    # ax[1].axhline(CODES['FTOPHYB1'], color='red')
    # ax[1].set_ylim(CODES['TOPHYB1']-1, CODES['FTOPHYB1']+1)
    # [a.axvspan(t_LH[0], t_LH[-1], color='grey', alpha=.5) for a in ax]
