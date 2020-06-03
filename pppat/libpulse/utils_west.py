# -*- coding: utf-8 -*-
"""
Convenient WEST data functions
"""
import socket
import numpy as np
import pandas as pd
import pywed as pw
from datetime import datetime
from IRFMtb import tsdernier_choc
from scipy.signal import savgol_filter  # for smooth

def is_online():
    """
    Return the online status (True or False).

    Returns
    -------
    status: Boolean
            The online status True is the IRFM database can be
            reached on the network. False if not ('offline' mode).
    """
    host = '10.8.86.1'  # deneb address
    port = 5880
    # create a dummy connection to test the server reachability
    try:
        s = socket.create_connection((host, port), timeout=2)
        return True
    except socket.error:
        return False


def last_pulse_nb():
    """ Return the latest WEST pulse number """
    if is_online():
        return tsdernier_choc()
    else:
        return -1

def pulse_datetime(pulse_nb):
    """
    Return the date, start and end times of a WEST pulse

    Parameters
    ----------
     - pulse_nb: int
         WEST pulse number

    Return
    ------
     - date: str
         date in format 'DD/MM/YY'.
     - t_start: str
         data start time in format 'hh:mm:ss'.
     - t_stop: str
         data end time in format 'hh:mm:ss'
     - pulse_dt: Timestamp (from pandas.Timestamp)
         WEST pulse datetime

    NB: to convert the pulse start time into cumuluated seconds from midnight:
        # pulse date Timestamp for reference (at 00:00:00)
        pulse_day = pd.to_datetime(pulse_dt.date())
        # duration between reference and pulse start in s
        t_start_s = (pulse_dt - pulse_day).total_seconds()
    """
    # Durée entre ORIGINE et finacquisition corrected from IGNITRON
    t_fin_acq = pw.tsmat(pulse_nb, 'FINACQ|1')[0]

    # date du LANCEMENT du choc
    date_apilote = pw.tsmat(pulse_nb, 'APILOTE;+VME_PIL;Date_Choc')
    pulse_dt = pd.to_datetime(date_apilote)
    # date conversion in 'dd/MM/yy'
    pulse_date = pulse_dt.strftime('%d/%m/%y')
    t_start = pulse_dt.strftime('%H:%M:%S')
    t_stop = (pulse_dt + pd.Timedelta(t_fin_acq, unit='s')).strftime('%H:%M:%S')

    return pulse_date, t_start, t_stop, pulse_dt


def temperature_from_pulse(pulse_nb, signame):
    """
    return a temperature signal from DCALOR during a WEST pulse

    Parameters
    ----------
     - pulse_nb: int
         pulse number
     - signame: str
         signal name

    Return
    -------
     - T: np.array
         temperature array
     - t: np.array
         time array in second. t=0 correspond to pulse DCALOR ORIGIN

    """
    pulse_date, t_start, t_stop, pulse_dt = pulse_datetime(pulse_nb)
    # Récupération de la datation de DCALOR (en ms depuis minuit)
    # lorsqu'il recoit ORIGINE (commence l'acquisition)
    # Instant qui définit t=0s
    t_origine = int(pw.tsmat(pulse_nb, 'DCALOR;PARAM;ORIGINE'))/1e3  # in s

#    # Convertit t_origine en HH:MM:SS
#    t_origine_str = (pd.to_datetime(pulse_date) + pd.Timedelta(t_origine, unit='s')).strftime('%H:%M:%S')

    # Durée entre ORIGINE et finacquisition corrected from IGNITRON
    t_fin_acq = pw.tsmat(pulse_nb, 'FINACQ|1')[0]

#    # Heure de la fin d'acquisition au format HH:MM:SS
#    t_fin_acq_str = (pd.to_datetime(pulse_date) + pd.Timedelta(t_origine, unit='s') + pd.Timedelta(t_fin_acq, unit='s')).strftime('%H:%M:%S')

    # La base de temps DCALOR est, disons, "perturbée". Un appel direct de
    # tsbase utilisant l'heure de début et de fin de choc renvoie parfois
    # des vecteurs temps incohérents. Pour palier cela, on télécharge une période
    # de temps plus grande (ici +/- 1 heure)
    # et on filtre ensuite les données relatives au choc.
    t_before = (pulse_dt - pd.Timedelta(hours=1)).strftime('%H:%M:%S')
    t_after = (pulse_dt + pd.Timedelta(hours=1)).strftime('%H:%M:%S')
    T, t = pw.tsbase(signame, pulse_date, t_before, t_after)

    idx = (t > t_origine) & (t < t_origine + t_fin_acq)
    t2 = t[idx[:,0]] - t_origine -32 #  ms (absolute) -> s (relative)
    T2 = T[idx[:,0]]

    # keep only physical temperatures (>10°C)
    t2 = np.where(T2 > 10, t2, np.NaN)
    T2 = np.where(T2 > 10, T2, np.NaN)

    return T2, t2


def continuous_signal_from_time(signame, date=None, t_start='00:01:00', t_stop='23:59:00'):
    """
    return a continuous acquisition signal from two dates

    Parameters
    ----------
     - signame: str
         signal name
     - date: str
         date in format 'DD/MM/YY'. Default value: date of the day
     - t_start: str
         data start time in format 'hh:mm:ss'. Default value: 00:01:00
     - t_stop: str
         data end time in format 'hh:mm:ss'. Default value: 23:59:00

    Return
    -------
     - T: np.array
         signal
     - t: np.array
         time vector of the signal

    """
    if not date:
        date = datetime.now().strftime('%d/%m/%y')

    T, t = pw.tsbase(signame, date, t_start, t_stop)

    return T, t


def smooth(y, window_length=51, polyorder=3):
    """
    Smooth a signal using a time filter.

    Parameters
    ----------
    y: array
        signal to smooth
    window_length: float
        Time Window Length in points. Default is 51
    polyorder: integer
        Polinom order. Default is 3 
    """
    return savgol_filter(np.squeeze(y), window_length, polyorder)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    pulse_nb = 53744
    signame = 'GETC_ISP_6A'

    T, t = temperature_from_pulse(pulse_nb, signame)

    fig,ax = plt.subplots()
    #ax.axvspan(0, t_fin_acq, alpha=0.2, color='red')
    #ax.plot(t, T, '.')
    ax.plot(t, T, '.')
    #ax.set_xlim(- 5*60, t_fin_acq + 5*60)
    fig.show()

