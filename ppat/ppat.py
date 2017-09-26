#! /Applications/Python-3.3.5/bin/python3.3
# /usr/bin/python

#-*-coding: utf-8 -*-
from Qt.QtWidgets import QApplication

import matplotlib
matplotlib.use('Qt4Agg')

from mainWindow import mainWindow
import os,sys,getopt

def main(argv):
    showMainWindow = True

    # Workaround to allow launching the code from Spyder
    # if the QApp exists (case in Spyder), use it rather than making new one
    app = QApplication.instance()
    if app is None:
        app = QApplication(argv)

    # argv[0] is the path/name of the configuration file (EiC or SL) to be used.

    f=mainWindow("WEST Pre-Pulse Analysis Tools (PPAT)",argv[0])

    if showMainWindow:
        f.show()
    r = app.exec_()
    return r

if __name__=="__main__":
    if len(sys.argv) > 1: 
        main(sys.argv[1:])
    else:
        main(['PPATConfig_EiC.xml'])
