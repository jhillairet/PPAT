# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test

Lower divertor temperature (WOI 6.1)
"""

import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import post_pulse_test
from pppat.libpulse.utils_west import temperature_from_pulse

import logging
logger = logging.getLogger(__name__)

# Seuils de temperature max d'alertes en °C
T_ERROR = 1200
T_WARNING = 800

# Lower Divertor Thermocouples
sig_TCs_divertor = ['GETC_ISP_6A',  # TC inner strike point Q6A
                    'GETC_OSP_6A',  # TC outer strike point Q6A
                    'GETC_OSP_1A',  # TC outer strike point Q1A
                    'GETC_RIPL_6A']  # TC toroidaux Q6A

# TODO: Bragg Grating Fibers

class check_temperature_divertor_lower(Result):
    """
    The lower divertor during WEST phase 1 consists in both actively cooled
    ITER monoblocks and inertial W-coated graphite PFU.

    The operational limit on W monoblocks is 1200°C

    The maximum temperature increase during

    A new pulse may be launched only if T<200°C
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.

        self.name = 'Lower Divertor Temperature'
        self.default = True

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Get the lower divertor max. temperature measured during the shot.

        This temperature should be below 1200°C.
        """
        max_temp = []
        for sig in sig_TCs_divertor:
            T, t = temperature_from_pulse(pulse_nb, sig)
            # replace unrealistic temperatures (<10°C) by -1
            T2 = np.where(T > 10, T, -1)
            
            max_temp.append(np.amax(T2))

        max_max_temp = np.amax(max_temp)

        if max_max_temp > T_ERROR:
            self.code = self.ERROR
            self.text = f'Lower divertor max. temp. above {T_ERROR}°C: {max_max_temp:.0f}°C'
        elif max_max_temp > T_WARNING:
            self.code = self.WARNING
            self.text = f'Lower divertor max. temp. above {T_WARNING}°C: {max_max_temp:.0f}°C'
        else:  # I guess it is OK then
            self.code = self.OK
            self.text = f'Lower divertor max. temp. : {max_max_temp:.0f}°C'

    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display

        Display the lower divertor temperatures during the pulse.
        """
        fig, axes = plt.subplots(len(sig_TCs_divertor), sharex=True)
        title = f'WEST #{pulse_nb} Lower Divertor Temperature'
        fig.canvas.set_window_title(title)

        for (sig, ax) in zip(sig_TCs_divertor, axes):
            T, t = temperature_from_pulse(pulse_nb, sig)
            # replace unrealistic temperatures (<10°C) by -1
            T2 = np.where(T > 10, T, np.NaN)
            t2 = np.where(T > 10, t, np.NaN)
            ax.plot(t2, T2, '.')
            ax.set_title(sig)
            # Display thresholds without changing the ylim
            ylim = ax.get_ylim() 
            ax.axhline(T_ERROR, lw=2, ls='--', color='red')
            ax.axhline(T_WARNING, lw=2, ls='--', color='orange')
            ax.set_ylim(ylim)
        
        ax.set_xlabel('t [s]')
        fig.show()
