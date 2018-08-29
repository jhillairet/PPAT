# -*- coding: utf-8 -*-
"""
WOI 1.1 pre-pulse tests
"""
import pywed as pw

#from pppat.libpulse.check_result import CheckResult
from pppat.libpulse.DCS_settings import DCSSettings


    
def test_WOI_1p1_torus_pressure():
    """ Check the torus pressure before a pulse """
    p = pw.tsmat(0,'EXP=T=S;General;TTORE')
    torus_pressure = p[0]*10**(p[1])
    
    if torus_pressure < 1e-5:
        return True
    else:
        raise ValueError('Pressure too high')