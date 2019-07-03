# -*- coding: utf-8 -*-
"""
Check current PCS Top parameters
"""
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.waveform import get_waveform
from pppat.libpulse.utils import (pre_pulse_test, 
                                  is_ICRH_on_pulse, is_LHCD_on_pulse)
from pywed import tsmat
import numpy as np
import logging
logger = logging.getLogger(__name__)

# Nom des producteurs Top et valeurs nominales attendues
HEATING_SECURITY_PARAMETERS = 'DPCS;HEATING_PARA;HEATING_SECU'
HEATING_PERMISSIONS = 'DPCS;HEATING_PARA;HEATING_PERM'

# Default values given by Remy NOUAILLETAS 25/06/2019
HEATING_SECURITY_PARAMETERS_DEFAULT_VALUES = np.r_[
        1,  # 'LH Cu impurity protection enable',
        1,  # 'LH Fe impurity protection enable',
        1,  # 'IC Cu impurity protection enable',
        1,  # 'IC Fe impurity protection enable',
        0.05,  # 'power reduction time [sec]',
        0.2,  # 'power recovery time [sec]',
        0.25,  # 'max power reduction',
        1,  # 'delay before impurity event [sec]',
        1,  # 'ROI LH modulation enable',
        1,  # 'ROI IC modulation enable',
        10,  # 'maximal dhyb heartbeat errors',
        10,  # 'maximal dfci heartbeat errors',
        13,  # 'maximal dsurvie heartbeat errors',
        50  # 'maximal dwms heartbeat errors'
        ]    
HEATING_PERMISSIONS_DEFAULT_VALUES = np.r_[
        1e5,  # 'Minimal Ip for heating permission [A]',
        1,  #   'Minimal density for heating permission [1e19]',
        10,  #   'Maximal density for heating permission [1e19]',
        5e7,  #   'Maximal dIp/dt for heating permission [A/sec]',
        0,  #   'notching time for LH system [sec]',
        0  #   'notching time for IC system [sec]'],
        ]

# TODO: get the pulse number. If next pulse use 0 (current configuration)

# TODO: Securités IR
# - si chocs ohmiques: pas de securités IR
# - si chocs avec chauffages: juste un warning pour le moment 

# TODO: autorisations de chauffage et sécurités impuretés
# - non validation --> info si pas de puissance
# - non validation --> 
# - warning si puissance
# Sécurité		        Ohmique	    ICRH / LHCD on
# Impuretés		        Info		Warning
# Permission Flag		Info		Warning (interdiction de tir si notching time>0)
# ROI modulation		Info		Warning


def test_against_default_values(Top_productor, default_values, pulse_nb=0):
    """
    Returns a list of the tests which failed to pass against default values
    
    Parameters
    ----------
    Top_productor : str
        Name of the Top producer to check.
    default_values : numpy array
        Default values expected for default WEST plasma configuration

    Returns
    -------
    non_passed_tests : list of str
        List of failed tests. 

    """
    # get current Top configuration
    # NB: At the moment of this test, Top configuration should be frozen!
    parameter_descriptions, values = tsmat(pulse_nb, Top_productor)

    # for each security parameter check if equal to its associated default value
    passed_tests = np.isclose(values, default_values)
    
    # for all tests, extract the one not passed.
    not_passed_test = []
    for (desc, val, val_def, is_test_passed) in \
            zip(parameter_descriptions, values, default_values, passed_tests):
        if not is_test_passed: 
            not_passed_test.append(f'{desc}: flag is {is_test_passed} ')
    
    return not_passed_test

@pre_pulse_test
def check_Top_safety_heating_parameters(is_online=True, waveforms=None):
    """
    Check the heating permission values defined in Top producer 
        'DPCS;HEATING_PARA;HEATING_PERM'
    against default values.
    """
    CHECK_NAME = 'Top Heating Permissions'
    
    if not is_online:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text='Top configuration not available')        
    else:
        not_passed_test = test_against_default_values(
                HEATING_PERMISSIONS,
                HEATING_PERMISSIONS_DEFAULT_VALUES
                )

        if len(not_passed_test) == 0:  # no error
            return Result(name=CHECK_NAME, code=Result.OK,
                          text='All Top heating permission parameters nominal.')       
  
        else: #  if at least one test has not passed, return error
            return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=str(not_passed_test))

@pre_pulse_test
def check_Top_heating_permissions(is_online=True, waveforms=None):
    """
    Check the heating security parameter values defined in Top producer 
        'DPCS;HEATING_PARA;HEATING_SECU'
    against default values.
    """
    CHECK_NAME = 'Top Heating Securities'
    
    if not is_online:
        return Result(name=CHECK_NAME, code=Result.UNAVAILABLE,
                      text='Top configuration not available')        
    else:
        not_passed_test = test_against_default_values(
                HEATING_SECURITY_PARAMETERS,
                HEATING_SECURITY_PARAMETERS_DEFAULT_VALUES
                )

        if len(not_passed_test) == 0:  # no error
            return Result(name=CHECK_NAME, code=Result.OK,
                          text='All Top heating security parameters nominal.')       
            
        elif not_passed_test == ['ROI LH modulation enable: flag is False ',
                               'ROI IC modulation enable: flag is False ']:
            # WARNING JH 28/06/2019
            # IR safety is currently not available. 
            # The resulting tests thus give False, but this is normal
            # I've kept it as a warning in order to not forget these tests
            return Result(name=CHECK_NAME, code=Result.WARNING,
                          text=str(not_passed_test))
   
        else: #  if at least one test has not passed, return error
            return Result(name=CHECK_NAME, code=Result.ERROR,
                          text=str(not_passed_test))

if __name__ == '__main__':

    res=check_Top_safety_heating_parameters()
    print(res)
    