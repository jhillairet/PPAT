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


# ICRH waveforms name
wf_names = ['rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref',
            'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref',
            'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref']

@pre_pulse_test
def check_WOI_5p5_energy_limits(is_online=False, waveforms=None):
    """ Check the max energy limits for ICRH """
    CHECK_NAME = 'WOI 5.5: ICRH Energy limits'

    # retrieve ICRH waveforms
    wfs = []
    for wf_name in wf_names:
        wfs.append(get_waveform(wf_name, waveforms))
    # integrate the power to get the energy
    E_MJ = []
    for wf in wfs:
        E_MJ.append(np.trapz(wf.values, wf.times) / 1e6)  # in Mega Joules
    # check if one of the waveform is higher than the limits
    if np.any(np.array(E_MJ) > MAX_ENERGY_WITHOUT_IR):
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'max IC programmed energy: {np.amax(E_MJ):.3f} MJ > {MAX_ENERGY_WITHOUT_IR} MJ (no IR)')
    else:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'max IC programmed energy: {np.amax(E_MJ):.3f} MJ < {MAX_ENERGY_WITHOUT_IR} MJ (no IR)')


@pre_pulse_test
def check_WOI_5p5_power_limits(is_online=False, waveforms=None):
    """ Check the max power limits for ICRH """
    CHECK_NAME = 'WOI 5.5: ICRH Power limits'

    # retrieve ICRH waveforms
    wfs = []
    for wf_name in wf_names:
        wfs.append(get_waveform(wf_name, waveforms))
    # retrieve the max power programmed
    P_IC_max = []
    for wf in wfs:
        P_IC_max.append(np.amax(wf.values)/1e6)  # in Mega Watts
    # check if one of the waveform is higher than the limits
    if np.any(np.array(P_IC_max) > MAX_POWER_WITHOUT_IR):
        return Result(name=CHECK_NAME, code=Result.ERROR,
                      text=f'max IC programmed power: {np.amax(P_IC_max):.3f} MW > {MAX_ENERGY_WITHOUT_IR} MW (no IR)')
    else:
        return Result(name=CHECK_NAME, code=Result.OK,
                      text=f'max IC programmed power: {np.amax(P_IC_max):.3f} MW < {MAX_ENERGY_WITHOUT_IR} MW (no IR)')

@pre_pulse_test
def check_WOI_5p5_duration_limits(is_online=False, waveforms=None):
    """ Check the max duration limits for ICRH """
    CHECK_NAME = 'WOI 5.5: ICRH Power duration'

    # retrieve ICRH waveforms
    wfs = []
    for wf_name in wf_names:
        wfs.append(get_waveform(wf_name, waveforms))
    # retrieve the duration of the IC pulse
    ic_durations = []
    for wf in wfs:
        try:    
            ic_times = wf.times[np.nonzero(wf.values)]
            ic_durations.append(ic_times[-1] - ic_times[0])
        except IndexError as e:
            # case if no IC power is expected on an antenna
            pass
    if ic_durations:
        # check if one of the waveform is higher than the limits
        if np.any(np.array(ic_durations) > MAX_DURATION_WITH_IR):
            return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=f'max IC programmed duration: {np.amax(ic_durations):.3f} s > {MAX_DURATION_WITH_IR} s (no IR)')
        else:
            return Result(name=CHECK_NAME, code=Result.OK,
                          text=f'max IC programmed duration: {np.amax(ic_durations):.3f} s < {MAX_DURATION_WITH_IR} s (no IR)')
    else:
            return Result(name=CHECK_NAME, code=Result.OK,
                          text=f'No IC programmed')
        

# For debug and testing purpose
if __name__ == '__main__':
    from pppat.libpulse.waveform import get_waveform
    from pppat.libpulse.pulse_settings import PulseSettings
    # get pulse settings
    ps = PulseSettings(53726)

    wf_names = ['rts:WEST_PCS/Actuators/Heating/ICRH/power/1/waveform.ref',
                'rts:WEST_PCS/Actuators/Heating/ICRH/power/2/waveform.ref',
                'rts:WEST_PCS/Actuators/Heating/ICRH/power/3/waveform.ref']
    # retrieve ICRH waveforms
    wfs = []
    for wf_name in wf_names:
        wfs.append(get_waveform(wf_name, ps.waveforms))

    # integrate the power to get the energy
    E_MJ, P_IC_max = [], []
    for wf in wfs:
        E_MJ.append(np.trapz(wf.values, wf.times) / 1e6)  # in Mega Joules
        P_IC_max.append(np.amax(wf.values)/1e6)  # in Mega Watts

#    # test the pre test functions
#    res_p = check_WOI_5p5_power_limits(is_online=False, waveforms=ps.waveforms)
#    res_e = check_WOI_5p5_energy_limits(is_online=False, waveforms=ps.waveforms)
#    res_t = check_WOI_5p5_duration_limits(is_online=False, waveforms=ps.waveforms)

