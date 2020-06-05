# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:11:36 2020

@author: JH218595
"""

import sys
from collections import defaultdict  # to store data conviently in

import qtpy.QtGui as QtGui
import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets

from qtpy.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QHBoxLayout, QVBoxLayout, QAction, qApp, QLabel,
                            QScrollArea, QTextBrowser, QFrame, QTextEdit, QLineEdit,
                            QFileDialog, QPlainTextEdit, QTableWidgetItem, QToolButton,
                            QMessageBox, QComboBox, QCompleter, QListWidget, 
                            QSplitter, QStyleFactory, QTabWidget, QTabBar)
from qtpy.QtGui import QIcon, QCursor, QDesktopServices
from qtpy.QtCore import QDir, Slot, Signal, Qt, QUrl, QStringListModel, QSize

from pppat.ui.collapsible_toolbox import QCollapsibleToolbox
from pppat.ui.control_room.signals import signals, get_sig
from pppat.libpulse.utils import wait_cursor
from pppat.libpulse.pulse_settings import PulseSettings

MINIMUM_WIDTH = 800



# class TabBarPlus(QTabBar):
#     """Tab bar that has a plus button floating to the right of the tabs."""

#     plusClicked = Signal()

#     def __init__(self):
#         super().__init__()

#         # Plus Button
#         self.plusButton = QPushButton("+")
#         self.plusButton.setParent(self)
#         self.plusButton.setFixedSize(20, 20)  # Small Fixed size
#         self.plusButton.clicked.connect(self.plusClicked.emit)
#         self.movePlusButton() # Move to the correct location

#     def sizeHint(self):
#         """Return the size of the TabBar with increased width for the plus button."""
#         sizeHint = QTabBar.sizeHint(self) 
#         width = sizeHint.width()
#         height = sizeHint.height()
#         return QSize(width+25, height)

#     def resizeEvent(self, event):
#         """Resize the widget and make sure the plus button is in the correct location."""
#         super().resizeEvent(event)

#         self.movePlusButton()


#     def tabLayoutChange(self):
#         """This virtual handler is called whenever the tab layout changes.
#         If anything changes make sure the plus button is in the correct location.
#         """
#         super().tabLayoutChange()

#         self.movePlusButton()

#     def movePlusButton(self):
#         """Move the plus button to the correct location."""
#         # Find the width of all of the tabs
#         size = sum([self.tabRect(i).width() for i in range(self.count())])
#         # size = 0
#         # for i in range(self.count()):
#         #     size += self.tabRect(i).width()

#         # Set the plus button location in a visible area
#         h = self.geometry().top()
#         w = self.width()
#         if size > w: # Show just to the left of the scroll buttons
#             self.plusButton.move(w-54, h)
#         else:
#             self.plusButton.move(size, h)

def list_signals(pulse=None):
    sig_list = []
    for sig in signals:
        sig_list.append(sig+': '+signals[sig]['label'])    
    return sig_list

def list_waveforms(pulse=None):
    # TODO return waveform names
    return ['toto', 'tata']

class Panel(QSplitter):
    def __init__(self, parent=None):
        QSplitter.__init__(self, Qt.Horizontal, parent=parent)
        
        # Create the list of all the signals to display
        self.sig_list = list_signals()
        self.wf_list  = list_waveforms()
            
        # List of signals to plot
        self._signals = []
        # List of pulses to plot
        self._pulses = []
        
        # Dictionnary of signals data. Contain (y,t,pulse)
        self.data = defaultdict(dict)
        
        # GUI Creation
        self._create_left_side()
        self._create_right_side()
        
        # create a vertical splitter with signal list at left and plot at right
        # self.splitter_vert = QSplitter(Qt.Horizontal)
        self.addWidget(self.panel_left)
        self.addWidget(self.panel_right)
        
        # Allows the vertical splitter to collapse
        self.setCollapsible(0, True)
    
    # Getter and setter of Panel properties
    @property
    def signals(self):
        return self._signals

    @signals.setter 
    def signals(self, siglist):
        self._signals = siglist

    @property
    def pulses(self):
        return self._pulses
    
    @pulses.setter 
    def pulses(self, pulselist):
        self._pulses = pulselist
        
    def get_pulse_list(self):
        'Convert the pulse list in meaningfull list of pulses'
        # TODO: convert 0, -1, etc to meaning values
        return self.pulses               

    def update(self):
        self.update_data()
        self.update_plot()

    def update_data(self):
        # TODO : retrieve only missing data 
        # TODO : paralilize data retrieval
        with wait_cursor():
            for pulse in self.get_pulse_list():
                for sig in self.signals:
                    signame = sig.split(':')[0]
                    print(f'Retrieve {signame} for #{pulse}...')
                    _y, _t = get_sig(pulse, signals[signame]) 


    def update_plot(self):
        for sig in self.signals:
            print('UPDATE:', sig)

    def _create_right_side(self):
        'GUI: Create right side (plot window)'
        self.panel_right = QTextEdit()
        
    def _create_left_side(self):
        'GUI; Create left side (search bar and list of signals)'
        # Search bar to search and filter signals or waveform name
        self.qt_search_bar = QLineEdit()
        # Select box for choice between standard signals or DCS settings
        self.qt_sig_type = QComboBox()
        self.qt_sig_type.addItem('signals')
        self.qt_sig_type.addItem('PCS waveforms')
        self.qt_sig_type.activated.connect(self._setup_signal_list)
        self.widget_search = QWidget()
        self.widget_search_layout = QHBoxLayout()
        self.widget_search_layout.addWidget(self.qt_search_bar)
        self.widget_search_layout.addWidget(self.qt_sig_type)
        self.widget_search.setLayout(self.widget_search_layout)
        

        ## Create the list of signals
        self.signals_list = QListWidget()
        self._setup_signal_list()
        # allows selecting multiple number of signals
        self.signals_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # define right click context menu
        self.signals_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.signals_list.customContextMenuRequested[QtCore.QPoint].connect(self._item_context_menu_event)
        
        ## Creating the panel
        self.panel_left = QWidget()
        self.panel_left_layout = QVBoxLayout()
        
        self.panel_left_layout.addWidget(self.widget_search)
        self.panel_left_layout.addWidget(self.signals_list)
        self.panel_left.setLayout(self.panel_left_layout)

    # @Slot(str)
    def _setup_signal_list(self, text):
               
        if text == 'signals':
            qt_sig_list = self.sig_list
        elif text == 'PCS waveforms':
            qt_sig_list = self.wf_list
        
        # Setup the search bar and completion style  
        model = QStringListModel()
        model.setStringList(self.sig_list)
        
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setModelSorting(QCompleter.UnsortedModel)
        completer.setFilterMode(Qt.MatchContains)
            
        self.qt_search_bar.setCompleter(completer)
        self.signals_list.clear()
        self.signals_list.addItems(qt_sig_list)        
        
    def _item_context_menu_event(self, event):
        'GUI: signal list context menu'
        right_menu = QtWidgets.QMenu(self.signals_list)
        action_add = QtWidgets.QAction("Add", self, triggered=self.add_signals)
        action_rem = QtWidgets.QAction("Remove", self, triggered=self.remove_signals)
        right_menu.addAction(action_add)
        right_menu.addAction(action_rem)
        right_menu.exec_(QtGui.QCursor.pos())
        
    def add_signals(self, event):
        '''
        Add a list signals to the list of signals to be plotted
        '''
        selections  = [item.text() for item in self.signals_list.selectedItems()]
        for sig in selections:
            if sig:
                # add the signals to the list of signals to be plotted
                self.signals.append(sig)
                # put the signal name in red in the list of signals
                qt_items = self.signals_list.findItems(sig, Qt.MatchExactly)
                for qt_item in qt_items:
                    qt_item.setForeground(Qt.red)
        # update plots 
        self.update()
        
    def remove_signals(self, event):
        '''
        Remove a list of signal of the list of signals to be plotted
        '''
        selections  = [item.text() for item in self.signals_list.selectedItems()]
        for sig in selections:
            if sig in self.signals:
                # remove the signame from the list of signals to be plotted
                self.signals.remove(sig)
                # put back the signal name in black
                qt_items = self.signals_list.findItems(sig, Qt.MatchExactly)
                for qt_item in qt_items:
                    print(qt_item)
                    qt_item.setForeground(Qt.black)
        # update plot
        self.update()

        
    # def handleSplitterButton(self, left=True):
    #     if not all(self.splitter_vert.sizes()):
    #         self.splitter_vert.setSizes([1, 1])
    #     elif left:
    #         self.splitter_vert.setSizes([0, 1])
    #     else:
    #         self.splitter_vert.setSizes([1, 0])           
        
class ControlRoom(QMainWindow):
    """
    Central GUI class which also serves as main Controller
    """
    def __init__(self, parent=None):
        super(ControlRoom, self).__init__(parent)  # initialize the window
        ## Control Room Properties
        # Window properties
        self.setWindowTitle('Control Room [WEST]')
        self.title = 'Control Room [WEST]'
        # self.iconName = 'icon.png'

        # self.left =
        # self.top =
        # self.width =
        # self.height =
        # self.setGeometry(self.left, self.top, self.width, self.height)


        # setup window size to 90% of avail. screen height
        rec = QApplication.desktop().availableGeometry()
        self.resize(MINIMUM_WIDTH, .9*rec.height())

        # Menu Bar
        self.menu_bar()


        
        # create pulse number edit bar
        self.qt_pulses = QLineEdit()
        self.qt_pulses.editingFinished.connect(self.update_pulses)
        # TODO : validator
        # .setValidator(QIntValidator())
        
        
        # create tabs. Panels are defined inside each tab
        # self.tab = TabBarPlus()
        self.qt_tabs = QTabWidget()
        # self.qtabwidget.setTabBar(self.tab)
                # Signals
        # self.tab.plusClicked.connect(self.create_tab)
        # self.tab.tabMoved.connect(self.moveTab)
        
        
        # create panels
        self.panels = [Panel(), 
                       Panel()]
        
        # tab_panels = QWidget()
        # # TODO : make handlers
        # tab_panels_layout = QVBoxLayout()
        # for panel in panels:
        #     tab_panels_layout.addWidget(panel)
        # tab_panels.setLayout(tab_panels_layout)
         
        tab_panels = QSplitter(Qt.Vertical)
        for panel in self.panels:
            tab_panels.addWidget(panel)
        

        tab_index1 = self.qt_tabs.addTab(tab_panels, 'Traces #1')
        self.qt_tabs.setTabsClosable(True)  
        self.qt_tabs.setMovable(True)
        self.qt_tabs.tabCloseRequested.connect(self.close_handler)     
        
        # Central Widget
        self.qt_central = QWidget()
        self.qt_central_layout = QVBoxLayout()
        self.qt_central_layout.addWidget(self.qt_pulses)
        self.qt_central_layout.addWidget(self.qt_tabs)
        self.qt_central.setLayout(self.qt_central_layout)
        self.setCentralWidget(self.qt_central)

    def update_pulses(self):
        # Get the text from the QLineEdit
        text = self.qt_pulses.text()
        # split ',' -> pulses number
        # TODO check integer
        pulses = [int(p) for p in text.split(',')]
        print('NEW PULSE LIST:', pulses)
        # update pulse list and plots for each panels
        for panel in self.panels:
            panel.pulses = pulses
            panel.update()

    def add_tab(self):
        index = self.qt_tabs.count() + 1
        self.qt_tabs.addTab(QWidget(), "Traces #%d" % index)
        self.qt_tabs.setCurrentIndex(index)
        
        
    @Slot(int)
    def close_handler(self, index):
        """
            Removes a tab with the specified index, but first deletes the widget it contains. 
        """
        reply = QMessageBox.question(
            self, "Message",
            "Close this tab?",
            QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            # gets the widget
            widget = self.qt_tabs.widget(index)
    
            # if the widget exists
            if widget:
                # removes the widget
                widget.deleteLater()
                
            # removes the tab of the QTabWidget
            self.qt_tabs.removeTab(index)    
        else:
            pass    
        
    @Slot(int)
    def qtabwidget_currentchanged(self, index):
        print(f"The new index of the current page: {index}")
       
           
    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed 
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()
        else:
            pass    
 
        
    def menu_bar(self):
        """ Menu bar """
        self.menuBar = self.menuBar()

        # file menu
        menu_file = self.menuBar.addMenu('&File')
        action_file_exit = QAction('&Exit', self)
        action_file_exit.setStatusTip('Exit')
        action_file_exit.setShortcut('Ctrl+Q')
        action_file_exit.triggered.connect(self.closeEvent)
        menu_file.addAction(action_file_exit)
        
        menu_tabs = self.menuBar.addMenu('&Tabs')
        action_tab_add_tab = QAction('&Add Tab', self)
        action_tab_add_tab.triggered.connect(self.add_tab)
        menu_tabs.addAction(action_tab_add_tab)        

        

    # def generate_central_widget(self):
    #     """
    #     Define the central widget, which contain the main GUI of the app,
    #     mostly the various tools.
    #     """
    #     # Define the various collabsible panels (leave "child=" avoid Qt bug)
    #     self.panel_rappels = QCollapsibleToolbox(child=EiCReminderWidget(), title='Cahier de liaison des EiC / EiC\'s Notebook')
    #     self.panel_pre_pulse = QCollapsibleToolbox(child=PrePulseAnalysisWidget(), title='Pre-pulse Analysis')
    #     self.panel_pulse_display = QCollapsibleToolbox(child=PrePulseDisplayWidget(), title='Pre-pulse Display')
    #     self.panel_post_pulse = QCollapsibleToolbox(child=PostPulseAnalysisWidget(), title='Post-pulse Analysis')
    #     self.panel_log = QCollapsibleToolbox(child=QPlainTextEditLogger(), title='Logs')
    #     self.panel_console = QCollapsibleToolbox(child=ConsoleWidget(), title='Python Console')

    #     # stacking the collapsible panels vertically
    #     vbox = QVBoxLayout()
    #     vbox.addWidget(self.panel_rappels)
    #     vbox.addWidget(self.panel_pre_pulse)
    #     vbox.addWidget(self.panel_pulse_display)
    #     vbox.addWidget(self.panel_post_pulse)
    #     vbox.addWidget(self.panel_log)
    #     vbox.addWidget(self.panel_console)

    #     # making the whole panels scrollable
    #     # The scrollbar should be set for a widget, here a dummy one
    #     collaps = QWidget()
    #     collaps.setLayout(vbox)
    #     scroll = QScrollArea(self)
    #     scroll.setWidget(collaps)
    #     scroll.setWidgetResizable(True)
    #     self.central_widget = scroll


# TODO : Dark Theme
# https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets
        
def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))            
    win = ControlRoom()
    win.show()
    sys.exit(app.exec_())
    return app.exec_()

# Running this script will launch a ControlRoom instance
if __name__ == '__main__':
    main()
