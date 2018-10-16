import os.path
import socket
from contextlib import contextmanager

from getpass import getuser
from qtpy.QtWidgets import (QMainWindow, QApplication, QWidget,
                            QHBoxLayout, QVBoxLayout, QAction, qApp,
                            QScrollArea, QTextBrowser, QFrame, QTextEdit,
                            QFileDialog, QPlainTextEdit, QTableWidgetItem)
from qtpy.QtGui import QIcon, QCursor
from qtpy.QtCore import QDir, Slot, Qt

from pppat.ui.reminder import EiCReminderWidget
from pppat.ui.console import ConsoleWidget
from pppat.ui.collapsible_toolbox import QCollapsibleToolbox
from pppat.ui.pre_pulse_analysis import PrePulseAnalysisWidget
from pppat.ui.pre_pulse_display import PrePulseDisplayWidget
from pppat.ui.log import QPlainTextEditLogger
from pppat.libpulse.pulse_settings import PulseSettings
from pppat.ui.BigPicture import BigPicture_disp

import logging
logger = logging.getLogger(__name__)

# PPPAT minimum width in pixels
MINIMUM_WIDTH = 800


class MainWindow(QMainWindow):
    """
    Central GUI class which also serves as main Controller
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # initialize the window
        # Window properties
        self.setWindowTitle('Pre & Post Pulse Analysis Tool for WEST')

        # setup window size to 90% of avail. screen height
        rec = QApplication.desktop().availableGeometry()
        self.resize(MINIMUM_WIDTH, .9*rec.height())

        # Menu Bar
        self.menu_bar()

        # Set the various PPPAT tools as the central Widget
        self.generate_central_widget()
        self.setCentralWidget(self.central_widget)

        # connect the various button to their controller
        self.panel_pre_pulse.widget.push_load.clicked.connect(self.load_pulse_settings)
        self.panel_pre_pulse.widget.push_browse.clicked.connect(self.browse_pulse_settings_directory)
        self.panel_pre_pulse.widget.push_check.clicked.connect(self.check_pulse_settings)
        self.panel_pulse_display.widget.push_bigpicture.clicked.connect(self.display_big_picture)

        # Application icon
        self.setWindowIcon(QIcon('resources/icons/pppat.png'))

        # open some panels at startup
        # self.panel_rappels.toggleButton.click()
        self.panel_pre_pulse.toggleButton.click()
        self.panel_pulse_display.toggleButton.click()
        self.panel_log.toggleButton.click()

        # define set of internal parameters
        self.pulse_settings = None
        self.pulse_settings_dir = None
        self.pulse_settings_files = None
        self.pulse_settings_shot = None

        # Display user role in the status Bar
        logger.info(f'PPPAT has been launched by user {self.user_login}')
        self.statusBar().showMessage(f'PPPAT launched by {self.user_role}')

#        # Depending of the user's role, enable/disable loading pulse setup from SL
#        if self.user_role == 'eic':
#            self.panel_pre_pulse.widget.radio_sl.setChecked(True)
#        else:
#            self.panel_pre_pulse.widget.radio_sl.setDisabled(True)
#            self.panel_pre_pulse.widget.radio_shot.setChecked(True)

        logger.info('Starting PPPAT')

    def menu_bar(self):
        """ Menu bar """
        self.menuBar = self.menuBar()

        file_menu = self.menuBar.addMenu('&File')
        action_file_exit = QAction('&Exit', self)
        action_file_exit.setStatusTip('Exit')
        action_file_exit.setShortcut('Ctrl+Q')
        action_file_exit.triggered.connect(qApp.quit)
        file_menu.addAction(action_file_exit)

    def generate_central_widget(self):
        """
        Define the central widget, which contain the main GUI of the app,
        mostly the various tools.
        """
        # Define the various collabsible panels (leave "child=" avoid Qt bug)
        self.panel_rappels = QCollapsibleToolbox(child=EiCReminderWidget(), title='Cahier de liaison des EiC / EiC\'s Notebook')
        self.panel_pre_pulse = QCollapsibleToolbox(child=PrePulseAnalysisWidget(), title='Pre-pulse Analysis')
        self.panel_pulse_display = QCollapsibleToolbox(child=PrePulseDisplayWidget(), title='Pre-pulse Display')
        self.panel_post_pulse = QCollapsibleToolbox(child=QTextBrowser(), title='Post-pulse Analysis')
        self.panel_log = QCollapsibleToolbox(child=QPlainTextEditLogger(), title='Logs')
        self.panel_console = QCollapsibleToolbox(child=ConsoleWidget(), title='Python Console')

        # stacking the collapsible panels vertically
        vbox = QVBoxLayout()
        vbox.addWidget(self.panel_rappels)
        vbox.addWidget(self.panel_pre_pulse)
        vbox.addWidget(self.panel_pulse_display)
        vbox.addWidget(self.panel_post_pulse)
        vbox.addWidget(self.panel_log)
        vbox.addWidget(self.panel_console)

        # making the whole panels scrollable
        # The scrollbar should be set for a widget, here a dummy one
        collaps = QWidget()
        collaps.setLayout(vbox)
        scroll = QScrollArea(self)
        scroll.setWidget(collaps)
        scroll.setWidgetResizable(True)
        self.central_widget = scroll

    @property
    def user_login(self):
        """
        User's login name
        """
        return getuser()

    @property
    def user_role(self):
        """
        User's "role", Could be:
            - Engineer in Charge ("eic")
            - Session Leader ("sl")
            - someone else (None)
        Depending of this "role", some options in PPPAT might differ.
        """
        if self.user_login == 'eic' or 'JH218595':
            return 'eic'
        elif self.user_login == 'sl':
            return 'sl'
        else:
            return None

    @Slot()
    def check_pulse_settings(self):
        """ Check pulse setting vs all tests """
        
        with self.wait_cursor():
            check_results = self.pulse_settings.check_all(self.is_online())

        # display the check results into the table
        for i, result in enumerate(check_results):
            self.panel_pre_pulse.widget.check_table.setItem(i, 0, QTableWidgetItem(result.name))
            self.panel_pre_pulse.widget.check_table.setItem(i, 1, QTableWidgetItem(result.code_name))
            self.panel_pre_pulse.widget.check_table.setItem(i, 2, QTableWidgetItem(result.text))
            # # Stretch 
            # self.panel_pre_pulse.widget.check_table.horizontalHeader().setStretchLastSection(True)
            
            # Add color to the result item (OK, WARNING, ERROR or UNAVAILABLE)
            if result.code == result.ERROR:
                self.panel_pre_pulse.widget.check_table.item(i, 1).setForeground(Qt.red)
            elif result.code == result.WARNING:
                self.panel_pre_pulse.widget.check_table.item(i, 1).setForeground(Qt.darkYellow)
            elif result.code == result.OK:
                self.panel_pre_pulse.widget.check_table.item(i, 1).setForeground(Qt.darkGreen)
            elif result.code == result.UNAVAILABLE:
                self.panel_pre_pulse.widget.check_table.item(i, 1).setForeground(Qt.darkMagenta)
            # else leave it black (default)

##            # Check if a watchdog already exists in order not to create a new one for each folder change               
##            if not hasattr(self, 'FolderWatcher'):
##                # No pre existing watchdog
##                self.FolderWatcher = ModifFolderWatcher(self.parent,self.LoadFolderName)
##                
##            else:
##                # preexisting watchdog: stop and recreate a new one.
##                self.FolderWatcher.resetModifFolderWatcher(self.LoadFolderName)
#
#            # Resets text area and colored squares
#            self.parent.CheckAreaWidget.resetChecks()
#
#            # Update the next shot number
#            self.parent.OnlineSituationAreaWidget.updateNextShot()
#
#            # Update the last modification time
#            self.parent.OnlineSituationAreaWidget.updateModTime()
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



    @Slot()
    def load_pulse_settings(self):
        """ Load the pulse settings when user clicks on 'load' """
        # construct the pulse settings
        self.pulse_settings = PulseSettings()
        # default loading state
        res_load = False

        with self.wait_cursor():
            # Load the pulse setting depending on the loading option
            # Load pulse settings from the Session Leader proposal
            if self.panel_pre_pulse.widget.radio_sl.isChecked():
                # TODO : check if SL pulse setting is available
                pulse_settings_SL_avail = True
    
                if not pulse_settings_SL_avail:
                    logger.error('Pulse settings from SL are not available!')
                else:
                    logger.info('Loading pulse setting from SL')
                    self.panel_pre_pulse.widget.pulse_setting_origin.setText('from SL')
    
                    res_load = self.pulse_settings.load_from_session_leader()
    
            # Load pulse settings from a set of .xml files
            elif self.panel_pre_pulse.widget.radio_file.isChecked():
                if not self.pulse_settings_dir:
                    logger.error('Browse a directory first !')
                else:
                    self.panel_pre_pulse.widget.pulse_setting_origin.setText(
                            self.pulse_settings_dir)
                    logger.info('loading pulse setting from files')
    
                    res_load = self.pulse_settings.load_from_file(self.pulse_settings_files)
    
            # Load pulse settings from a pulse number
            elif self.panel_pre_pulse.widget.radio_shot.isChecked():
                pulse_nb = self.panel_pre_pulse.widget.edit_shot.text()
                if not pulse_nb:
                    logger.error('Set pulse number first !')
                else:
                    logger.info(f'loading pulse setting from WEST shot #{pulse_nb}')
    
                    self.panel_pre_pulse.widget.pulse_setting_origin.setText(
                            f'WEST shot number {pulse_nb}')
                    self.pulse_settings_shot = int(pulse_nb)
    
                    res_load = self.pulse_settings.load_from_pulse(self.pulse_settings_shot)

        # if the pulse settings have been correctly loaded
        # some widgets (buttons) are enabled
        # and the nominal scenario trajectory is displayed
        if res_load:
            logger.info('Pulse settings successfully loaded :)')
            self.panel_pre_pulse.widget.push_check.setEnabled(True)
            self.panel_pulse_display.widget.push_bigpicture.setEnabled(True)

            try:
                nominal_trajectory = self.pulse_settings.DCS_settings.nominal_trajectory
                # create a string which summarize the trajectory
                nominal_trajectory_str = ' -> '.join(nominal_trajectory)
                nominal_trajectory_str = nominal_trajectory_str.replace('segment', '')
                logger.info(nominal_trajectory_str)

                self.panel_pre_pulse.widget.pulse_properties.setText(nominal_trajectory_str)
            except AttributeError as e:
                logger.error(e)
        else:
            logger.error('Problem during pulse settings loading :(')

    @Slot()
    def browse_pulse_settings_directory(self):
        """
        Open a file dialog to select the directory which contains the sup.xml
        and dp.xml files.

        # TODO : also deals with zip or tar.gz file containing the .xml files
        """
        # if user click on the 'browse' button, then automatically select
        # the "file" mode
        self.panel_pre_pulse.widget.radio_file.setChecked(True)
        # open file dialog
        _pulse_settings_dir = \
            QFileDialog.getExistingDirectory(self,
                                             'Select XML/DCS files directory',
                                             directory=QDir.currentPath()
                                             )
        _pulse_settings_files = {
                'sup': f'{_pulse_settings_dir}/Sup.xml',
                'dp': f'{_pulse_settings_dir}/DP.xml'
                }

        # test if both file dp.xml and sup.xml exist. If not -> error msg
        if os.path.isfile(_pulse_settings_files['dp']) and \
            os.path.isfile(_pulse_settings_files['sup']):

            self.pulse_settings_dir = _pulse_settings_dir
            self.pulse_settings_files  = _pulse_settings_files
            logger.info(f'Pulse setting dir set to {self.pulse_settings_dir}')
            logger.info(f'Pulse setting files exist into {self.pulse_settings_dir}')
        else:
            logger.error("One or both of the pulse setting files do not exist!" )

    @Slot()
    def display_big_picture(self):
        """
        Display the big picture of the pulse setting.
        """
        # TODO : check data first?
        nominal_scenario = self.pulse_settings.DCS_settings.nominal_scenario
        dp_file = self.pulse_settings.files['dp']
        wfs = self.pulse_settings.waveforms

        BigPicture_disp(nominal_scenario, dp_file, wfs, 
                        self.pulse_settings_shot)

    @staticmethod
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

    @staticmethod
    @contextmanager
    def wait_cursor():
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            yield
        finally:
            QApplication.restoreOverrideCursor()

#     def __init__(self, title, config_file):
#        super(mainWindow, self).__init__()  # top-level window creator
#
#        self.setWindowTitle(title)
#
#        self.centralwidget = QtWidgets.QWidget(self)
#        self.setObjectName("MainWindow")
#
#        self.resize(1165, 723)
#        font = QtGui.QFont()
#        self.setFont(font)
#        icon = QtGui.QIcon()
#        icon.addPixmap(QtGui.QPixmap("gui/ppat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#        self.setWindowIcon(icon)
#
#        self.setTabShape(QtWidgets.QTabWidget.Rounded)
#        self.centralwidget.setObjectName("centralwidget")
#
#        self.centralwidget.config_file_name = config_file
#
#
#
#        self.centralwidget.statusAreaWidget = statusArea.statusArea(self.centralwidget)
#        # Check if PPAt is started in online or offline mode.
#        self.centralwidget.statusAreaWidget.update_status(1)
#
#        # Initialization:
#        # Instance of a class defining the top part of the GUI where the scenario (i.e. the sequence of
#        # segments is defined. Contains methods to load DCS files and update the display accordingly.
#        self.centralwidget.scenarioAreaWidget = scenarioArea.scenarioArea(self.centralwidget)
#
#        # Initialization:
#        # Class defining the lower right part of the GUI displaying pulse number and time of last DCS file.
#        # Contains methods to update these numbers.
#        self.centralwidget.OnlineSituationAreaWidget = OnlineSituationArea.OnlineSituationArea(self.centralwidget)
#
#
#        # Geometry of upper right part of GUI (external tools)
#        # Probably to be defined in a separate class in the future.
#        # VerticalLayout to stack buttons.
#        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
#        self.verticalLayoutWidget.setGeometry(QtCore.QRect(850, 100, 240, 240))
#        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
#        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
#        self.verticalLayout.setObjectName("verticalLayout")
#
#        # Button to run the Big Picture
#        # Improvement suggestion: gray it out if no scenario is loaded.
#        self.pushButton_BigPicture = QtWidgets.QPushButton(self.verticalLayoutWidget)
#        font = QtGui.QFont()
#        font.setPixelSize(15)
#        self.pushButton_BigPicture.setFont(font)
#        self.pushButton_BigPicture.setObjectName("pushButton_BigPicture")
#        self.pushButton_BigPicture.setText("Big Picture")
#        self.verticalLayout.addWidget(self.pushButton_BigPicture)
#
#        # Button to run ICRH resonance calculation tool
#        # Deactivated for the moment.
#        self.pushButton_ICRHres = QtWidgets.QPushButton(self.verticalLayoutWidget)
#        font = QtGui.QFont()
#        font.setPixelSize(15)
#        self.pushButton_ICRHres.setFont(font)
#        self.pushButton_ICRHres.setAutoRepeat(False)
#        self.pushButton_ICRHres.setObjectName("pushButton_ICRHres")
#        self.pushButton_ICRHres.setText("ICRH resonance calculator")
#        self.verticalLayout.addWidget(self.pushButton_ICRHres)
#        self.pushButton_ICRHres.setEnabled(False)
#
#        # Button to run the magnetic connections tool (whatever that is) for the current scenario.
#        # Deactivated for the moment.
#        self.pushButton_Magnetic_connections = QtWidgets.QPushButton(self.verticalLayoutWidget)
#        font = QtGui.QFont()
#        font.setPixelSize(15)
#        self.pushButton_Magnetic_connections.setFont(font)
#        self.pushButton_Magnetic_connections.setObjectName("pushButton_Magnetic_connections")
#        self.pushButton_Magnetic_connections.setText("Magnetic connections")
#        self.verticalLayout.addWidget(self.pushButton_Magnetic_connections)
#        self.pushButton_Magnetic_connections.setEnabled(False)
#
#        # Button to run Plato
#        # Deactivatedfor the moment.
#        self.pushButton_Plato = QtWidgets.QPushButton(self.verticalLayoutWidget)
#        font = QtGui.QFont()
#        font.setPixelSize(15)
#        self.pushButton_Plato.setFont(font)
#        self.pushButton_Plato.setObjectName("pushButton_Plato")
#        self.pushButton_Plato.setText("Run Plato")
#        self.verticalLayout.addWidget(self.pushButton_Plato)
#        self.pushButton_Plato.setEnabled(False)
#
#
#        # Initialization:
#        # Instance of the class defining the central part of the GUI (colored squares
#        # and text area)
#
#
#        self.centralwidget.CheckAreaWidget = CheckArea.CheckArea(self.centralwidget)
#
#
#
#        # Cosmetic improvements
#
#        self.line = QtWidgets.QFrame(self.centralwidget)
#        self.line.setGeometry(QtCore.QRect(10, 80, 1131, 16))
#        self.line.setFrameShape(QtWidgets.QFrame.HLine)
#        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
#        self.line.setObjectName("line")
#        self.line_2 = QtWidgets.QFrame(self.centralwidget)
#        self.line_2.setGeometry(QtCore.QRect(770, 100, 20, 521))
#        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
#        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
#        self.line_2.setObjectName("line_2")
#        self.line_3 = QtWidgets.QFrame(self.centralwidget)
#        self.line_3.setGeometry(QtCore.QRect(800, 330, 311, 20))
#        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
#        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
#        self.line_3.setObjectName("line_3")
#
#        # Central Widget final display
#        self.setCentralWidget(self.centralwidget)
#
#
#        # Connexion of the Big Picture button to the associated function.
#        self.pushButton_BigPicture.clicked.connect(lambda: BigPicture_disp(self.centralwidget.scenarioAreaWidget.segmentTrajectory,self.centralwidget.scenarioAreaWidget.dpFilename))
