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
wf_names = ['rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref',
            'rts:WEST_PCS/Actuators/Heating/LHCD/power/2/waveform.ref']

@pre_pulse_test
def check_WOI_5p2_antenna_max_powers(is_online=False, waveforms=None):
    CHECK_NAME = 'WOI 5.2: LHCD Antenna max powers'
    # retrieve LHCD waveforms
    wfs = []
    for wf_name in wf_names:
        wfs.append(get_waveform(wf_name, ps.waveforms))

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

# For debug and testing purpose
if __name__ == '__main__':
    from pppat.libpulse.waveform import get_waveform
    from pppat.libpulse.pulse_settings import PulseSettings
    # get pulse settings
    ps = PulseSettings(53725)


    # retrieve LHCD waveforms
    wfs = []
    for wf_name in wf_names:
        wfs.append(get_waveform(wf_name, ps.waveforms))

    # integrate the power to get the energy
    E_MJ, P_LH_max = [], []
    for wf in wfs:
        E_MJ.append(np.trapz(wf.values, wf.times) / 1e6)  # in Mega Joules
        P_LH_max.append(np.amax(wf.values)/1e6)  # in Mega Watts

