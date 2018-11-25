# -*- coding: utf-8 -*-
"""
WOI 5.5 :
POWER INJECTION
ION CYCLOTRON WAVE HEATING SYSTEM
POWER AND ENERGY LIMITS

WOI V3 (20/11/2018)
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import pre_pulse_test
import numpy as np
import logging
logger = logging.getLogger(__name__)


# TODO : use global settings

# Maximum values with and without infra-red
MAX_ENERGY_WITHOUT_IR = 2  # MJ
MAX_POWER_WITHOUT_IR = 1  # MW
MAX_DURATION_WITHOUT_IR = 2  # s

MAX_DURATION_WITH_IR = 5  # s

# TODO : use global settings
# Max settings for Q1, Q2 and Q4
MAX_ENERGIES = {'Q1': 2,  # in MJ. No IR for Q1 -> 2 MJ max
                'Q2': None,  # no limit for Q2
                'Q4': None}  # no Q4 yet
MAX_DURATIONS = {'Q1': 5, 
                 'Q2': 5, 
                 'Q4': 5}  # s

# ICRH waveforms name
wf_names = ['rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref',
            'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref',
            'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref']

@pre_pulse_test
def check_WOI_5p5_energy_limits(is_online=False, waveforms=None):
    """ Check the max energy limits for ICRH """
    CHECK_NAME = 'WOI 5.5: ICRH Energy limits'
        
    # check if one of the waveform is higher than the limits
    antennas = ['Q1', 'Q2', 'Q4']
    text = 'Energies: ' 
    code = Result.OK
    for (antenna, wf_name) in zip(antennas, wf_names):
        # retrieve ICRH waveforms
        wf = get_waveform(wf_name, waveforms)
        
        # integrate the power to get the energy
        E_MJ = np.trapz(wf.values, wf.times) / 1e6  # in Mega Joules
        
        # if there is an energy limit for the current antenna, and if > limit
        if MAX_ENERGIES[antenna] and (E_MJ > MAX_ENERGIES[antenna]):
            text += f'{antenna}: {E_MJ:.3f} MJ>{MAX_ENERGIES[antenna]} MJ - '
            code = Result.WARNING
        else:
            text += f'{antenna}: OK - '

    if code == Result.WARNING:
        return Result(name=CHECK_NAME, code=code, text=text)
    elif code == Result.OK:
        return Result(name=CHECK_NAME, code=code, text=text)
    else:
        return Result(name=CHECK_NAME, code=code, text='Not available')

@pre_pulse_test
def check_WOI_5p5_duration_limits(is_online=False, waveforms=None):
    """ Check the max duration limits for ICRH """
    CHECK_NAME = 'WOI 5.5: ICRH Power duration'

    # check if one of the waveform is higher than the limits
    antennas = ['Q1', 'Q2', 'Q4']
    text = 'Durations: ' 
    code = Result.OK
    for (antenna, wf_name) in zip(antennas, wf_names):
        # retrieve ICRH waveforms
        wf = get_waveform(wf_name, waveforms)
        # retrieve the duration of the IC pulse
        try:    
            ic_times = wf.times[np.nonzero(wf.values)]
            ic_duration = ic_times[-1] - ic_times[0]
        except IndexError as e:
            # case if no IC power is expected on an antenna
            ic_duration = None
            
        # if there is a duration limit for the current antenna, and if > limit
        if ic_duration and (ic_duration > MAX_DURATIONS[antenna]):
            text += f'{antenna}: {ic_duration:.3f} s>{MAX_DURATIONS[antenna]} s - '
            code = Result.WARNING
        else:
            text += f'{antenna}: OK - '

    if code == Result.WARNING:
        return Result(name=CHECK_NAME, code=code, text=text)
    elif code == Result.OK:
        return Result(name=CHECK_NAME, code=code, text=text)
    else:
        return Result(name=CHECK_NAME, code=code, text='Not available')

# For debug and testing purpose
if __name__ == '__main__':
    from pppat.libpulse.waveform import get_waveform
    from pppat.libpulse.pulse_settings import PulseSettings
    # get pulse settings
    ps = PulseSettings(53706)

    wf_names = ['rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref',
                'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref',
                'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref']
        
    antennas = ['Q1', 'Q2', 'Q4']
    text = 'Max IC energy: ' 
    for (antenna, wf_name) in zip(antennas, wf_names):
        # retrieve ICRH waveforms
        wf = get_waveform(wf_name, ps.waveforms)
        
        # integrate the power to get the energy
        E_MJ = np.trapz(wf.values, wf.times) / 1e6  # in Mega Joules
        print(E_MJ)
        if MAX_ENERGIES[antenna]:
            if E_MJ > MAX_ENERGIES[antenna]:
                print(f'{antenna} !!')
#    # test the pre test functions
#    res_e = check_WOI_5p5_energy_limits(is_online=False, waveforms=ps.waveforms)
#    res_t = check_WOI_5p5_duration_limits(is_online=False, waveforms=ps.waveforms)

