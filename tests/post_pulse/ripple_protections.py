# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test

Ripple protection heat load (WOI 6.6)
"""

import pywed as pw
import numpy as np
import matplotlib.pyplot as plt

from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import post_pulse_test

# Seuils de puissance en kW
P_ERROR = 25
P_WARNING = 20


# Design value of the steady state heat load
# to each plane ripple protection in kW
def ripple_protection_loss(ip, nl, p_lh):
    """
    Return the power loss on the ripple protection according the scale law:
        P_rp [kW] = 29 * p_lh [MW]**1.85 * ip [MA]**1.5 / nl[10^19 m^-2]**2.2
    This power should be < 25 kW in steady-state for safety.

    Parameters
    ----------
     - ip: np.array
         plasma current in MA
     - nl: np.array
         central lineic density in 10^19 m^-2
     - plh: np.array
         Total Coupled LH power in MW

    Return
    -------
     - P_rp: np.array
         Ripple protection power loss in kW

    """
    P_rp = 29 * p_lh**1.85 * ip**1.5 / nl**2.2  # should be < 25
    return P_rp


def ripple_protection_loss_for_pulse(pulse):
    """
    Return the power loss on the ripple protection in kW

    Parameters
    ----------
     - pulse: int
         WEST pulse number

    Return
    -------
     - P_rp: np.array
         Ripple protection power loss in kW
     - t_ip: np.array
         Time array from plasma current
     - ip: np.array
         Plasma current
     - nl: np.array
         Central Lineic density interpolated on plasma current timebase
     - p_lh: np.array
         Total coupled lH power interpolated on plasma current timebase
    """
    # retrieve plasma current, total coupled LH power and lineic density
    ip, t_ip = pw.tsbase(pulse, 'SMAG_IP', nargout=2)
    p_lh, t_lh = pw.tsbase(pulse, 'SHYBPTOT', nargout=2)
    nl, t_nl = pw.tsbase(pulse, 'GINTLIDRT%3', nargout=2)

    # interpolate the data based on the plasma current time
    ip = np.squeeze(ip)
    nl = np.interp(np.squeeze(t_ip), np.squeeze(t_nl), np.squeeze(nl))
    p_lh = np.interp(np.squeeze(t_ip), np.squeeze(t_lh), np.squeeze(p_lh))

    # current shot power loss in kW
    P_rp = ripple_protection_loss(ip/1e3, nl, p_lh)
    # replace inf (where density is measured as 0) to Nan
    P_rp[np.isinf(P_rp)] = np.nan

    return P_rp, t_ip, ip, nl, p_lh


class check_ripple_protection(Result):
    """
    Test the heat load deposited on the ripple protection according to
    the scale law defined in WOI 6.6:
        P_rp [kW] = 29 * p_lh [MW]**1.85 * ip [MA]**1.5 / nl[10^19 m^-2]**2.2
    This power should be < 25 kW
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.

        # nom du test. À modifier
        self.name = 'Ripple proctection heat load'

        # Est-ce un test à réaliser par défaut ? True/False. À modifier.
        self.default = True

    # méthode de test. À laisser et compléter.
    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Plasma disruption Post-test
        """

        P_rp, t_ip, ip, nl, p_lh = ripple_protection_loss_for_pulse(pulse_nb)

        # maximum power without NaN
        P_rp_max = np.nanmax(P_rp)

        if np.isnan(P_rp_max):
            self.code = self.BROKEN
            self.text = f'Maw Ripple loss: {P_rp_max:.1f} kW return an error?'
        else:
            if P_rp_max >= P_ERROR:
                self.code = self.ERROR
                self.text = f'Max Ripple loss: {P_rp_max:.1f} kW > {P_ERROR} kW '
            elif (P_rp_max >= P_WARNING) and (P_rp_max < P_ERROR):
                self.code = self.WARNING
                self.text = f'Max Ripple loss: {P_rp_max:.1f} kW > {P_WARNING} kW '
            else:
                self.code = self.OK
                self.text = f'Max Ripple loss: {P_rp_max:.1f} kW < {P_WARNING} kW'

    # La méthode suivante sert à tracer des choses utiles. À modifier.
    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display
        """
        P_rp, t_ip, ip, nl, p_lh = ripple_protection_loss_for_pulse(pulse_nb)

        # Plot everything for the pulse
        fig, axes = plt.subplots(4, 1, sharex=True)
        axes[0].set_title(f'WEST #{pulse_nb}')
        axes[0].plot(t_ip, ip, label='Plasma Current [kA]')
        axes[1].plot(t_ip, p_lh, label='Total Coupled LH Power [MW]')
        axes[2].plot(t_ip, nl, label='Lineic Density [10^19 m^-2]')
        axes[3].plot(t_ip, P_rp, label='Ripple Loss [kW]')
        for ax in axes:
            ax.legend()
        fig.show(True)

        # plot the specific WOI figure (P_rp = 25 kW)
        fig, ax = plt.subplots()
        _nl = np.linspace(1, 6, num=101)
        _ips = [0.4, 0.6, 0.8, 1.0]
        for _ip in _ips:
            _p_lh = (25/29/_ip**1.5*_nl**2.2)**(1/1.85)
            ax.plot(_nl, _p_lh, label=f'Ip={_ip} MA', lw=2)
        # Add the current plot points to the current figure
        ax.plot(nl, p_lh, '.', label=f'WEST #{pulse_nb}')

        ax.set_ylim(1, 7)
        ax.set_xlim(1, 6)
        ax.grid(True)
        ax.legend()
        ax.set_xlabel('nl [$m^{-2}$]')
        ax.set_ylabel('P LH [MW]')

        fig.show(True)

        
if __name__ == '__main__':
    # testing 
    pulse = 53640
    test_ripple = check_ripple_protection()
    test_ripple.test(pulse)

    



