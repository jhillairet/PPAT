#-*-coding: utf-8 -*-
#from PyQt4 import QtCore, QtGui
from .Qt import QtWidgets, QtCore, QtGui
       
import os
import numpy as np
import os.path

from segmentTrajectoryFinder import segmentTrajectoryFinder

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#def debug_trace():
#    '''Set a tracepoint in the Python debugger that works with Qt'''
#    from PyQt5.QtCore import pyqtRemoveInputHook
#
#    from pdb import set_trace
#    pyqtRemoveInputHook()
#    set_trace()
    

#class MyHandler(FileSystemEventHandler, QtCore.QThread):
#    """
#     Handler class for Watchdog.
#     Inherits from FileSystemEventHandler as a file system monitoring class and from QThread
#     apparently for multithreaded operation within the PyQt.
#
#     IMPORTANT NOTE: for some unknown reason, this watchdog only works if the process
#     which changes the folder or its content runs on the same machine as the watchdog
#     itself. This has issues if Sup.xml and DP.xml files are erased/modified from a
#     process run on deneb, which could be the case after a pulse.
#     Potential solution: run a script hosted on the machine where PPAT is launched
#     through an ssh connection from anywhere.
#    """
#    def __init__(self, foldername):
#        """
#        Overloaded init to be able to pass the watched foldername as argument
#        """
#        super(MyHandler, self).__init__()
#        self.foldername = foldername
#
#    def on_any_event(self,event):
#        """
#        Method called when any kind of event happens to the monitored folder or its contents.
#        The signal is received
#        """
#        self.emit(QtCore.Signal("FolderModified"))
#
#
#class ModifFolderWatcher(QtCore.QThread):
#    """
#    Watcher class to monitor file changes on DP.xml or Sup.xml
#    Methods:
#    - modified: actions to perform when a folder/file change is detected
#    - resetFolderWatcher: actions to perform when the user changes the folder to be monitored
#    """
#    def __init__(self,parentWidget,folderName):
#        """
#        Overloaded init to be able to pass the parent widget (for addressing purposes)
#        and the folder to be monitored.
#        """
#        super(ModifFolderWatcher, self).__init__()
#        self.folderName = folderName
#        self.parent = parentWidget
#        # Start the observer process (standard way to do it for the watchdog package)
#        self.observer = Observer()
#        self.event_handler = MyHandler(self.folderName)
#        self.observer.schedule(self.event_handler, self.folderName, recursive=True)
#        self.observer.start()
#        # Method called when a change is detected
#        self.connect(self.event_handler, QtCore.Signal("FolderModified"), self.modified) #PyQt4
#
#
#    def modified(self):
#        """
#        Performs actions when a file change is detected.
#        - Stops the watcher to avoid signal saturation.
#        - Resets the results of checks in the checkArea (returns colored squares to black)
#        - Resets the scenario display area
#        - Update the next shot number
#        - Unload the DCS files to prevent any subsequent check or BigPicture by the user
#        - Remove the changetime from the onlineSituation Area (because the DCS file has to be reloaded
#        """
#        #self.emit(QtCore.SIGNAL("fileModified1"))
#        self.observer.stop()
#        self.parent.CheckAreaWidget.resetScenario()
#        self.parent.scenarioAreaWidget.resetScenarioDisplay()
#        self.parent.OnlineSituationAreaWidget.updateNextShot()
#        self.parent.scenarioAreaWidget.unloadDCS()
#        self.parent.OnlineSituationAreaWidget.removeModTime()
#
#    def resetModifFolderWatcher(self,folderName):
#        """
#        Stops the pre-existing watcher and starts a new one with a new folder to be monitored
#        Similar procedure as in the init.
#        """
#        self.observer.stop()
#        self.folderName = folderName
#        self.observer = Observer()
#        self.event_handler = MyHandler(self.folderName)
#        self.observer.schedule(self.event_handler, self.folderName, recursive=True)
#        self.observer.start()
#        self.connect(self.event_handler, QtCore.Signal("FolderModified"), self.modified)

class scenarioArea():
    """
    Class defining the scenario Area widget on top of the GUI.
    Notable attributes:
    - parentwidget: for addressing purposes (call methods of other widget-like classes)
    - buttons to load DCS files from the default folder or from a custom folder
    - scenario display area: display the chain of segment selected by the user
    - supFilename: path to the Sup.xml DCS file. Used by several other methods in the GUI
    - dpFilename: path to the DP.xml DCS file. Used by several other methods in the GUI
    - segmentTrajectory : string containing the sequence of segments (=scenario)
    Methods:
    - LoadDCSdefault: loads DCS files from the default folder. Called by the relevant button
    - LoadDCSfrom: loads DCS files from a custom folder. Called by the relevant button
    - UnLoadDCS: resets the DCS file/folder names. Called by watchdog events or if any load
    operation has failed.
    - updateScenarioDisplay: displays the default scenario after a successful DCS file load
    - resetScenarioDisplay: removes the segments from the display area. Called by watchdog events or
    if a load operation has failed.
    """


    def __init__(self,parentWidget):
        # Initiate the segmentTrajectory string (=scenario) to nothing.
        # Initiate file paths
        self.segmentTrajectory = ''
        self.supFilename = ''
        self.dpFilename = ''

        #Boolean to check that a scenario has been properly loaded.
        self.isScenarioLoaded = False

        #Parent widget should be the centralWidget, parent of all other GUI widgets.
        self.parent = parentWidget

        # Nominal scenario label
        self.label_nomsc = QtWidgets.QLabel(parentWidget)
        self.label_nomsc.setGeometry(QtCore.QRect(40, 10, 191, 31))
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.label_nomsc.setFont(font)
        self.label_nomsc.setObjectName("Label_Nominal_scenario")
        self.label_nomsc.setText("Nominal scenario")

        # Push button to load DCS default files.
        self.pushButton_LoadDCSdefault = QtWidgets.QPushButton(parentWidget)
        self.pushButton_LoadDCSdefault.setGeometry(QtCore.QRect(10, 40, 110, 35))
        font = QtGui.QFont()
        font.setPixelSize(10)
        self.pushButton_LoadDCSdefault.setFont(font)
        self.pushButton_LoadDCSdefault.setStyleSheet("Text-align:center")
        self.pushButton_LoadDCSdefault.setObjectName("pushButton_LoadDCSdefault")
        self.pushButton_LoadDCSdefault.setText("Load XML DCS \n default")

        # Push button to load custom DCS files.
        self.pushButton_LoadDCSfrom = QtWidgets.QPushButton(parentWidget)
        self.pushButton_LoadDCSfrom.setGeometry(QtCore.QRect(130, 40, 110, 35))
        font = QtGui.QFont()
        font.setPixelSize(10)
        self.pushButton_LoadDCSfrom.setFont(font)
        self.pushButton_LoadDCSfrom.setStyleSheet("Text-align:center")
        self.pushButton_LoadDCSfrom.setObjectName("pushButton_LoadDCSfrom")
        self.pushButton_LoadDCSfrom.setText("Load XML DCS\n from...")

        # Array of drop down menu objects for segment choices in the scenario display
        self.ComboBox_segmentList = np.array([],dtype='object')
        # Array of "==>" string to be displayed in between segments in the scenario display area.
        self.Label_arrowsList = np.array([],dtype='object')

        # QWidget containing the horizontal layout widget for scenario display.
        # Could be done in a simpler way ? Always confused by Horizontal Layouts.
        self.HLayout_Scenario_Widget = QtWidgets.QWidget(parentWidget)
        self.HLayout_Scenario_Widget.setGeometry(QtCore.QRect(280, 30, 800, 40))

        # Horizontal Layout in which the sequence of segments is displayed.
        self.horizontalLayout_Scenario = QtWidgets.QHBoxLayout(self.HLayout_Scenario_Widget)
        self.horizontalLayout_Scenario.setObjectName("horizontalLayout_Scenario")
        #self.horizontalLayout_Scenario.setGeometry(QRect(280, 400, 300, 200))

        # Push button connexions to relevant methods.
        self.pushButton_LoadDCSdefault.clicked.connect(self.LoadDCSdefault)
        self.pushButton_LoadDCSfrom.clicked.connect(self.LoadDCSfrom)

        # Useless ?
        #self.label_arrow_segments = QLabel(parentWidget)



    def LoadDCSdefault(self):
        """
        Method to load the DCS files from a default folder.
        Updates the DP and Sup filenames attributes
        Inits the folder watchdog.
        Calls update functions:
        - Resets the check Area
        - Updates the next pulse number
        - Updates the timechange
        """
        # Asks to update for online/offline status and requests it from statusAreaWidget where it is stored.
        self.parent.statusAreaWidget.update_status(1)
        online_status = self.parent.statusAreaWidget.login_status
        # Retrieves the assumed role (EiC or SL) from statusAreaWidget attributes.
        role = self.parent.statusAreaWidget.role

        # In online mode, sets default DCS files folders as a function of the role.
        # Note: Folders are currently the same for EiC and SL. This might change in the future.
        # Note 2: PPAT is usually run on nunki. therefore, it cannot access deneb filesystem.
        if (online_status==1) and (role=='Session Leader'):
            self.LoadFolderName = '/var/tmp/pilotes/XEDIT2DCS'
        elif (online_status==1) and (role=='Engineer in Charge'):
            self.LoadFolderName = '/var/tmp/pilotes/XEDIT2DCS'

        #In Offline mode, sets the default folder as the following. Should be the default output folder for XEDIT2DCS.
        else:
            self.LoadFolderName = '/Home/%s/XEDIT2DCS/data/output'%(self.parent.statusAreaWidget.login_name)

        # DP.xml and Sup.xml are supposed to be in th same folder.
        self.supFilename = '%s/Sup.xml'%(self.LoadFolderName)
        self.dpFilename = '%s/DP.xml'%(self.LoadFolderName)
    
        # Case if both files have been loaded successfully.
        if (os.path.isfile(self.dpFilename) and os.path.isfile(self.supFilename)):
            # the sequence of segments (=segment trajectory) is retrieved from the Sup.xml file.
            # At the moment, only the nominal scenario i.e. the scenario containing the most segments
            # with numbers < 100 is retrieved.
            self.segmentTrajectory = segmentTrajectoryFinder(self.supFilename)

            # Update the scenario display with the nominal scenario
            self.updateScenarioDisplay()

#            # Check if a watchdog already exists in order not to create a new one for each folder change               
#            if not hasattr(self, 'FolderWatcher'):
#                # No pre existing watchdog
#                self.FolderWatcher = ModifFolderWatcher(self.parent,self.LoadFolderName)
#                
#            else:
#                # preexisting watchdog: stop and recreate a new one.
#                self.FolderWatcher.resetModifFolderWatcher(self.LoadFolderName)

            # Resets text area and colored squares
            self.parent.CheckAreaWidget.resetChecks()

            # Update the next shot number
            self.parent.OnlineSituationAreaWidget.updateNextShot()

            # Update the last modification time
            self.parent.OnlineSituationAreaWidget.updateModTime()

        # Case if the user cancels the load operation or if the file has not been found
        else:
            # Displays a text message saying the load operation has not been completed.
            self.parent.CheckAreaWidget.WrongDCSFile()
            # Updates the next shot number
            self.parent.OnlineSituationAreaWidget.updateNextShot()
            # Erases the scenario display
            self.parent.scenarioAreaWidget.resetScenarioDisplay()
            # Unloads the DCS file
            self.unloadDCS()
            # Removes the changetime for current file.
            self.parent.OnlineSituationAreaWidget.removeModTime()


    def LoadDCSfrom(self):
        """
        Method to load the DCS file from a custum chosen folder.
        Almost identical to LoadDCSdefault, except the file menu.
        """

        self.LoadFolderName = QtWidgets.QFileDialog.getExistingDirectory(self.parent,"Load XML/DCS file",'.')
        self.supFilename = '%s/Sup.xml'%(self.LoadFolderName)
        self.dpFilename = '%s/DP.xml'%(self.LoadFolderName)
        if (os.path.isfile(self.dpFilename) and os.path.isfile(self.supFilename)):
            self.segmentTrajectory = segmentTrajectoryFinder(self.supFilename)
            self.updateScenarioDisplay()

            try:
                FolderWatcher = self.FolderWatcher
            except AttributeError:
                self.FolderWatcher = ModifFolderWatcher(self.parent,self.LoadFolderName)
            else:
                self.FolderWatcher.resetModifFolderWatcher(self.LoadFolderName)

            self.parent.statusAreaWidget.update_status(0)
            self.parent.CheckAreaWidget.resetChecks()
            self.parent.OnlineSituationAreaWidget.updateNextShot()
            self.parent.OnlineSituationAreaWidget.updateModTime()
        else:
            self.parent.OnlineSituationAreaWidget.updateNextShot()
            self.parent.scenarioAreaWidget.resetScenarioDisplay()
            self.parent.CheckAreaWidget.WrongDCSFile()
            self.unloadDCS()
            self.parent.OnlineSituationAreaWidget.removeModTime()

    def unloadDCS(self):
        """
        Method to reset the DCS file names.
        Called by watchdog events or failed DCS load attempts.
        """
        self.LoadFolderName = ''
        self.supFilename = ''
        self.dpFilename = ''

    def updateScenarioDisplay(self):
        """
        Method to display the selected scenario
        """
        #Records that a scenario was properly loaded
        self.isScenarioLoaded = True

        # First reset the scenario display area.
        for kk in reversed(range(self.horizontalLayout_Scenario.count())):
            self.horizontalLayout_Scenario.itemAt(kk).widget().setParent(None)

        self.ComboBox_segmentList = np.array([],dtype='object')
        self.Label_arrowsList = np.array([],dtype='object')

        # Loop over the segment list in segmentTrajectory and add them in the scenario display area.
        for k in range(0, len(self.segmentTrajectory)):

            # Add the segment as a drop down menu in the scenario display area array
            self.ComboBox_segmentList = np.append(self.ComboBox_segmentList, QtWidgets.QComboBox())
            # Add the segment name in the dropdown list.
            # Note: at the moment, only one segment is proposed.
            # In the future, all possible segments might be proposed, with different transition conditions.
            self.ComboBox_segmentList[k].addItem(self.segmentTrajectory[k,0])
            # Creates the arrow lists (actually text labels) to chain the segments
            self.Label_arrowsList = np.append(self.Label_arrowsList, QtWidgets.QLabel())
            self.Label_arrowsList[k].setText("==>")
            # Add the dropdown menu and arrows in the horizontal layout
            self.horizontalLayout_Scenario.addWidget(self.ComboBox_segmentList[k], QtCore.Qt.AlignLeft)
            self.horizontalLayout_Scenario.addWidget(self.Label_arrowsList[k], QtCore.Qt.AlignLeft)

        # Final segment (add "End" after the last segment in the segment trajectory)
        self.Label_arrowsList = np.append(self.Label_arrowsList, QtWidgets.QLabel())
        self.Label_arrowsList[-1].setText("End")
        self.horizontalLayout_Scenario.addWidget(self.Label_arrowsList[-1], QtCore.Qt.AlignLeft)

    def resetScenarioDisplay(self):
        #Records that no scenario is currently loaded (any more)
        self.isScenarioLoaded = False
        for kk in reversed(range(self.horizontalLayout_Scenario.count())):
            self.horizontalLayout_Scenario.itemAt(kk).widget().setParent(None)
        self.ComboBox_segmentList = np.array([],dtype='object')
        self.ComboBox_segmentList = np.array([],dtype='object')
