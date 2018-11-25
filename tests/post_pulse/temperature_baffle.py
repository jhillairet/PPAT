# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test

Baffle temperature (WOI 6.3)
"""

import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import post_pulse_test
from pppat.libpulse.utils_west import temperature_from_pulse

import logging
logger = logging.getLogger(__name__)

# Seuils de temperature max d'alertes en °C
T_ERROR = 450
T_WARNING = 300

# Baffle Thermocouples
sig_TCs_baffle = ['GETC_BAFF_2A',  # TC baffle Q2A
                  'GETC_BAFF_5A']  # TC baffle Q5A


class check_temperature_baffle(Result):
    """
    The steady-state temperature of the baffle should be < 450°C
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.

        self.name = 'Baffle Temperature'
        self.default = True

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Get the Baffle max. temperature measured during the shot.

        This temperature should be below 450°C.
        """
        max_temp = []
        for sig in sig_TCs_baffle:
            T, t = temperature_from_pulse(pulse_nb, sig)
            max_temp.append(np.amax(T))

        max_max_temp = np.amax(max_temp)

        if max_max_temp > T_ERROR:
            self.code = self.ERROR
            self.text = f'Baffle max. temp. above {T_ERROR}°C: {max_max_temp:.0f}°C'
        elif max_max_temp > T_WARNING:
            self.code = self.WARNING
            self.text = f'Baffle max. temp. above {T_WARNING}°C: {max_max_temp:.0f}°C'
        else:  # I guess it is OK then
            self.code = self.OK
            self.text = f'Baffle max. temp. : {max_max_temp:.0f}°C'

    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display

        Display the Baffle temperatures during the pulse.
        """
        fig, axes = plt.subplots(len(sig_TCs_baffle), sharex=True)
        title = f'WEST #{pulse_nb} Baffle Temperature'
        fig.canvas.set_window_title(title)

        for (sig, ax) in zip(sig_TCs_baffle, axes):
            T, t = temperature_from_pulse(pulse_nb, sig)
            ax.plot(t, T)
            ax.set_title(sig)
            # Display thresholds without changing the ylim
            ylim = ax.get_ylim() 
            ax.axhline(T_ERROR, lw=2, ls='--', color='red')
            ax.axhline(T_WARNING, lw=2, ls='--', color='orange')
            ax.set_ylim(ylim)

        ax.set_xlabel('t [s]')
        fig.show()
