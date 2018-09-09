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
        logger.info(f'B30 pressure:{PB30}')
        # TODO 
        return Result(name='WOI 2.2: (dummy)', code=Result.OK, 
                      text='dummy test')
    else:
        return Result(name='WOI 2.2: (dummy)', code=Result.UNAVAILABLE, 
                      text='dummy test')
