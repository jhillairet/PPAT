# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:11:36 2020

@author: JH218595
"""

import sys
import numpy as np
import pickle
import pyqtgraph as pg
## Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

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
from pppat.libpulse.utils import wait_cursor, nested_dict
from pppat.libpulse.pulse_settings import PulseSettings
from pppat.libpulse.utils_west import last_pulse_nb
from pppat.libpulse.waveform import get_waveform


MINIMUM_WIDTH = 800

# # Enable antialiasing for prettier plots
# pg.setConfigOptions(antialias=True)

def translate_pulse_numbers(pulses: list) -> list:
    '''
    Convert the pulse list edited by the user in the GUI to meaningfull WEST pulse numbers.
    
    For example translate 0 is the next pulse, -1 the last achieved pulse, etc

    Parameters
    ----------
    pulses : list of integers 
        List of WEST pulse numbers (shot numbers and shortcuts like 0, -1, etc).

    Returns
    -------
    west_pulses: list of integers 
        List of WEST pulse numbers (all positives and shot numbers >50000).

    '''
    west_pulses = np.array(pulses, dtype=int)
    # if there are any negative number, get the lastest pulse number
    # and translate negative numbers into meaningfull pulse numbers
    if np.any(west_pulses <= 0):
        last_achieved_plasma = last_pulse_nb()
        west_pulses[west_pulses <= 0] += last_achieved_plasma + 1
    # convert back to a list (of integer)
    return [int(pulse) for pulse in west_pulses]

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

       

# class ControlRoomConfiguration():
#     def __init__(self, fname=None):
#         """
#         Control Room Configuration. Describe the configuration of a Control Room session.
        
#         This configuration saves:
#             - Tabs properties (number and names)
#             - Panels properties for each Tabs (number)
#             - selected curves for each panels

#         Parameters
#         ----------
#         fname : TYPE, optional
#             DESCRIPTION. The default is None.

#         Returns
#         -------
#         None.

#         """
#         self._pulses = [0]
#         self._panels = []
#         self._tabs = []
#         self.default_signal_type = 'PCS waveforms' # 'signals' or 'PCS waveforms'
#         self.setup = nested_dict()
        
#     @property
#     def pulses(self) -> list:
#         # get last pulse
#         return self._pulses
    
#     @pulses.setter
#     def pulses(self, pulses: list):
#         self._pulses = pulses
    
#     @property
#     def panels(self):
#         return self._panels

#     @panels.setter
#     def panels(self, panels):
#         self._panels = panels
        
#     def __repr__(self):
#         description = f'Control Room Configuration: {len(self._tabs)} Tabs containing {self._panels}'
#         return description
        
#     def export(self, filename: str):
#         """
#         Export the configuration of a ControlRoom session.

#         Parameters
#         ----------
#         filename : str
#             configuration file.

#         Returns
#         -------
#         None.

#         """
#         pass
#         # >>> import json
#         # >>> config = {'handler' : 'adminhandler.py', 'timeoutsec' : 5 }
#         # >>> json.dump(config, open('/tmp/config.json', 'w'))
#         # >>> json.load(open('/tmp/config.json'))   
#         # {u'handler': u'adminhandler.py', u'timeoutsec': 5}


    

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
        self.default_signal_type = 'PCS waveforms'
        self.selected_signals = []
        self.backend = 'matplotlib'
        self.data = nested_dict()

class Panel(QSplitter):
    def __init__(self, parent=None, config: PanelConfiguration=None):
        """
        Panel

        A Panel is a QSplitter GUI which contains a search bar at left and a plot at right   

        """
        QSplitter.__init__(self, Qt.Horizontal, parent=parent)

        # Panel configuration
        if not config:
            self.config = PanelConfiguration()
        else:
            self.config = config
        
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
            pulses = translate_pulse_numbers(pulses)
            self.update_data(pulses)
            self.update_plot(pulses)

    def update_data(self, pulses: list=None, reload: bool=False):
        """
        Update the signals data.

        Parameters
        ----------
        pulses : list, optional
            WEST pulse list. The default is None.
        reload : bool, optional
            Reload data already downloaded? The default is False.
        """
        # TODO : retrieve only missing data 
        # TODO : paralilize data retrieval
        if pulses:
            print(f'Updating data for pulses {pulses}')
            with wait_cursor():
                for pulse in pulses:
                    if not self.config.data[pulse]['PulseSetting']:
                        ps = PulseSettings(pulse)
                        self.config.data[pulse]['PulseSetting'] = ps
                    
                    print(f'Updating data for pulse {pulse}')
                    for sig in self.config.selected_signals:
                        if self.config.data[pulse][sig]:
                            print('{sig} for #{pulse} already downloaded. Skipping...')
                        else:
                            print(f'Retrieve {sig} for #{pulse}...')
                            if sig.startswith('rts:'):
                                wf = get_waveform(sig, self.config.data[pulse]['PulseSetting'].waveforms)
                                # remove 40 seconds to match pulses
                                self.config.data[pulse][sig]['times'] = wf.times - 40
                                self.config.data[pulse][sig]['values'] = wf.values
                            else:                       
                                signame = sig.split(':')[0]
                                _y, _t = get_sig(pulse, signals[signame]) 
                                self.config.data[pulse][sig]['times'] = _t
                                self.config.data[pulse][sig]['values'] = _y
                            

    def update_plot(self, pulses: list=None):
        # For all pulses and selected signals, plot associated y(t)
        if pulses:
            # clear graph
            self.graphWidget.clear()
            
            for pulse in pulses:
                for sig in self.config.selected_signals:
                    data = self.config.data[pulse][sig]
                    times = data['times']
                    values = data['values']
                    self.graph.plot(times, values)
                
                

    def _create_right_side(self):
        'GUI: Create right side (plot window)'
        self.graphWidget = pg.PlotWidget()       
        self.panel_right = QWidget()
        self.panel_right_layout = QVBoxLayout()
        self.panel_right_layout.addWidget(self.graphWidget)
        self.panel_right.setLayout(self.panel_right_layout)
        
        
    def _create_left_side(self):
        'GUI; Create left side (search bar and list of signals)'
        # Search bar to search and filter signals or waveform name
        self.qt_search_bar = QLineEdit()
        self.qt_search_bar.textChanged.connect(self.on_textChanged)
        # Select box for choice between standard signals or DCS settings
        self.qt_sig_type = QComboBox()
        self.qt_sig_type.addItem('PCS waveforms')
        self.qt_sig_type.addItem('signals')
        self.qt_sig_type.activated[str].connect(self._setup_signal_list)
        self.qt_widget_search = QWidget()
        self.qt_widget_search_layout = QHBoxLayout()
        self.qt_widget_search_layout.addWidget(self.qt_search_bar)
        self.qt_widget_search_layout.addWidget(self.qt_sig_type)
        self.qt_widget_search.setLayout(self.qt_widget_search_layout)

        ## Create the list of signals
        self.qt_signals_list = QListWidget()
        # select the default signal type as defined in the PanelConfiguration
        self.qt_sig_type.setCurrentText(self.config.default_signal_type)
        self._setup_signal_list(self.config.default_signal_type)
        # allows selecting multiple number of signals
        self.qt_signals_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # define right click context menu
        self.qt_signals_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.qt_signals_list.customContextMenuRequested[QtCore.QPoint].connect(self._item_context_menu_event)
        
        ## Creating the panel
        self.panel_left = QWidget()
        self.panel_left_layout = QVBoxLayout()
        
        self.panel_left_layout.addWidget(self.qt_widget_search)
        self.panel_left_layout.addWidget(self.qt_signals_list)
        self.panel_left.setLayout(self.panel_left_layout)

    @Slot(str)
    def on_textChanged(self, text):
        '''
        Hide the elements of the signals list which does not fit the search bar text
        '''
        for row in range(self.qt_signals_list.count()):
            item = self.qt_signals_list.item(row)
           
            if text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
                
    @Slot(str)
    def _setup_signal_list(self, text):
        if text == 'signals':
            self.qt_sig_list = self.sig_list
        elif text == 'PCS waveforms':
            self.qt_sig_list = self.wf_list
        
        # # Setup the search bar and completion style  
        # model = QStringListModel()
        # model.setStringList(self.qt_sig_list)
        
        # completer = QCompleter()
        # completer.setModel(model)
        # completer.setCaseSensitivity(Qt.CaseInsensitive)
        # completer.setCompletionMode(QCompleter.PopupCompletion)
        # completer.setModelSorting(QCompleter.UnsortedModel)
        # completer.setFilterMode(Qt.MatchContains)
        # self.qt_search_bar.setCompleter(completer)

        self.qt_signals_list.clear()
        self.qt_signals_list.addItems(self.qt_sig_list)        
        
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

        config : dict, optional
            ControlRoom configuration. The default is None (->default config).

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

        
        # self.left =
        # self.top =
        # self.width =
        # self.height =
        # self.setGeometry(self.left, self.top, self.width, self.height)


        # setup window size to 90% of avail. screen height
        rec = QApplication.desktop().availableGeometry()
        self.resize(MINIMUM_WIDTH, .9*rec.height())

        # Menu Bar
        self.ui_menu_bar()

        # create pulse number edit bar
        self.ui_pulses()
        # TODO : validator
        # .setValidator(QIntValidator())
                
        # create tabs. Panels are defined inside each tab
        # self.tab = TabBarPlus()
        self.qt_tabs = QTabWidget()
        
        self.qt_tabs.setTabsClosable(True)  
        self.qt_tabs.setMovable(True)
        self.qt_tabs.tabCloseRequested.connect(self.ui_close_tab)     
        # Central Widget
        self.qt_central = QWidget()
        self.qt_central_layout = QVBoxLayout()
        self.qt_central_layout.addWidget(self.qt_pulses)
        self.qt_central_layout.addWidget(self.qt_tabs)
        self.qt_central.setLayout(self.qt_central_layout)
        self.setCentralWidget(self.qt_central)
               
        # setup UI from configuration if passed, or default config otherwise
        if config:
            self.config = config
        else:
            self.config = self.default_configuration()

        # setup the GUI (pulse list, tabs and panels and selected signals)
        self.ui_setup_from_config()
        
    def ui_setup_from_config(self, clear=True):
        """
        Setup the GUI according to the configuration.
        
        Parameters
        ----------
        clear: bool, optional
            Clear all the tab of the application before creating new. Default is True.
            if False, it will append the tabs to the existing ones.
        """        
        # fill the edit text line with the configuration pulses
        self.qt_pulse_line_edit.setText(self.pulses_str())
        
        # eventually clear all the tabs
        if clear:
            self.qt_tabs.clear()
        
        # create the tab and panels
        for tab in self.config['tabs']:
            self.ui_add_tab(panel_configs=tab['panel_configs'], label=tab['label'])

        # synchronize x-axis between panels
        self.synchronize_panels()

    def synchronize_panels(self, sharex: bool=True, sharey: bool=False):
        """
        Synchronize the x-axis between panels
        
        Parameters
        ----------
        sharex: bool, optional
            Link x-axis between panels. Default is True
        
        sharey: bool, optional
            Link y-axis between panels. Default is False.
        """
        for tab_index in range(self.qt_tabs.count()):
            tab = self.qt_tabs.widget(tab_index)
            panels = tab.panels
            if panels:
                for panel in panels[1:]:
                    if sharex:
                        panel.graphWidget.setXLink(panels[0].graphWidget)
                    if sharey:
                        panel.graphWidget.setYLink(panels[0].graphWidget)
                
    
    def pulses_str(self) -> str:
        '''
        Pulse numbers string, separated by commas

        Returns
        -------
        pulses_str: str
            pulses number separated by commas. Return '' if no pulse.

        '''
        if self.config['pulses']:
            return ', '.join([str(pulse) for pulse in self.config['pulses'] ])
        else:
            return ''
        
    def ui_pulses(self):
        '''
        Pulse(s) edit bar and plot button
        '''
        self.qt_pulse_line_edit = QLineEdit()
        # Signals: update the pulse list if user edit it. If enter is pressed,
        # update all the plot
        self.qt_pulse_line_edit.editingFinished.connect(self.update_config_pulses)
        self.qt_pulse_line_edit.returnPressed.connect(self.update)
        self.qt_plot_button = QPushButton(text='Plot')
        self.qt_plot_button.clicked.connect(self.update)
        
        self.qt_pulses = QWidget()
        self.qt_pulses_layout = QHBoxLayout()
        self.qt_pulses_layout.addWidget(self.qt_pulse_line_edit)
        self.qt_pulses_layout.addWidget(self.qt_plot_button)

        self.qt_pulses.setLayout(self.qt_pulses_layout)
        
    @property
    def pulses(self) -> list:
        """
        Pulse list as entered in the edit box

        Returns
        -------
        pulses: list
            list of int or None

        """
        text = self.qt_pulse_line_edit.text()
        # split ',' -> pulses number
        if text:
            return [int(p) for p in text.split(',')]
        else:
            return None
        
    def ui_add_tab(self, panel_configs: list=None, label: str=None) -> None:
        '''
        Add a new Tab
        
        Parameters
        ----------
        panel_configs: list. optional
            list of PanelConfiguration objects. Default: default configuration

        label: str. optional
            label of the tab. Default: 'Traces #' where # is the number of tabs.
        '''
        if not panel_configs:
            panel_configs = self.default_panel_configs()
        # tab configuration. Setup default values if arguments are None
        tab_config = self.tab_config(label=label, panel_configs=panel_configs)
        # list of Panel object to be stored into the Qt Tab object
        panels = []
        # Add the panels vertically in a Splitter and create Tab
        page = QSplitter(Qt.Vertical)
        for panel_config in tab_config['panel_configs']:
            panel = Panel(config=panel_config)
            page.addWidget(panel)
            panels.append(panel)
        tab_index = self.qt_tabs.addTab(page, tab_config['label'])
        # store the panels config in the qt widget
        self.qt_tabs.widget(tab_index).panel_configs = tab_config['panel_configs']
        self.qt_tabs.widget(tab_index).panels = panels
        # focus on the new created tab
        self.qt_tabs.setCurrentWidget(page)
        
        # update the configuration
        self.update_config()

      

    def ui_rename_current_tab(self):
        ''' 
        display a dialog to rename the current tab
        '''
        current_tab_index = self.qt_tabs.currentIndex()
        new_label, ok = QInputDialog.getText(self, "New Tab Label", "Tab Label:",
                                 QLineEdit.Normal, 
                                 self.qt_tabs.tabText(current_tab_index))
        if ok:
            self.qt_tabs.setTabText(current_tab_index, new_label)
        
        # update the configuration
        self.update_config()
        
    def ui_close_current_tab(self):
        '''
        Close the current Tab
        '''
        tab_index = self.qt_tabs.currentIndex()
        print(f'user want to close {tab_index}')
        self.ui_close_tab(tab_index)

    @Slot(int)
    def ui_close_tab(self, index):
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

        # update the configuration
        self.update_config()

    @Slot(int)
    def qtabwidget_currentchanged(self, index):
        print(f"The new index of the current page: {index}")
       
           
    def ui_exit(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed 
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            QtCore.QCoreApplication.quit()
        else:
            # do nothing
            pass    
 
        
    def ui_menu_bar(self):
        """ Menu bar """
        self.menuBar = self.menuBar()

        # file menu
        menu_file = self.menuBar.addMenu('&File')
        
        action_open = QAction('&Open', self)
        action_open.triggered.connect(self.ui_open_configuration)
        menu_file.addAction(action_open)
        
        action_save = QAction('&Save', self)
        action_save.triggered.connect(self.ui_save_configuration)
        menu_file.addAction(action_save)
        
        action_save_as = QAction('Save &As', self)
        action_save_as.triggered.connect(self.ui_save_configuration_as)
        menu_file.addAction(action_save_as)
        
        menu_file.addSeparator()
        
        action_file_exit = QAction('&Exit', self)
        action_file_exit.setStatusTip('Exit')
        action_file_exit.setShortcut('Ctrl+Q')
        action_file_exit.triggered.connect(self.ui_exit)
        menu_file.addAction(action_file_exit)
        
                
        # Tabs
        menu_tabs = self.menuBar.addMenu('&Tabs')
        action_add_tab = QAction('&Add Tab', self)
        action_add_tab.triggered.connect(self.ui_add_tab)
        menu_tabs.addAction(action_add_tab)
        
        action_rename_tab = QAction('&Rename Current Tab', self)
        action_rename_tab.triggered.connect(self.ui_rename_current_tab)
        menu_tabs.addAction(action_rename_tab)
        
        action_remove_tab = QAction('&Close Current Tab', self)
        action_remove_tab.triggered.connect(self.ui_close_current_tab)
        menu_tabs.addAction(action_remove_tab)
        
        # Panels
        menu_panels = self.menuBar.addMenu('&Panels')
        action_add_panel = QAction('&Add Panel', self)
        action_add_panel.triggered.connect(self.ui_add_panel)
        menu_panels.addAction(action_add_panel)
        
        action_remove_panel = QAction('&Remove Panel', self)
        action_remove_panel.triggered.connect(self.ui_remove_panel)
        menu_panels.addAction(action_remove_panel)        
        
    def ui_add_panel(self, tab_index: int=None):
        """
        Add a panel to a specified tab 

        Parameters
        ----------
        tab_index : int, optional
            tab index. The default is None (->current tab).

        Returns
        -------
        None.

        """
        new_panel = Panel()

        if not tab_index:           
            tab_index = self.qt_tabs.currentIndex()
            
        # get the tab page (which is a QSplitter)
        # and add the new Panel() widget to it
        page = self.qt_tabs.widget(tab_index)
        page.addWidget(new_panel)
        page.panels.append(new_panel)
        
        # resynchornize panels
        self.synchronize_panels()

    
    def ui_remove_panel(self, panel_index: int=None, tab_index=None):
        """
        Remove a panel from a specified tab

        Parameters
        ----------
        panel_index : int, optional
            panel index to remove. Default is -1 (->remove the last one)

        tab_index : int, optional
            tab index. The default is None (->current tab).

        Returns
        -------
        None.

        """
        if not tab_index:           
            tab_index = self.qt_tabs.currentIndex()
            
        # get the tab page (which is a QSplitter)
        # and remove the new Panel() widget to it.
        #  Many things in Qt cannot be "traditionally" removed. Instead call hide() on it and destruct it. From QSplitter documentation:
        # When you hide() a child its space will be distributed among the other children. It will be reinstated when you show() it again.
        page = self.qt_tabs.widget(tab_index)
        if not panel_index:
            # last element
            panel_index = page.count() - 1
            removed_panel = page.panels.pop(-1)
        panel_to_remove = page.widget(panel_index)
        panel_to_remove.hide()
        removed_panel = page.panels.pop(-panel_index)
        # TODO bug with pop()
        
        
        
        
        # resynchornize panels
        self.synchronize_panels()
        
    def tab_config(self, label: str=None, panel_configs: list=None, layout=None) -> dict:
        """
        Tab configuration

        Parameters
        ----------
        label : str, optional
            Tab label. The default is None.
        panel_configs : list, optional
            list of PanelConfiguration(). The default is None.
        layout : TYPE, optional
            panel layout. The default is None.

        Returns
        -------
        tab_config: dict
            Tab configuration

        """
        # default Tab label
        if not label:
            next_tab_index = self.qt_tabs.count() + 1
            label = "Traces #%d" % next_tab_index
        # default list of Panels
        if not panel_configs:
            panel_configs = self.default_panel_configs()
            
        return {'label': label, 'panel_configs': panel_configs, 'layout': layout}
    
    def default_panel_configs(self) -> list:
        """
        Default list of PanelConfiguration objets

        Returns
        -------
        panels: list: 
            list of PanelConfiguration()

        """
        panel1_config = PanelConfiguration()
        panel1_config.default_signal_type = 'PCS waveforms'
        panel1_config.selected_signals = ['rts:WEST_PCS/Actuators/Heating/LHCD/power/1/waveform.ref']
        
        panel2_config = PanelConfiguration()
        panel2_config.default_signal_type = 'signals'
        panel2_config.selected_signals = ['Ip: Plasma current']
       
        return [panel1_config, panel2_config]
    
    def default_configuration(self) -> dict:
        """
        Return the ControlPanel default configuration
        
        Returns
        -------
        default_config: dict
            Default ControlPanel configuration dictionnary
            
        """        
        default_config = {
        'tabs': [self.tab_config()],
        'pulses': [55799],
        'config_file': None,
        }
        
        return default_config
             
    @property
    def tab_configs(self) -> list:
        """
        Current tab configurations

        Returns
        -------
        tab_configs: list
            list of dict.

        """
        tab_configs = []
        for tab_index in range(self.qt_tabs.count()):
            tab = self.qt_tabs.widget(tab_index)
            tab_config = self.tab_config(label=self.qt_tabs.tabText(tab_index), 
                                         panel_configs=tab.panel_configs)
            tab_configs.append(tab_config)
        return tab_configs
    
    def update_config(self):
        """
        Update the internal configuration from all the elements of the UI

        Returns
        -------
        None.

        """
        # update pulse list config
        self.update_config_pulses()
        # update 
        self.config['tabs'] = self.tab_configs
        
        print('Update configuration:', self.config)

    def update_config_pulses(self) -> None:
        '''
        Update the list of pulses from the GUI edit bar
        '''
        self.config['pulses'] = self.pulses
        
        print('Qt Line Edit Pulse list:', self.config['pulses'])

    def update(self) -> None:
        '''
        Update pulse list and plots for each panels
        '''
        print('Updating data and plots... ')
        # be sure to get the latest pulses
        self.update_config_pulses()
        # for all tabs
        west_pulses = translate_pulse_numbers(self.config['pulses'])
        
        for tab_index in range(self.qt_tabs.count()):
            tab = self.qt_tabs.widget(tab_index)
            print(f"Updating tab {self.qt_tabs.tabText(tab_index)}")
            # for all Panel() object stored into the tab
            for panel in tab.panels:
                panel.update(pulses=west_pulses)


    def export_config(self, fname: str=None):
        """
        Export the current configuration into a file

        Parameters
        ----------
        fname : str, optional
            Filename. The default is None (autosave).

        Returns
        -------
        None.

        """
        # TODO : serialize into JSON instead of pickle? 
        # Some objects like PanelConfiguration are not JSON-serializable... 
        # import json        
        # if not fname:
        #     fname = 'autosave.json'        
        # with open(fname, 'w') as outfile:
        #     json.dump(self.config, outfile)
       
        if not fname:
            fname = '.autosave.config'

        with open(fname, 'wb') as fhandler:
            pickle.dump(self.config, fhandler)

    def load_config(self, file_name) -> dict:
        """
        Load a Control Room configuration file (.config)

        Parameters
        ----------
        file_name : str
            filename (.config)

        Returns
        -------
        config: dict
            Control Room configuration dictionnary

        """
        # TODO: test validity of the file??
        with open(file_name, 'rb') as fhandler:
            config = pickle.load(fhandler)
        return config

    def ui_open_configuration(self):
        """
        Open a File Dialog to open a Control Room configuration (.config)
        """
        file_name, selected_filter = QFileDialog.getOpenFileName(self,
                                               "Open Configuration File", 
                                               "", "Config file (*.config)")
        # load the new configuration and setup the GUI accordingly
        self.config['config_file'] = file_name
        self.config = self.load_config(file_name)
        self.ui_setup_from_config()
       
    
    def ui_save_configuration(self):
        """
        Save the current Control Room configuration. 
        
        If not saved before, open a File Dialog to save a Control Room configuration (.config)
        """
        if not self.config['config_file']:
            self.ui_save_configuration_as()
        else:
            self.export_config(self.config['config_file'])
            
    
    def ui_save_configuration_as(self):
        """
        Open a File Dialog to save a Control Room configuration (.config)
        """
        file_name, selected_filter = QFileDialog.getSaveFileName(self,
                  "Save Configuration File", "", filter="Config file (*.config)")
        print(f'Saving configuration to {file_name}...')
        self.config['config_file'] = file_name
        self.export_config(self.config['config_file'])


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
