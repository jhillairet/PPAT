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
                            QFileDialog, QInputDialog,
                            QPlainTextEdit, QTableWidgetItem, QToolButton,
                            QMessageBox, QComboBox, QCompleter, QListWidget, 
                            QSplitter, QStyleFactory, QTabWidget, QTabBar)
from qtpy.QtGui import QIcon, QCursor, QDesktopServices
from qtpy.QtCore import QDir, Slot, Signal, Qt, QUrl, QStringListModel, QSize

from pppat.ui.collapsible_toolbox import QCollapsibleToolbox
from pppat.ui.control_room.signals import signals, get_sig
from pppat.libpulse.utils import wait_cursor
from pppat.libpulse.pulse_settings import PulseSettings

MINIMUM_WIDTH = 800



def list_signals(pulse=None) -> list:
    """
    List all WEST signals names for a given pulse. If no pulse, default list names. 

    Parameters
    ----------
    pulse : int, optional
        WEST pulse number. The default is None.

    Returns
    -------
    wf_names: list
        list of all signal names

    """
    sig_list = []
    for sig in signals:
        sig_list.append(sig+': '+signals[sig]['label'])    
    return sig_list

def list_waveforms(pulse=None) -> list:
    """
    List all waveform names for a given pulse. If no pulse, default list names. 

    Parameters
    ----------
    pulse : int, optional
        WEST pulse number. The default is None.

    Returns
    -------
    wf_names: list
        list of all waveform names

    """
    if pulse:
        ps = PulseSettings(pulse)
        return ps.waveform_names
    else:
        with open('pppat/ui/control_room/waveform_names.txt') as file:
            data = file.read()
            
        return data.splitlines()

class ControlRoomConfiguration():
    def __init__(self, fname=None):
        """
        Control Room Configuration. Describe the configuration of a Control Room session.
        
        This configuration saves:
            - Tabs properties (number and names)
            - Panels properties for each Tabs (number)
            - selected curves for each panels

        Parameters
        ----------
        fname : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        self._pulses = [0]
        self._panels = []
        self._tabs = defaultdict()
        self.default_signal_type = 'PCS waveforms' # 'signals' or 'PCS waveforms'
        
    @property
    def pulses(self) -> list:
        # get last pulse
        return self._pulses
    
    @pulses.setter
    def pulses(self, pulses: list):
        self._pulses = pulses
    
    @property
    def panels(self):
        return self._panels

    @panels.setter
    def panels(self, panels):
        self._panels = panels

class PanelConfiguration:
    def __init__(self):
        """
        Panel Configuration.
        
        Contains:
            - the default type of signal
            - the selected signals
            - the type plotting backend 

        Parameters
        ----------
        control_room_config : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.default_signal_type = 'PCS'
        self.selected_signals = []
        self.backend = 'matplotlib'

class Panel(QSplitter):
    def __init__(self, parent=None, panel_config: PanelConfiguration=None):
        """
        Panel

        A Panel is a QSplitter GUI which contains a search bar at left and a plot at right   

        """
        QSplitter.__init__(self, Qt.Horizontal, parent=parent)

        # Panel configuration
        if not panel_config:
            self.config = PanelConfiguration()
        else:
            self.config = panel_config
        
        # list of all the signals to display
        self.sig_list = list_signals()
        self.wf_list  = list_waveforms()
            
        # GUI Creation
        self._create_left_side()
        self._create_right_side()
        
        # create a vertical splitter with signal list at left and plot at right
        # self.splitter_vert = QSplitter(Qt.Horizontal)
        self.addWidget(self.panel_left)
        self.addWidget(self.panel_right)
        
        # Allows the vertical splitter to collapse
        self.setCollapsible(0, True)
        
        # set configuration
        self.update_selected_signals()
    
    # Getter and setter of Panel properties
    @property
    def signals(self):
        return self._signals

    @signals.setter 
    def signals(self, siglist):
        self._signals = siglist

    def update(self, pulses: list=None):
        if pulses:
            self.update_data(pulses)
            self.update_plot(pulses)

    def update_data(self, pulses: list=None):
        # TODO : retrieve only missing data 
        # TODO : paralilize data retrieval
        if pulses:
            with wait_cursor():
                for pulse in pulses:
                    for sig in self.config.selected_signals:
                        signame = sig.split(':')[0]
                        print(f'Retrieve {signame} for #{pulse}...')
                        _y, _t = get_sig(pulse, signals[signame]) 


    def update_plot(self, pulses: list=None):
        for sig in self.config.selected_signals:
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
        self.qt_sig_type.addItem('PCS waveforms')
        self.qt_sig_type.addItem('signals')
        self.qt_sig_type.activated[str].connect(self._setup_signal_list)
        self.widget_search = QWidget()
        self.widget_search_layout = QHBoxLayout()
        self.widget_search_layout.addWidget(self.qt_search_bar)
        self.widget_search_layout.addWidget(self.qt_sig_type)
        self.widget_search.setLayout(self.widget_search_layout)
        

        ## Create the list of signals
        self.qt_signals_list = QListWidget()
        # default signal list
        self._setup_signal_list('PCS waveforms')
        # allows selecting multiple number of signals
        self.qt_signals_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # define right click context menu
        self.qt_signals_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.qt_signals_list.customContextMenuRequested[QtCore.QPoint].connect(self._item_context_menu_event)
        
        ## Creating the panel
        self.panel_left = QWidget()
        self.panel_left_layout = QVBoxLayout()
        
        self.panel_left_layout.addWidget(self.widget_search)
        self.panel_left_layout.addWidget(self.qt_signals_list)
        self.panel_left.setLayout(self.panel_left_layout)

    @Slot(str)
    def _setup_signal_list(self, text):
        print(text)
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
        self.qt_signals_list.clear()
        self.qt_signals_list.addItems(qt_sig_list)        
        
    def _item_context_menu_event(self, event):
        'GUI: signal list context menu'
        right_menu = QtWidgets.QMenu(self.qt_signals_list)
        action_add = QtWidgets.QAction("Add", self, triggered=self.add_selected_signals)
        action_rem = QtWidgets.QAction("Remove", self, triggered=self.remove_selected_signals)
        right_menu.addAction(action_add)
        right_menu.addAction(action_rem)
        right_menu.exec_(QtGui.QCursor.pos())

    def update_selected_signals(self):
        '''
        Update the color of the signals in signal list to identify selected items
        '''
        # put all in black (default color)
        for qt_item in self.qt_signals_list.findItems('*', Qt.MatchWildcard):
            qt_item.setForeground(Qt.black)
        # put selected signals corresponding items in red
        for sig in self.config.selected_signals:
            qt_items = self.qt_signals_list.findItems(sig, Qt.MatchExactly)
            for qt_item in qt_items:
                qt_item.setForeground(Qt.red)
        
    def add_selected_signals(self, event):
        '''
        Add a list signals to the list of signals to be plotted
        '''
        selections  = [item.text() for item in self.qt_signals_list.selectedItems()]
        for sig in selections:
            if sig:
                # add the signals to the list of signals to be plotted
                self.config.selected_signals.append(sig)
        
        print('selected signals are now:', self.config.selected_signals)
        # update selected signals list
        self.update_selected_signals()
        # update plots panel
        self.update()
        
    def remove_selected_signals(self, event):
        '''
        Remove a list of signal of the list of signals to be plotted
        '''
        selections  = [item.text() for item in self.qt_signals_list.selectedItems()]
        for sig in selections:
            if sig in self.config.selected_signals:
                # remove the signame from the list of signals to be plotted
                self.config.selected_signals.remove(sig)

        print('selected signals are now:', self.config.selected_signals)
        # update selected signals list
        self.update_selected_signals()
        # update plot panel
        self.update()

   
        
class ControlRoom(QMainWindow):
    """
    Central GUI class which also serves as main Controller
    """
    def __init__(self, parent=None, config=None):
        """
        Control Room Application

        Parameters
        ----------
        parent : TYPE, optional
            DESCRIPTION. The default is None.
        config : ControlRoolConfiguration, optional
            ControlRoom configuration. The default is None (default config).

        Returns
        -------
        None.

        """
        super(ControlRoom, self).__init__(parent)  # initialize the window
        ## Control Room Properties
        # Window properties
        self.setWindowTitle('Control Room [WEST]')
        self.title = 'Control Room [WEST]'
        # self.iconName = 'icon.png'

        # Configuration
        if config:
            self.config = config
        else:
            self.config = ControlRoomConfiguration()
        
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
        self.qt_pulses = self.ui_pulses()
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
        # self.add_panel()
        # self.add_panel()
        
        # tab_panels = QWidget()
        # # TODO : make handlers
        # tab_panels_layout = QVBoxLayout()
        # for panel in panels:
        #     tab_panels_layout.addWidget(panel)
        # tab_panels.setLayout(tab_panels_layout)
        
        panels = [Panel(), Panel()]

        self.add_tab(panels)     
        # self.qt_tabs.setCurrentWidget(page)
        # tab_index1 = self.qt_tabs.addTab(page, 'Traces #1')

        self.qt_tabs.setTabsClosable(True)  
        self.qt_tabs.setMovable(True)
        self.qt_tabs.tabCloseRequested.connect(self.close_tab)     
        
        # Central Widget
        self.qt_central = QWidget()
        self.qt_central_layout = QVBoxLayout()
        self.qt_central_layout.addWidget(self.qt_pulses)
        self.qt_central_layout.addWidget(self.qt_tabs)
        self.qt_central.setLayout(self.qt_central_layout)
        self.setCentralWidget(self.qt_central)

    def pulses_str(self) -> str:
        '''
        Pulse numbers string, separated by commas

        Returns
        -------
        pulses_str: str
            pulses number separated by commas

        '''
        return ', '.join([str(pulse) for pulse in self.config.pulses])

    def ui_pulses(self):
        '''
        Pulse(s) edit bar
        '''
        return QLineEdit(self.pulses_str())

    def update_pulses(self) -> None:
        '''
        Update the list of pulses from the GUI edit bar
        '''
        # Get the text from the QLineEdit
        text = self.qt_pulses.text()
        # split ',' -> pulses number
        # TODO check integer
        pulses = [int(p) for p in text.split(',')]
        print('NEW PULSE LIST:', pulses)
        # update pulse list and plots for each panels
        for panel in self.config.panels:
            panel.pulses = pulses
            panel.update()

    def add_tab(self, panels: list=None, label: str=None) -> None:
        '''
        Add a new Tab 
        '''
        index = self.qt_tabs.count() + 1
        # default Tab label
        if not label:
            label = "Traces #%d" % index
        # default list of Panels
        if not panels:
            panels = [Panel()]
        # Add the panels vertically in a Splitter and create Tab
        page = QSplitter(Qt.Vertical)
        for panel in panels:
            page.addWidget(panel)       
        self.qt_tabs.addTab(page, label)
        # focus on the new created tab
        self.qt_tabs.setCurrentWidget(page)

    def rename_current_tab(self):
        ''' 
        display a dialog to rename the current tab
        '''
        current_tab_index = self.qt_tabs.currentIndex()
        new_label, ok = QInputDialog.getText(self, "New Tab Label", "Tab Label:",
                                 QLineEdit.Normal, 
                                 self.qt_tabs.tabText(current_tab_index))
        if ok:
            self.qt_tabs.setTabText(current_tab_index, new_label)
        
    def close_current_tab(self):
        '''
        Close the current Tab
        '''
        tab_index = self.qt_tabs.currentIndex()
        print(f'user want to close {tab_index}')
        self.close_tab(tab_index)

    @Slot(int)
    def close_tab(self, index):
        """
        Removes a Tab with the specified index, but first deletes the widget it contains. 
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
        
        # Tabs
        menu_tabs = self.menuBar.addMenu('&Tabs')
        action_add_tab = QAction('&Add Tab', self)
        action_add_tab.triggered.connect(self.add_tab)
        menu_tabs.addAction(action_add_tab)
        
        action_rename_tab = QAction('&Rename Current Tab', self)
        action_rename_tab.triggered.connect(self.rename_current_tab)
        menu_tabs.addAction(action_rename_tab)
        
        action_remove_tab = QAction('&Close Current Tab', self)
        action_remove_tab.triggered.connect(self.close_current_tab)
        menu_tabs.addAction(action_remove_tab)
        
        # Panels
        menu_panels = self.menuBar.addMenu('&Panels')
        action_add_panel = QAction('&Add Panel', self)
        action_add_panel.triggered.connect(self.add_panel)
        menu_panels.addAction(action_add_panel)
        
        action_remove_panel = QAction('&Remove Panel', self)
        action_remove_panel.triggered.connect(self.remove_panel)
        menu_panels.addAction(action_remove_panel)        
        
    def add_panel(self, tab_index=None):
        print('Before adding a panel:', self.config.panels)
        self.config.panels.append(Panel())
        print('After adding a panel:', self.config.panels)

    def remove_panel(self, panel_index: int, tab_index=None):
        pass
    
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
