#-*-coding: utf-8 -*-
#from PyQt4 import QtCore, QtGui
from .Qt import QtWidgets, QtCore, QtGui

import os,sys
import xml.etree.ElementTree as ET
import pylab as plt
import numpy as np
import time
import importlib
import re
from getpass import getuser
from subprocess import call


class statusArea():
    """
    Determines the user status: online/offline and EiC/SL.
    Notable attributes:
    - parent: parent widget name to call methods from instances of other classes.
    - label_LoginStatus: text display of the user status
    - role: "EiC" or "SL" (string)
    - login_status: 0 for offline. 1 for online (integer)
    Methods:
    - update_status: changes the user status as a function of external events. Called when DCS files are loaded.
    """
    def __init__(self,parentWidget):
        self.parent = parentWidget
        # Login status display text init
        self.label_LoginStatus = QtWidgets.QLabel(self.parent)
        self.label_LoginStatus.setGeometry(QtCore.QRect(20, 650, 700, 31))
        font = QtGui.QFont()
        font.setPixelSize(14)
        self.label_LoginStatus.setFont(font)
        self.label_LoginStatus.setObjectName("LoginStatus")
        # Get the user name to determine if the user is online or offline.
        # NOTE: the role is not taken from the config file, not the user name
        # An SL might want to open an EiC PPAT to check something on "the other side".
        self.login_name = getuser()

        # Determine the role (EiC or SL) from the Config File
        xml_doc = ET.parse(str(self.parent.config_file_name))
        xml_root = xml_doc.getroot()
        self.role = xml_root.find('ROLE').text

        # Define the login status as offline by default.
        self.login_status = 0

    def update_status(self,force_status):
        """
        Method to update the online status following events.
        force_status is used to override the automatic status determination from the login name
        The logic is that by default, if the login name is either EiC or SL then PPAT is online
        as long as the chosen DCS folder is the online (default) one.
        If the user chooses a different folder, PPAT goes in offline mode.
        """

        if (force_status==0):
            #Force offline status if all conditions are not fullfilled (example: a custom XML/DCS file is loaded)
            self.login_status = 0
            self.label_LoginStatus.setText("WARNING: You are now using PPAT as %s - OFFLINE mode"%(self.role))
            self.label_LoginStatus.setStyleSheet("color : \"red\" ")

        elif (force_status==1):
            # Default check to determine if online or offline mode.
            # If the shell login name is either eic or pilotes, set as online
            # The role (EiC or Session Leader) is taken from the configuration file rather from the Login name.
            # This allows either role to run PPAT as the other role should this be needed.
            # Besides, when running offline, there is no way to know which role is assumed except by looking into
            # the configuration file.

            if (self.login_name=='pilotes') or (self.login_name=='eic'):
                self.label_LoginStatus.setText("You are using PPAT as %s - online mode"%(self.role))
                self.login_status = 1
                self.label_LoginStatus.setStyleSheet("color : \"black\" ")
            else:
                self.label_LoginStatus.setText("You are using PPAT as %s - offline mode"%(self.role))
                self.login_status = 0
                self.label_LoginStatus.setStyleSheet("color : \"black\" ")
