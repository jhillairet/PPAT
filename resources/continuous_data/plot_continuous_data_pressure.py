# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 18:08:42 2020

@author: JH218595
"""

#%% Import libraries
from numpy import *
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pywed as pw
import time
from datetime import datetime, timedelta

TIME_BETWEEN_POINTS = 5  # s


def pressure_from_date(day, start_time, stop_time):
    '''
    Return the pressure data from continuous acquisition

    Parameters
    ----------
    day : str
        Day of the start time in 'dd-mm-yyyy'
    start_time : str
        start time in 'HH:MM:SS'
    stop_time : str
        stop time in 'HH:MM:SS'

    Returns
    -------
    torus_pressure : array
        torus pressure in [Pa]

    '''
    # p = pw.tsmat(0, 'EXP=T=S;General;TTORE')  # not updated in real time...
    # torus_pressure = p[0]*10**(p[1])
    [xM, t] = pw.tsbase('SDVMTPJ11', day, start_time, stop_time)  # Pressure Mantisse Torus
    [xE, t] = pw.tsbase('SDVETPJ11', day, start_time, stop_time)  # Pressure Exposant Torus
     # xE est l’exposant, xM est la mantisse. La pression est xM*10^xE
    torus_pressure = xM * 10**xE

    return torus_pressure, t

def day_and_times(nb_seconds=60) -> list:
    '''
    Return the current day, current time and time few seconds before

    Parameters
    ----------
    nb_seconds : int
        number of seconds desired

    Returns
    -------
    day_and_times : list of strings
        [today, start_time, stop_time]

    '''
    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    time_stop = now.strftime("%H:%M:%S")
    time_start = (now - timedelta(seconds=nb_seconds)).strftime("%H:%M:%S")

    return today, time_start, time_stop

### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Vacuum Pressure") # creates a window
p = win.addPlot(title="Pressure")  # creates empty space for the plot in the window
curve = p.plot()                        # create an empty "plot" (a curve to plot)
p.setLogMode(False, True)               # logY

windowWidth = 500                       # width of the window displaying the curve
ptr = -windowWidth                      # set first x position

# initialize the data with the past 200 points
# pressure data are released every seconds. Take a point every TIME_BETWEEN_POINTS
previous_pressure, previous_t = pressure_from_date(*day_and_times(nb_seconds=500*5))
Xm = previous_pressure.squeeze()[::5]

#%%
# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global curve, ptr, Xm

    # get the current pressure data value
    today, time_start, time_stop = day_and_times(nb_seconds=TIME_BETWEEN_POINTS)
    try:
        torus_pressure, t = pressure_from_date(today, time_start, time_stop)

        # shift data in the temporal mean 1 sample left
        Xm[:-1] = Xm[1:]

        # update the vector containing the instantaneous values
        Xm[-1] = torus_pressure[-1]

        # update the plot
        curve.setData(Xm)                     # set the curve with this data
        curve.setPos(ptr,0)                   # set x position in the graph to 0

        ptr += TIME_BETWEEN_POINTS            # update x position for displaying the curve
        QtGui.QApplication.processEvents()    # MUST process the plot now
    except ValueError as e:
        print('skiping a point')

# update the graph every TIME_BETWEEN_POINTS seconds
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(TIME_BETWEEN_POINTS * 1000)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
