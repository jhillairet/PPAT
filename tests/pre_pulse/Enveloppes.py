# -*- coding: utf-8 -*-
"""
Waveform envelopes verifications.

Check that the envelopes, which are safety limits defined by the SL,
are correct with respect to the associated waveforms. 
- if an envelope is too low (waveform values above limit)

Reaching an envelope during a pulse will trigger a change of segment, 
most often a change to the soft lending segment, which would result is a 
pulse failure. Et donc des sous perdus.

"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import pre_pulse_test
import numpy as np
import logging
logger = logging.getLogger(__name__)

# Names of the tested waveforms.
# This is a dict of dict, where for each base item are associated the
# waveform reference, the min and max envelopes.
WFS = {
        'Ip': {
                'ref': 'rts:WEST_PCS/Plasma/Ip/waveform.ref',
                'min': 'rts:WEST_PCS/Plasma/Ip/min_env_waveform.ref',
                'max': 'rts:WEST_PCS/Plasma/Ip/max_env_waveform.ref',
                }
        # 'LH1 Pow': {
        #         'ref': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref',
        #         'min': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/1/min_env_waveform.ref',
        #         'max': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/1/max_env_waveform.ref'
        #         },
        # 'LH2 Pow': {
        #         'ref': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref',
        #         'min': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/min_env_waveform.ref',
        #         'max': 'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/max_env_waveform.ref',
        #         },
        # 'IC Q1 Pow': {
        #         'ref': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref',
        #         'min': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/1/min_env_waveform.ref',
        #         'max': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/1/max_env_waveform.ref',
        #         },
        # 'IC Q2 Pow': {
        #         'ref': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref',
        #         'min': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/min_env_waveform.ref',
        #         'max': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/max_env_waveform.ref',
        #         },
        # 'IC Q4 Pow': {
        #         'ref': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref',
        #         'min': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/min_env_waveform.ref',
        #         'max': 'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/max_env_waveform.ref',
        #         },
}


def _test_envelope_min(is_online=False, waveforms=None, name='', min_val=0):
    """
    Test a waveform vs its envelope min values.
    
    For each time of the envelope, get the waveform value and test
    if this value is below the envelope values. Returns the first error found.
    """
    CHECK_NAME = f'Envelope: mininum values of {name}'

    wf = get_waveform(WFS[name]['ref'], waveforms)
    env_min = get_waveform(WFS[name]['min'], waveforms)

    for (t, val) in zip(env_min.times, env_min.values):
        idts = np.argwhere(wf.times == t)
        for idt in idts:  # maybe few matches
            if (wf.values[idt] <= val) and (val > min_val):
                return Result(name=CHECK_NAME, code=Result.ERROR,
                              text=f'Waveform of {name} below min envelope in {wf.segments[int(idt)]}')
    # if here, everything is fine
    return Result(name=CHECK_NAME, code=Result.OK,
                  text=f'Waveform of {name} higher than all min envelope (OK)')

def _test_envelope_max(is_online=False, waveforms=None, name='', min_val=0):
    """
    Test a waveform vs its envelope max values.
    
    For each time of the envelope, get the waveform value and test
    if this value is above the envelope values. Returns the first error found.
    """
    CHECK_NAME = f'Envelope: maximum values of {name}'

    wf = get_waveform(WFS[name]['ref'], waveforms)
    env_max = get_waveform(WFS[name]['max'], waveforms)

    for (t, val) in zip(env_max.times, env_max.values):
        idts = np.argwhere(wf.times == t)
        for idt in idts:  # maybe few matches
            if (wf.values[idt] >= val) and (val > min_val):
                return Result(name=CHECK_NAME, code=Result.ERROR,
                              text=f'Waveform of {name} above max envelope in {wf.segments[int(idt)]}')
    # if here, everything is fine
    return Result(name=CHECK_NAME, code=Result.OK,
                  text=f'Waveform of {name} lower than all max envelope (OK)')

@pre_pulse_test
def check_envelope_max_Ip(is_online=False, waveforms=None):
    """
    Check the plasma current waveform against its max envelope. 
    """
    # min plasma current is supposed to be 100e3 A.
    return _test_envelope_max(waveforms=waveforms, name='Ip', min_val=100e3)

@pre_pulse_test
def check_envelope_min_Ip(is_online=False, waveforms=None):
    """
    Check the plasma current waveform against its min envelope. 
    """
    # min plasma current is supposed to be 100e3 A.
    return _test_envelope_min(waveforms=waveforms, name='Ip', min_val=100e3)

# For debug and testing purpose
if __name__ == '__main__':
    from pppat.libpulse.waveform import get_waveform
    from pppat.libpulse.pulse_settings import PulseSettings

    # Example of envelope error on Ip : 54636
    ps = PulseSettings(54636)
    print(check_envelope_max_Ip(waveforms=ps.waveforms))

    # Example of ok: 54635
    ps = PulseSettings(54635)
    print(check_envelope_max_Ip(waveforms=ps.waveforms))

#    name = 'Ip'
#    wf = get_waveform(WFS[name]['ref'], ps.waveforms)
#    env_min = _get_envelope_min(name, ps.waveforms)
#    env_max = _get_envelope_max(name, ps.waveforms)
#
#    import matplotlib.pyplot as plt
#    fig, ax = plt.subplots()
#    ax.plot(wf.times, wf.values)
#    ax.plot(env_min.times, env_min.values)
#    ax.plot(env_max.times, env_max.values)



