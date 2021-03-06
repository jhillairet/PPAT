# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test

Plasma disruption tests
"""

import pywed as pw
import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import is_online, wait_cursor, post_pulse_test

import logging
logger = logging.getLogger(__name__)


class check_disruption_characteristic_time(Result):
    """
    Il existe plusieurs définitions du temps caractéristique d’une disruption
    τCQ. Une définition utilisée par l’ITPA [1,2,3] part du temps 80-20%
    τ80-20, durée pour passer d’une valeur du courant plasma de 80% à 20%.
    Si t80 et t20 sont respectivement les temps auxquels le courant plasma
    vaut 80% et 20% de sa valeur initiale avant disruption, alors le temps
    caractéristique de disruption τCQ peut être défini par :
         τCQ = 5/3 τ80-20
    où
         τ80-20 = t20 – t80
    Le facteur 5/3 permet une extrapolation du temps τ80-20 (qui est mesurable)
    à τCQ qui est une valeur théorique [3].

    [1] ITER Physics Expert Group on Disruptions, Plasma Control, and MHD and ITER Physics Basis Editors 1999 Nucl. Fusion 39 2251,
    [2] S.P. Gerhardt et al 2009 Nucl. Fusion 49 025005
    [3] Wesley J.C. 2006 Disruption characterization and databases activities for ITER, Proc. 21st Conf. on Fusion Energy, (Chengdu) (Vienna: IAEA) Paper IT/P1-21 https://fusion.gat.com/pubs-ext/IAEA06/A25588.pdf
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.

        self.name = 'Disruption characteristic time'
        self.default = False
        
        # Time at which the disruption is detected
        self.t_disruption = None
        self.t_20, self.t_80 = None, None
        self.ip_20, self.ip_80, self.delta_ip = None, None, None

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Plasma disruption Post-test
        """
        logger.info(f'Testing disruption for pulse {pulse_nb}')

        ip, t_ip = pw.tsbase(pulse_nb, 'SMAG_IP', nargout=2)
        # squeeze arrays for compatibility with np.gradient
        ip, t_ip = np.squeeze(ip), np.squeeze(t_ip)
        # time derivative of the plasma current
        dip_dt = np.gradient(ip, t_ip)
        # search for the maximum of the derivative :
        # this should matches the time of the disruption
        index_disruption = np.argmax(np.abs(dip_dt))
        self.t_disruption = t_ip[index_disruption]
        logger.info(f'Plasma disruption found at t={self.t_disruption}')
        # plasma current values few points before and after the disruption
        ip_before = ip[index_disruption - 20]

        # find the time and current at which we have 80% of ip before disruption
        idx_80 = np.abs(ip[index_disruption - 20:index_disruption] - 0.8*ip_before).argmin()
        self.t_80 = t_ip[index_disruption - 20:index_disruption][idx_80]
        self.ip_80 = ip[np.argmin(np.abs(t_ip - self.t_80))]
        # find the time and current at which we have 20% of ip after disruption
        idx_20 = np.abs(ip[index_disruption:index_disruption + 20] - 0.2*ip_before).argmin()
        self.t_20 = t_ip[index_disruption:index_disruption + 20][idx_20]
        self.ip_20 = ip[np.argmin(np.abs(t_ip - self.t_20))]
        
        t_80_20 = self.t_20 - self.t_80
        self.delta_ip = ip_before 

        text = f'Disruption @t={self.t_disruption:.2f}, char. time: t_80-20={t_80_20*1e3:.1f} ms from Ip={ip_before} kA'
        logger.info(text)
        self.text = text

        if t_80_20 < 1e-3:
            self.code = self.ERROR
        elif (t_80_20 > 1e-3) and (t_80_20 < 5e-3):
            self.code = self.WARNING
        else:
            self.code = self.OK


    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display
        """
        ip, t_ip = pw.tsbase(pulse_nb, 'SMAG_IP', nargout=2)

        fig, ax = plt.subplots()
        ax.plot(t_ip, ip)
        ax.grid(True)
        ax.set_xlabel('t [s]')
        ax.set_ylabel('Ip [kA]')
        # if the test has been prealably run, display additional information
        if self.t_20:
            # ax.axvline(self.t_disruption, color='gray', ls='--')
            ax.axvline(self.t_20, color='red', ls='--')    
            ax.axvline(self.t_80, color='red', ls='--')
            ax.axhline(self.ip_20, color='red', ls='--')    
            ax.axhline(self.ip_80, color='red', ls='--') 
        fig.show()



