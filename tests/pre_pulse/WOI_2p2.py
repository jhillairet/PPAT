# -*- coding: utf-8 -*-
"""
WOI 2.2 : In-vessel components water coolling loop (B30) - operation modes

pre-pulse tests
"""
import pywed as pw
from pppat.libpulse.check_result import CheckResult as Result
import logging
logger = logging.getLogger(__name__)


def check_WOI_2p2_B30_pressure(is_online=True, waveforms=None):
    """
    Check the B30 water loop pressure.
    """
    check_name = 'WOI 2.2: B30 pressure'

    if is_online:
        pB30 = pw.tsmat(0, 'EXP=T=S;General;PB30')
        logger.info(f'B30 pressure: {pB30:.1f}')

        if (pB30 < 15) or (pB30 > 24):  # TODO : margins ?
            return Result(name=check_name, code=Result.ERROR,
                          text=f'B30 Pressure below 15 bars: {pB30:.1f}')
        else:
            return Result(name=check_name, code=Result.OK,
                          text=f'B30 Pressure between 15 and 24 bars: {pB30:.1f}')
    else:
        return Result(name=check_name, code=Result.UNAVAILABLE,
                      text='B30 Pressure not available')
