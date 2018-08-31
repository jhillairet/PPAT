# -*- coding: utf-8 -*-
"""
WOI 1.1 pre-pulse tests
"""
import pywed as pw
from pppat.libpulse.check_result import CheckResult as Result
import logging
logger = logging.getLogger(__name__)

    
def check_WOI_2p2(is_online=True):

    if is_online:
        PB30 = pw.tsmat(0,'EXP=T=S;General;PB30')
        logger.info(PB30)
        # TODO 
        return Result(name='WOI 2.2', code=Result.OK)
    else:
        return Result(name='WOI 2.2', code=Result.UNAVAILABLE)
