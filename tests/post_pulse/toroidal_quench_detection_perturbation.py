# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test
"""
# modules python nécessaires
import pywed as pw
import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import post_pulse_test
from pppat.libpulse.utils_west import pulse_datetime
import pandas as pd

import logging  # pour ajouter des informations au log de PPPPAT
logger = logging.getLogger(__name__)

# Seuils d'erreurs
# Ecart aux seuils tension (2V): EcV = 2 - max(max(DV))
EcV_ERROR = 0
EcV_WARNING = 0.5
# Ecart au seuils de pression (2bar): EcP=2-max(max(Pres))
EcP_ERROR = 0
EcP_WARNING = 0.3

# TODO:
#Sécurité niveaux liquides : Soit NL la matrice des vecteurs colonnes des NLi
#Calcul de l’écart au seuil (1.95K) : EcNL=min(min(NL))-1.95
#-          Si EcNL superieur à 50E-3 K: OK
#-          Si EcNL entre 50E-3K et 0E-3 : Warning
#-          Si ENL négatif : Crosscheck obligatoire
#
#Sécurité températures : Soit T la matrice des vecteurs colonnes des Ti
#Calcul de l’écart au seuil (1.98K) : EcT=1.98-max(max(T))
#-          Si EcT superieur à 150E-3 K: OK
#-          Si EcT entre 150E-3K et 0E-3 : Warning
#-          Si EcT négatif : Crosscheck obligatoire

class check_toro_pression(Result):
    """
     Sécurité Pressions : Soit Pres la matrice des vecteurs colonnes des Pi
     Calcul de l’écart au seuil (2bar) : EcP=2-max(max(Pres))
     - Si EcP superieur à 0.3bar : OK
     - Si EcP entre 0.3bar et 0bar : Warning
     - Si EcP négatif : Crosscheck obligatoire
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.
        self.name = 'Toroidal Coils Pressure'
        self.default = True

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        date, t_start, t_end, _ = pulse_datetime(pulse_nb)
        Pres, tp = pw.tsbase('gpressions', date, t_start, t_end)

        EcP = 2 - np.amax(Pres)

        if EcP > EcP_WARNING:
            self.code = self.OK
            self.text = f'Max. Toroidal coils pressure {EcP:.1f} bar > {EcP_WARNING} bar'
        elif (EcP > EcP_ERROR) and (EcP <= EcP_WARNING):
            self.code = self.WARNING
            self.text = f'Max. Toroidal coils pressure {EcP:.1f} bar < {EcP_WARNING} bar'
        else:  # Ecv < 0:
            self.code = self.ERROR
            self.text = f'Max. Toroidal coils pressure {EcP:.1f} bar < {EcP_WARNING} bar'

    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display
        """
        # pulse date and times
        date, t_start, t_end, pulse_dt = pulse_datetime(pulse_nb)
        # start time in second from beginning of the day
        pulse_day = pd.to_datetime(pulse_dt.date())
        t_start_s = (pulse_dt - pulse_day).total_seconds()

        # toroidal coil voltages
        Pres, tp = pw.tsbase('gpressions', date, t_start, t_end)
        tpres = tp[:,0] - t_start_s

        ax = plot_toro_vs_Ip_RF(pulse_nb, tpres, Pres)
        ax.set_title('Seuil > 2b/Tempo 200ms')
        ax.set_ylabel('Pression [bar]')
        ax.axhline(2, color='r', lw=2)  # red line
        ax.fill_between(tpres, 2, 10, color='r', alpha=0.6)  # red zone above 2 bar


class check_toro_DeltaV(Result):
    """
     Sécurités tensions : Soit DV la matrice des vecteurs colonnes des DVi (18, N)
     Calcul de l’écart au seuil (2V) : EcV = 2 - max(max(DV))
       - Si EcV superieur à 0.5V : OK
       - Si EcV entre 0.5 et 0V : Warning
       - Si EcV négatif : Crosscheck obligatoire
    """
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.
        self.name = 'Toroidal Coils Voltage'
        self.default = True

    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        date, t_start, t_end, _ = pulse_datetime(pulse_nb)
        DV, tdv = toro_DeltaV(date, t_start, t_end)
        EcV = 2 - np.amax(DV)

        if EcV > EcV_WARNING:
            self.code = self.OK
            self.text = f'Max. Toroidal coils voltage {EcV:.1f} V > {EcV_WARNING} V'
        elif (EcV > EcV_ERROR) and (EcV <= EcV_WARNING):
            self.code = self.WARNING
            self.text = f'Max. Toroidal coils voltage {EcV:.1f} V  < {EcV_WARNING} V'
        else:  # Ecv < 0:
            self.code = self.ERROR
            self.text = f'Max. Toroidal coils voltage {EcV:.1f} V < {EcV_WARNING} V'

    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display
        """
        # pulse date and times
        date, t_start, t_end, pulse_dt = pulse_datetime(pulse_nb)
        # start time in second from beginning of the day
        pulse_day = pd.to_datetime(pulse_dt.date())
        t_start_s = (pulse_dt - pulse_day).total_seconds()

        # toroidal coil voltages
        DV, tdv = toro_DeltaV(date, t_start, t_end)
        tdv2 = tdv[:,0] - t_start_s

        ax = plot_toro_vs_Ip_RF(pulse_nb, tdv2, DV.T)
        ax.set_title('Seuil >2V/Tempo 1s')
        ax.set_ylabel('$\Delta$ V [V]')
        ax.axhline(2, color='r', lw=2)  # red line
        ax.fill_between(tdv2, 2, 10, color='r', alpha=0.6)  # red zone above 2V


def plot_toro_vs_Ip_RF(pulse_nb, toro_t, toro_y):
    """
    Plot a new subplot figure with plasma current, heating power and a third
    quantity described in the paramaters. Return the matlplotlib axe related
    to this third quantity
    """
    # Plasma current
    Ip, t1 = pw.tsbase(pulse_nb, 'smag_ip', '+', nargout=2)
    fig, axes = plt.subplots(3, 1, sharex=True)
    axes[0].plot(t1, Ip, color='k', lw=2, label='Ip [kA]')
    axes[0].set_ylabel('Current [kA]')
    axes[0].legend()

    # Puissance FCI
    try:
        Pfci, tfci = pw.tsbase(pulse_nb, 'SICHPTOT', '+', nargout=2)
        axes[1].plot(tfci[:,0], Pfci, lw=2, label='IC Power [kW]')
    except pw.PyWEDException:
        logger.info(f'No ICRH power pulse #{pulse_nb}')
                    
    # Puissance Hybride
    try:
        Phyb, thyb = pw.tsbase(pulse_nb, 'SHYBPTOT', '+', nargout=2)
        axes[1].plot(thyb[:,0], Phyb, lw=2, label='LH Power [kW]')
    except pw.PyWEDException:
        logger.info(f'No ICRH power pulse #{pulse_nb}')

    axes[1].set_ylabel('RF Power [kW]')
    axes[1].legend()
    axes[2].plot(toro_t, toro_y)
    axes[2].set_ylim(-2, 2.5)
    axes[2].set_xlabel('t [s]')
    # all figures to same xlim
    for ax in axes:
        ax.set_xlim(np.amin(t1), np.amax(t1))

    fig.show(True)

    return axes[2]

def toro_DeltaV(date, t_start, t_end):
    """
    Retourne les differences de tensions DeltaV issues du signal GVBT

    Parameters
    ----------
     - date: str
         date in format 'DD/MM/YY'.
     - t_start: str
         data start time in format 'hh:mm:ss'.
     - t_stop: str
         data end time in format 'hh:mm:ss'
     - pulse_dt: Timestamp (from pandas.Timestamp)
         WEST pulse datetime

    Return
    ------
     - DV: np.array
     - t: np.array
    """
    V, t = pw.tsbase('gvbt', date, t_start, t_end)

    # La numerotation des tensions est definie selon l'indexation de Matlab
    # ex dans matlab: V03 = V(:,3);
    DV1 = V[:,1] - V[:,3]  # DeltaV1 = V2 - V4
    DV2 = V[:,5] - V[:,17]  # DeltaV12= V6 - V18
    DV3 = V[:,7] - V[:,9]  # DeltaV3 = V8 - V10
    DV4 = V[:,7] - V[:,11]  # DeltaV4 = V8 - V12
    DV5 = V[:,13] - V[:,17]  # DeltaV5 = V14 - V18
    DV6 = V[:,3] - V[:,15]  # DeltaV6 = V4 - V16
    DV7 = V[:,0] - V[:,4]  # DeltaV7 = V1 - V5
    DV8 = V[:,2] - V[:,14]  # DeltaV7 = V3 - V15
    DV9 = V[:,6] - V[:,10]   # DeltaV7 = V7 - V11
    DV10 = V[:,8] - V[:,16]  # DeltaV7 = V9 - V17
    DV11 = V[:,10] - V[:,12]  # DeltaV7 = V11 - V13
    DV12 = V[:,4] - V[:,6]  # DeltaV7 = V5 - V7
    DV13 = V[:,2] - V[:,8]  # DeltaV7 = V3 - V9
    DV14 = V[:,0] - V[:,12]  # DeltaV7 = V1 - V13
    DV15 = V[:,14] - V[:,16]  # DeltaV7 = V15 - V17
    DV16 = V[:,1] - V[:,9]  # DeltaV7 = V2 - V10
    DV17 = V[:,5] - V[:,11]  # DeltaV7 = V6 - V12
    DV18 = V[:,13] - V[:,15]  # DeltaV7 = V14 - V16

    DV = np.array(
            [DV1, DV2, DV3, DV4, DV5, DV6, DV7, DV8, DV9, DV10,
             DV11, DV12, DV13, DV14, DV15, DV16, DV17, DV18])
    return DV, t


if __name__ == '__main__':
    # testing
    pulse = 53640
    test_toro_DeltaV = check_toro_DeltaV()
    test_toro_pression = check_toro_pression()
