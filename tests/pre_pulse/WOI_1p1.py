# -*- coding: utf-8 -*-
"""
WOI 1.1 pre-pulse tests
"""
import pywed as pw
import numpy as np
from pppat.libpulse.check_result import CheckResult as Result
import logging
logger = logging.getLogger(__name__)


# Update JH 21/12/2020 with WOI 1.1 validated in 11/2020:
# The residual total pressure in the vacuum vessel (measured by the J11A signal from the pumping tank
# pressure gauges) must be checked at the beginning of each day and before launching each pulse. If its
# value is greater than the value given in the table below, a deeper analysis of the residual vacuum must
# be performed before any plasma initiation attempt (possible vacuum leak).
#
# Wall temperature      Max. pressure               Max. pressure
# (B30 temp)            (at beg. of each day)       (at new plasma)
# 40°C                  8x10-6 Pa                   5x10-5 Pa
# 70°C                  1.5x10-5 Pa                 6x10-5 Pa
# 120°C                 2.2x10-5 Pa                 8x10-5 Pa
# 150°C                 3.7x10-5 Pa                 10-4 Pa
#
# only take into account the max pressure before new plasma
MAX_PRESSURE_vs_TEMPERATURE = np.array([
        [40, 5e-5],
        [70, 6e-5],
        [120, 8e-5],
        [150, 1e-4]
])

def interpolate_pressure(temperature: float) -> float:
    """
    Interpolate the maximum pressure limit for a given temperature.

    Arguments
    ---------
    temperature: float
        Temperature to interpolate the max pressure to

    Returns
    --------
    pressure_max: float
        Maximum Pressure Limit

    """
    pressure_max = np.interp(temperature, MAX_PRESSURE_vs_TEMPERATURE[:,0], MAX_PRESSURE_vs_TEMPERATURE[:,1])
    return pressure_max

def check_WOI_1p1_torus_pressure(is_online=True, waveforms=None):
    """ Check the torus pressure before a pulse """
    CHECK_NAME = 'WOI 1.1: torus pressure'

    if is_online:
        p = pw.tsmat(0, 'EXP=T=S;General;TTORE')
        torus_pressure = p[0]*10**(p[1])
        logger.info(f'Current Torus Pressure: {torus_pressure} Pa')

        t_B30 = pw.tsmat(0, 'EXP=T=S;General;TB30')
        logger.info(f'Current Vessel Temperature (B30): {t_B30} deg')

        pressure_max = interpolate_pressure(t_B30)     

        if torus_pressure < pressure_max:
            return Result(name=CHECK_NAME, code=Result.OK,
                          text=f'Torus pressure {torus_pressure:.1e} Pa < {pressure_max:.1e} Pa for {t_B30:.1f} deg: OK)')
        elif torus_pressure > pressure_max:
            return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=f'Torus pressure {torus_pressure:.1e} Pa > {pressure_max:.1e} Pa for {t_B30:.1f} deg: ERROR')            

    else:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text='Torus pressure not available')


def test_WOI_1p1_torus_pressure_offline():
    res = check_WOI_1p1_torus_pressure(is_online=False)
    assert res.code == Result.UNAVAILABLE


def test_WOI_1p1_torus_pressure_online():
    res = check_WOI_1p1_torus_pressure(is_online=True)
    assert res.code == Result.ERROR or Result.WARNING or Result.OK
