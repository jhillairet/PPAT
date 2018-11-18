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
   
    # date du choc
    date_apilote = pw.tsmat(pulse_nb, 'APILOTE;+VME_PIL;Date_Choc')
    pulse_dt = pd.to_datetime(date_apilote)
    # date conversion in 'dd/MM/yy'
    pulse_date = pulse_dt.strftime('%d/%m/%y')
    t_start = pulse_dt.strftime('%H:%M:%S')
    t_stop = (pulse_dt + pd.Timedelta(t_fin_acq, unit='s')).strftime('%H:%M:%S')
    
    return pulse_date, t_start, t_stop, pulse_dt

def temperature_from_time(signame, date=None, t_start='00:01:00', t_stop='23:59:00'):
    """
    return a temperature signal from DCALOR from continuous acquisition

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
         temperature array
     - t: np.array
         time vector in ms from the beginning of the day (tbc)

    """
    if not date:
        date = datetime.now().strftime('%d/%m/%y')

    T, t = pw.tsbase(signame, date, t_start, t_stop)

    return T, t


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
    # Récupération de la datation de DCALOR (en ms depuis minuit)
    # lorsqu'il recoit ORIGINE (commence l'acquisition)
    # Instant qui définit t=0s
    t_origine = int(pw.tsmat(pulse_nb, 'DCALOR;PARAM;ORIGINE'))

    # continous time acquisition data
    pulse_date, t_start, t_stop, _ = pulse_datetime(pulse_nb)
    T, t = pw.tsbase(signame, pulse_date, t_start, t_stop)

    # convert time into pulse time in second
    t = t - t_origine/1e3 - 32
    return T, t
