# -*- coding: utf-8 -*-
"""
WOI 3.2 : Toroidal magnetic field
"""
import pywed as pw
from pppat.libpulse.check_result import CheckResult as Result
import logging
logger = logging.getLogger(__name__)


def check_WOI_3p2_toroidal_coil_current(is_online=True, waveforms=None):
    """ Check the toroidal field coil current value """
    check_name = 'WOI 3.2: toroidal coil current'

    if is_online:
        Itor = pw.tsmat(0, 'EXP=T=S;General;Itor')
        logger.info(f'Toroidal coil current: {Itor} A')

        # TODO : margins ?
        if Itor < 600:
            return Result(name=check_name, code=Result.ERROR,
                          text=f'Toroidal coild current below 600 A: {Itor}')
        elif (Itor >= 600) and (Itor <= 1250):
            return Result(name=check_name, code=Result.OK,
                          text=f'Toroidal coil current between 600 and 1250 A: {Itor}')
        elif (Itor > 1250) and (Itor < 1350):
            return Result(name=check_name, code=Result.WARNING,
                          text=f'Toroidal coil current between 1250 and 1350 A: {Itor}')
        else:
            return Result(name=check_name, code=Result.ERROR,
                          text=f'Toroidal coil current above 1350 A: {Itor}')
    else:
        return Result(name=check_name, code=Result.UNAVAILABLE,
                      text='Toroidal coil current not available')
