# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test

Lower divertor B30 delta temperature (WOI 6.1&7.4)
"""

import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import post_pulse_test
from pppat.libpulse.utils_west import temperature_from_pulse

import logging
logger = logging.getLogger(__name__)

# Seuils de temperature max d'alertes en °C
T_ERROR = 10.3
T_WARNING = T_ERROR - 3

# Lower Divertor Thermocouples
sig_B30_low_div = ['GCAL_T_LDIVA',  # outlet low divertor A
                   'GCAL_T_LDIVB']  # outlet low divertor B

sig_B30_global = ['SCAL_T_TEGLO']  # globale inlet temperature
delta_ldivA =[]
delta_ldivB=[]

sig_B30_delta = [delta_ldivA, delta_ldivB] #delta temperature between outlets and globale  
   
class check_temperature_divertor_lower(Result):
    """
    The lower divertor during WEST phase 1 consists in both actively cooled
    ITER monoblocks and inertial W-coated graphite PFU.

    The operational limit on W monoblocks is 1200°C

    The maximum temperature increase of temperature during a pulse is defined in WOI7.4. 
    For lower divertor the increase limit is 10.3

        """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.

        self.name = 'Low Div B30 increase of temperature'
        self.default = True

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Get the lower divertor global inlet and outlets.

        The delta must stay below 10.3.
        """
      
        max_increase = []
        G , t = temperature_from_pulse(pulse_nb, 'SCAL_T_TEGLO')
        
        for sig in sig_B30_low_div:
            T, t = temperature_from_pulse(pulse_nb, sig)
            max_increase.append(np.nanmax(T-G))
            max_max_increase = np.nanmax(max_increase)

        if max_max_increase > T_ERROR:
            self.code = self.ERROR
            self.text = f'Lower divertor B30 max. increase {T_ERROR}°C: {max_max_increase:.0f}°C'
        elif max_max_increase > T_WARNING:
            self.code = self.WARNING
            self.text = f'Lower divertor B30 max. increase {T_WARNING}°C: {max_max_increase:.0f}°C'
        else:  # I guess it is OK then
            self.code = self.OK
            self.text = f'Lower divertor B30 max. increase : {max_max_increase:.0f}°C'

    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display

        Display the lower divertor temperatures during the pulse.
        """
        fig, axes = plt.subplots(len(sig_B30_low_div), sharex=True)
        title = f'WEST #{pulse_nb} Lower Divertor Temperature'
        fig.canvas.set_window_title(title)
        G , t = temperature_from_pulse(pulse_nb, 'SCAL_T_TEGLO')

        for (sig, ax) in zip(sig_B30_low_div, axes):
            T, t = temperature_from_pulse(pulse_nb, sig)
            ax.plot(t, T-G)
            ax.set_title(sig)
            # Display thresholds without changing the ylim
            ylim = ax.get_ylim() 
            ax.axhline(T_ERROR, lw=2, ls='--', color='red')
            ax.axhline(T_WARNING, lw=2, ls='--', color='orange')
            ax.set_ylim(ylim)
        
        ax.set_xlabel('t [s]')
        fig.show()
