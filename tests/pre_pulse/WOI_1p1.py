# -*- coding: utf-8 -*-
"""
WOI 1.1 pre-pulse tests
"""
import pywed as pw
from pppat.libpulse.check_result import CheckResult as Result
import logging
logger = logging.getLogger(__name__)


def check_WOI_1p1_torus_pressure(is_online=True, waveforms=None):
    """ Check the torus pressure before a pulse """
    CHECK_NAME = 'WOI 1.1: torus pressure'
    PRESSURE_LIMIT_LOW = 1e-5
    PRESSURE_LIMIT_HIGH = 1e-4

    if is_online:
        p = pw.tsmat(0, 'EXP=T=S;General;TTORE')
        torus_pressure = p[0]*10**(p[1])
        logger.info(f'Torus pressure: {torus_pressure} Pa')

        if torus_pressure < PRESSURE_LIMIT_LOW:
            return Result(name=CHECK_NAME, code=Result.OK,
                          text=f'Torus pressure {torus_pressure:.1e} Pa < {PRESSURE_LIMIT_LOW} Pa: OK)')
        elif torus_pressure > PRESSURE_LIMIT_HIGH:
            return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=f'Torus pressure {torus_pressure:.1e} Pa > {PRESSURE_LIMIT_HIGH} Pa: ERROR')            
        elif (torus_pressure >= PRESSURE_LIMIT_LOW) and \
            (torus_pressure < PRESSURE_LIMIT_HIGH):
            return Result(name=CHECK_NAME, code=Result.WARNING,
                          text=f'Torus pressure {torus_pressure:.1e} Pa > {PRESSURE_LIMIT_LOW} Pa: WARNING')


    else:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text='Torus pressure not available')


def test_WOI_1p1_torus_pressure_offline():
    res = check_WOI_1p1_torus_pressure(is_online=False)
    assert res.code == Result.UNAVAILABLE


def test_WOI_1p1_torus_pressure_online():
    res = check_WOI_1p1_torus_pressure(is_online=True)
    assert res.code == Result.ERROR or Result.WARNING or Result.OK
