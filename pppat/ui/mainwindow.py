import os.path
from qtpy.QtWidgets import (QMainWindow, QApplication, QToolBox, QWidget,
                            QHBoxLayout, QVBoxLayout, QAction, qApp,
                            QScrollArea, QTextBrowser, QFrame, QTextEdit,
                            QFileDialog, QPlainTextEdit)
from qtpy.QtGui import QIcon
from qtpy.QtCore import QDir
# PPPAT's ui
from pppat.ui.reminder import EiCReminderWidget
from pppat.ui.console import ConsoleWidget
from pppat.ui.collapsible_toolbox import QCollapsibleToolbox
from pppat.ui.pre_pulse import PrePulseAnalysisWidget
from pppat.ui.log import QPlainTextEditLogger
# PPPAT's other stuffs
from pppat.pulse_setting import PulseSetting

import logging
logger = logging.getLogger(__name__)

MINIMUM_WIDTH = 800


class MainWindow(QMainWindow):  
    """
    Central class which serves as Controller
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
        self.panel_pre_pulse.widget.push_load.clicked.connect(self.load_pulse_setting)
        self.panel_pre_pulse.widget.push_browse.clicked.connect(self.browse_pulse_setting_directory)

        # Status Bar
        self.statusBar().showMessage('PPPAT')

        # Application icon
        self.setWindowIcon(QIcon('resources/icons/pppat.png'))

        # open some panels at startup
        # self.panel_rappels.toggleButton.click()
        self.panel_pre_pulse.toggleButton.click()
        self.panel_log.toggleButton.click()

        # define set of parameters
        self.pulse_setting_dir = None
        self.pulse_setting_files = None
        self.pulse_setting_shot = None
        
        logger.info('Starting PPPAT')        
        
    def menu_bar(self):
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
        # Define the various collabsible panels

        self.panel_rappels = QCollapsibleToolbox(child=EiCReminderWidget(), title='Cahier de liaison des EiC / EiC\'s Notebook')
        self.panel_pre_pulse = QCollapsibleToolbox(child=PrePulseAnalysisWidget(), title='Pre-pulse Analysis')
        self.panel_post_pulse = QCollapsibleToolbox(child=QTextBrowser(), title='Post-pulse Analysis')
        self.panel_pulse_display = QCollapsibleToolbox(child=QTextBrowser(), title='Pre-pulse Display')
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

    def load_pulse_setting(self):
        # decide how to load the pulse setting depending on the GUI status
        if self.panel_pre_pulse.widget.radio_sl.isChecked():
            pass
            # TODO

        if self.panel_pre_pulse.widget.radio_file.isChecked():
            if not self.pulse_setting_dir:
                logger.error('Browse a directory first !')
            else:
                self.panel_pre_pulse.widget.pulse_setting_origin.setText(
                        self.pulse_setting_dir)
                logger.info('load pulse setting from file')
                
        if self.panel_pre_pulse.widget.radio_shot.isChecked():
            shot_nb = self.panel_pre_pulse.widget.edit_shot.text()
            if not shot_nb:
                logger.error('Set pulse number first !')
            else:
                logger.info(f'load pulse setting from WEST shot #{shot_nb}')
                
                self.panel_pre_pulse.widget.pulse_setting_origin.setText(
                        f'WEST shot number {shot_nb}')
                self.pulse_setting_shot = int(shot_nb)
                



    def browse_pulse_setting_directory(self):
        """
        Open a file dialog to select the directory which contains the sup.xml 
        and dp.xml files. 
        
        # TODO : also deals with zip or tar.gz file containing the .xml files
        """
        # if user click on the 'browse' button, then automatically select
        # the "file" mode
        self.panel_pre_pulse.widget.radio_file.setChecked(True)
        # open file dialog
        _pulse_setting_dir = \
            QFileDialog.getExistingDirectory(self,
                                             'Select XML/DCS files directory',
                                             directory=QDir.currentPath()
                                             )
        _pulse_setting_files = {
                'sup': f'{_pulse_setting_dir}/Sup.xml',
                'dp': f'{_pulse_setting_dir}/DP.xml'
                }

        # test if both file dp.xml and sup.xml exist. If not -> error msg   
        if os.path.isfile(_pulse_setting_files['dp']) and \
            os.path.isfile(_pulse_setting_files['sup']):
            
            self.pulse_setting_dir = _pulse_setting_dir
            self.pulse_setting_files  = _pulse_setting_files
            logger.info(f'Pulse setting dir set to {self.pulse_setting_dir}')
            logger.info(f'Pulse settinf files exist into {self.pulse_setting_dir}')
        else:
            logger.error("One of the pulse setting file does not exist!" )
            
#        h = GuiLogger()
#        h.edit = self.log 
#        logging.getLogger().addHandler(h)
         
            
            
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
