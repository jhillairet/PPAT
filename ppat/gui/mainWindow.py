# /usr/bin/python
#-*-coding: utf-8 -*-

from .Qt import QtGui, QtWidgets, QtCore

from . import CheckArea, scenarioArea, statusArea, OnlineSituationArea
from .BigPicture import *


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self, title, config_file):
        super(mainWindow, self).__init__()  # top-level window creator

        self.setWindowTitle(title)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setObjectName("MainWindow")

        self.resize(1165, 723)
        font = QtGui.QFont()
        self.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/ppat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget.setObjectName("centralwidget")

        self.centralwidget.config_file_name = config_file



        self.centralwidget.statusAreaWidget = statusArea.statusArea(self.centralwidget)
        # Check if PPAt is started in online or offline mode.
        self.centralwidget.statusAreaWidget.update_status(1)

        # Initialization:
        # Instance of a class defining the top part of the GUI where the scenario (i.e. the sequence of
        # segments is defined. Contains methods to load DCS files and update the display accordingly.
        self.centralwidget.scenarioAreaWidget = scenarioArea.scenarioArea(self.centralwidget)

        # Initialization:
        # Class defining the lower right part of the GUI displaying pulse number and time of last DCS file.
        # Contains methods to update these numbers.
        self.centralwidget.OnlineSituationAreaWidget = OnlineSituationArea.OnlineSituationArea(self.centralwidget)


        # Geometry of upper right part of GUI (external tools)
        # Probably to be defined in a separate class in the future.
        # VerticalLayout to stack buttons.
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(850, 100, 240, 240))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Button to run the Big Picture
        # Improvement suggestion: gray it out if no scenario is loaded.
        self.pushButton_BigPicture = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(15)
        self.pushButton_BigPicture.setFont(font)
        self.pushButton_BigPicture.setObjectName("pushButton_BigPicture")
        self.pushButton_BigPicture.setText("Big Picture")
        self.verticalLayout.addWidget(self.pushButton_BigPicture)

        # Button to run ICRH resonance calculation tool
        # Deactivated for the moment.
        self.pushButton_ICRHres = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(15)
        self.pushButton_ICRHres.setFont(font)
        self.pushButton_ICRHres.setAutoRepeat(False)
        self.pushButton_ICRHres.setObjectName("pushButton_ICRHres")
        self.pushButton_ICRHres.setText("ICRH resonance calculator")
        self.verticalLayout.addWidget(self.pushButton_ICRHres)
        self.pushButton_ICRHres.setEnabled(False)

        # Button to run the magnetic connections tool (whatever that is) for the current scenario.
        # Deactivated for the moment.
        self.pushButton_Magnetic_connections = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(15)
        self.pushButton_Magnetic_connections.setFont(font)
        self.pushButton_Magnetic_connections.setObjectName("pushButton_Magnetic_connections")
        self.pushButton_Magnetic_connections.setText("Magnetic connections")
        self.verticalLayout.addWidget(self.pushButton_Magnetic_connections)
        self.pushButton_Magnetic_connections.setEnabled(False)

        # Button to run Plato
        # Deactivatedfor the moment.
        self.pushButton_Plato = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPixelSize(15)
        self.pushButton_Plato.setFont(font)
        self.pushButton_Plato.setObjectName("pushButton_Plato")
        self.pushButton_Plato.setText("Run Plato")
        self.verticalLayout.addWidget(self.pushButton_Plato)
        self.pushButton_Plato.setEnabled(False)


        # Initialization:
        # Instance of the class defining the central part of the GUI (colored squares
        # and text area)


        self.centralwidget.CheckAreaWidget = CheckArea.CheckArea(self.centralwidget)



        # Cosmetic improvements

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 80, 1131, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(770, 100, 20, 521))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(800, 330, 311, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # Central Widget final display
        self.setCentralWidget(self.centralwidget)


        # Connexion of the Big Picture button to the associated function.
        self.pushButton_BigPicture.clicked.connect(lambda: BigPicture_disp(self.centralwidget.scenarioAreaWidget.segmentTrajectory,self.centralwidget.scenarioAreaWidget.dpFilename))
