#-*-coding: utf-8 -*-
#from PyQt4 import QtCore, QtGui
from .Qt import QtCore, QtWidgets, QtGui

import os,sys
import xml.etree.ElementTree as ET
import pylab as plt
import numpy as np
import time
import importlib
import re
import socket
import IRFMtb
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def is_db_reachable():
    """
    Checks if the IRFM WEST database server is reachable on the network.

    Returns
    -------
    bool

    """
    host = '10.8.86.1'  # deneb address
    port = 5880
    try:
        s = socket.create_connection((host, port), timeout=2)
        return True
    except socket.error:
        return False





class OnlineSituationArea():
    """
    Defines the lower right part of the GUI (next shot number, DCS file date, etc.)
    Notable attributes:
    - parent widget for addressing purposes
    - Next shot number (label)
    - DCS folder loaded and time of last modification (label)
    Methods:
    - updateNextShot: called by changes of DCS files or watchdog events in online mode
    - updateModTime: called by changes of DCS files
    - removemodTime: called by watchdog events.
    """
    def __init__(self,parentWidget):
        self.parent = parentWidget
        # Next shot text display init
        self.label_NextShot = QtWidgets.QLabel(self.parent)
        self.label_NextShot.setGeometry(QtCore.QRect(850, 300, 200, 200))
        font = QtGui.QFont()
        font.setPixelSize(25)
        self.label_NextShot.setFont(font)
        self.label_NextShot.setObjectName("LabelNextShot")
        self.label_NextShot.setAlignment(QtCore.Qt.AlignCenter)

        # Current DCS file text display init
        self.label_CurrentFile= QtWidgets.QLabel(self.parent)
        self.label_CurrentFile.setGeometry(QtCore.QRect(750, 400, 400, 300))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_CurrentFile.setFont(font)
        self.label_CurrentFile.setObjectName("LabelCurrentFile")
        self.label_CurrentFile.setAlignment(QtCore.Qt.AlignCenter)


    def updateNextShot(self):
        """
        Method to update the shot number if the Tore Supra/WESt database is available
        Only displays the next shot number in online mode (irrelevant in offline mode)
        Note: the next shot number is simply the last shot in the database + 1
        """

        if is_db_reachable():
            nextShotNumber = IRFMtb.tsdernier_choc()

        else :
            nextShotNumber = -1
        if (self.parent.statusAreaWidget.login_status==1):
            self.label_NextShot.setText('Next Shot is \n%d'%(nextShotNumber+1))
        else:
            self.label_NextShot.setText('Next Shot is \n [Offline]')

    def updateModTime(self):
        """
        Method to display the last time the DCS files or their folder have been updated.
        Takes the latest changetime among the DP.xml, Sup.xml and containing folder.
        """
        mod_time_folder  = os.path.getmtime(self.parent.scenarioAreaWidget.LoadFolderName)
        mod_time_Supxml = os.path.getmtime(self.parent.scenarioAreaWidget.supFilename)
        mod_time_DPxml = os.path.getmtime(self.parent.scenarioAreaWidget.dpFilename)
        mod_time = time.ctime(max(mod_time_folder,mod_time_Supxml,mod_time_DPxml))
        self.label_CurrentFile.setText('Current DCS Files folder:\n %s \n - \n Last modified: %s'\
        %(self.parent.scenarioAreaWidget.LoadFolderName, mod_time))

    def removeModTime(self):
        """
        Removes the changetime in situations where it is not relevant anymore (DCS file change
        or watchdog event)
        """
        self.label_CurrentFile.setText('')
