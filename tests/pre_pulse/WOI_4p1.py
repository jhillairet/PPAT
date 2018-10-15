# -*- coding: utf-8 -*-
"""
WOI 4.1 : plasma density
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
import numpy as np
import logging
logger = logging.getLogger(__name__)


def check_WOI_4p1_plasma_density(is_online=False, waveforms=None):
    """ Check the expected plasma density values """
    CHECK_NAME = 'WOI 4.1: plasma density'
    DENSITY_LOWER_LIMIT = 1e18


    # retrieve the density waveform
    waveform_name = 'rts:WEST_PCS/Actuators/Gas/REF1/waveform.ref'
    waveform = get_waveform(waveform_name, waveforms)

    if not waveform:
        raise(ValueError(f'waveform {waveform_name} not found!?'))
    else:
        # check the min density (excluding 0 values)
        logger.info(waveform.values)
        n_min = 1e18*np.amin(waveform.values[np.nonzero(waveform.values)])
        logger.info(f'Min density from waveform: {n_min}')

        # TODO : retourner le temps & le segment de l'erreur (si erreur)
        if n_min < DENSITY_LOWER_LIMIT:
            return Result(name=CHECK_NAME, code=Result.WARNING,
                          text='Plasma density below minimum limit (risk of runaway electrons)')
        else:
            return Result(name=CHECK_NAME, code=Result.OK,
                          text='Plasma density OK')