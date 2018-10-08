# -*- coding: utf-8 -*-
"""
WOI 1.1 pre-pulse tests
"""
import pywed as pw
from pppat.libpulse.check_result import CheckResult as Result
import logging
logger = logging.getLogger(__name__)


def check_WOI_1p1_torus_pressure(is_online=True):
    """ Check the torus pressure before a pulse """
    check_name = 'WOI 1.1: torus pressure'

    if is_online:
        p = pw.tsmat(0, 'EXP=T=S;General;TTORE')
        torus_pressure = p[0]*10**(p[1])
        logger.info(f'Torus pressure: {torus_pressure} Pa')

        if torus_pressure < 1e-5:
            return Result(name=check_name, code=Result.OK,
                          text='Torus pressure OK')

        if (torus_pressure >= 1e-5) and (torus_pressure < 1e-4):
            return Result(name=check_name, code=Result.WARNING,
                          text='Torus pressure above lower limit')

        else:
            return Result(name=check_name, code=Result.ERROR,
                          text='Torus pressure above upper limit')
    else:
        return Result(name=check_name, code=Result.UNAVAILABLE,
                      text='Torus pressure not available')


def test_WOI_1p1_torus_pressure_offline():
    res = check_WOI_1p1_torus_pressure(is_online=False)
    assert res.code == Result.UNAVAILABLE


def test_WOI_1p1_torus_pressure_online():
    res = check_WOI_1p1_torus_pressure(is_online=True)
    assert res.code == Result.ERROR or Result.WARNING or Result.OK
