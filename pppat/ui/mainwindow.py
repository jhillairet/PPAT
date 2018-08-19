from qtpy.QtWidgets import (QMainWindow, QApplication, QToolBox, QWidget,
                            QHBoxLayout, QVBoxLayout, QAction, qApp, 
                            QScrollArea, QTextBrowser, QFrame)
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
from pppat.ui.reminder import EiCReminderWidget
from pppat.ui.console import ConsoleWidget
from pppat.ui.collapsibleToolBox import QCollapsibleToolbox

import logging
logger = logging.getLogger(__name__)

MINIMUM_WIDTH = 800


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # initialize the window
        # Window properties
        self.setWindowTitle('Pre & Post Pulse Analysis Tool for WEST')

        # setup window size to 90% of avail. screen height
        rec = QApplication.desktop().availableGeometry()
        self.resize(MINIMUM_WIDTH, .9*rec.height())

        # Menu Bar
        self.menu_bar()

        # Set the toolBox as the central Widget
        self.generate_central_widget()
        self.setCentralWidget(self.central_widget)

        # Status Bar
        self.statusBar().showMessage('PPPAT')

        # Application icon
        self.setWindowIcon(QIcon('resources/icons/pppat.png'))

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
#        # Qt ToolBox setup
#        self.tbx = QToolBox(parent=self)
#        StyleSheet = """
#        
#        /* Window{background: #b8cdee;}*/
#        
#        QToolBox::tab {
#            /* border-image: url(resources/95_Alu_gebuerstet.jpg); */
#            border: 1px solid #C4C4C3;
#            color: black;
#            font-size:12pt;
#            font: bold;
#            background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
#                                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
#                                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
#
#        }
#        
#        QToolBox::tab:first {
#            background: #4ade00;
#            color: black;
#        }
#        
#        QToolBox::tab:last {
#            background: #f95300;
#            color: black;
#        }
#        
#        QToolBox::tab:selected { /* italicize selected tabs */
#            font: italic bold;
#            color: white;
#            /* border-image: url(resources/brushed_aluminium_dark.jpg); */
#            /*     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
#                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
#                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);*/
#        }
#        """
#
#        self.tbx.setStyleSheet(StyleSheet)
#        
#        self.tbx.setMinimumWidth(self.width())
#        self.tbx.addItem(EiCReminderWidget(), '&Rappels')
#        self.tbx.addItem(QWidget(), 'Pre-Pulse &Analysis')
#        self.tbx.addItem(QWidget(), 'Pre-Pulse Setup &Display')
#        self.tbx.addItem(QWidget(), '&Post-Pulse Analysis')
#        self.tbx.addItem(QWidget(), '&Log')
#        self.console = ConsoleWidget()
#        self.tbx.addItem(self.console, '&Console')       
#        
#        # Horizontal layout allow resizing widget in the horizontal direction
#        # keeping vertical size constant
#        hbox = QHBoxLayout()
#        hbox.setSpacing(0)    
#        hbox.addWidget(self.tbx)      
#        self.setLayout(hbox)
#        
#        # the central widget only corresponds to the tool box for now
#        self.central_widget = self.tbx
        
        # Rappels aux EiC
        rappels = QCollapsibleToolbox(child=EiCReminderWidget(), title='Rappels aux EiC')
        pre_pulse = QCollapsibleToolbox(child=None, title='Pre-pulse Analysis')
        post_pulse = QCollapsibleToolbox(child=None, title='Post-pulse Analysis')
        pulse_display = QCollapsibleToolbox(child=None, title='Pre-pulse Display')
        log = QCollapsibleToolbox(child=QTextBrowser(), title='Logs')
        console = QCollapsibleToolbox(child=ConsoleWidget(), title='Console')
        
        # stacking the collapsible panels
        vbox = QVBoxLayout()
        vbox.addWidget(rappels)
        vbox.addWidget(pre_pulse)
        vbox.addWidget(pulse_display)
        vbox.addWidget(post_pulse)
        vbox.addWidget(log)
        vbox.addWidget(console)

        # making the whole panels scrollable
        # The scrollbar should be set for a widget, here a dummy one
        collaps = QWidget()
        collaps.setLayout(vbox)        
        scroll = QScrollArea(self)
        scroll.setWidget(collaps)
        scroll.setWidgetResizable(True) # do not forget !
        self.central_widget = scroll
        
        # open some panels at startup
        rappels.toggleButton.click() 
        
                    
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
