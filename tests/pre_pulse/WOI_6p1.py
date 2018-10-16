# -*- coding: utf-8 -*-
"""
WOI 6.1 : lower divertor PFUs
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
import numpy as np
import logging
logger = logging.getLogger(__name__)


def check_WOI_6p1(is_online=False, waveforms=None):
    """ Check the duration of the X-point phase """
    CHECK_NAME = 'WOI 6.1: lower PFUs'
    MAXIMUM_XPOINT_DURATION = 10  # s
    
    waveform_name = 'rts:WEST_PCS/Actuators/Poloidal/IXb/waveform.ref'
    waveform = get_waveform(waveform_name, waveforms)

    if not waveform:
        raise(ValueError(f'waveform {waveform_name} not found!?'))
    else:       
        IXb = waveform.values
        t_IXb = waveform.times
        nonzero_idx = np.argwhere(IXb != 0)
        
        logger.info(np.array(np.where(IXb != 0)).squeeze() )
        logger.info(t_IXb[nonzero_idx].squeeze() )
        
        # TODO : the following fails. 
        if len(nonzero_idx) > 0:
            #FirstNonZero_index = nonzero_idx[0]
            #LastZero_index = FirstNonZero_index - 1
            TimeXpointStart = np.interp(0.0, IXb[nonzero_idx], t_IXb[nonzero_idx])
            LastNonZero_indexes = np.where(IXb > 0)[0]
            LastNonZero_index = LastNonZero_indexes[-1]
            FinalZero_index = LastNonZero_index + 1
            TimeXpointStop = np.interp(0.0,IXb[LastNonZero_index:FinalZero_index],t_IXb[LastNonZero_index:FinalZero_index])
            duration_Xpoint = TimeXpointStop - TimeXpointStart
    
        else:
            duration_Xpoint = 0.0
            
        if duration_Xpoint > MAXIMUM_XPOINT_DURATION:
            return Result(name=CHECK_NAME, code=Result.ERROR,
                          text='Lower X-point phase too long: Lower divertor coils ON during')
        else:
            return Result(name=CHECK_NAME, code=Result.OK,
                          text='Lower X-point phase duration OK')
