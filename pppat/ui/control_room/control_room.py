# -*- coding: utf-8 -*-
"""
Created on Fri May 22 09:11:36 2020

@author: JH218595
"""

import sys
import os
import numpy as np
import pickle
import pyqtgraph as pg
import matplotlib.pyplot as plt
import itertools  # to cycle the style and colors
from lxml import html  # for strip_html_tags
import qtpy.QtGui as QtGui
import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets
from qtpy.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                            QHBoxLayout, QVBoxLayout, QAction, qApp, QLabel,
                            QScrollArea, QTextBrowser, QFrame, QTextEdit, QLineEdit,
                            QFileDialog, QInputDialog, QStatusBar, QProgressBar, 
                            QPlainTextEdit, QTableWidgetItem, QToolButton, QStyle,
                            QMessageBox, QComboBox, QCompleter, QListWidget,
                            QSplitter, QStyleFactory, QTabWidget, QTabBar)
from qtpy.QtGui import QIcon, QCursor, QDesktopServices
from qtpy.QtCore import QDir, Slot, Signal, Qt, QUrl, QStringListModel, QSize

from pppat.ui.collapsible_toolbox import QCollapsibleToolbox
from pppat.ui.control_room.signals import signals, get_sig, add_arcad_signals
from pppat.libpulse.utils import wait_cursor, nested_dict
from pppat.libpulse.pulse_settings import PulseSettings
from pppat.libpulse.utils_west import last_pulse_nb
from pppat.libpulse.waveform import get_waveform



# default color cycle : create a list of RGBA tuples from matplotlib colormap
cmap = plt.get_cmap("tab10")  # colormap from matplotlib
DEFAULT_COLORS = np.array(cmap(range(10)))*255  # normalized to 255 for pyqtgraph
            
# windows min width
MINIMUM_WIDTH = 800

# Default Paths
real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
WAVEFORMS_LIST = dir_path + '/waveform_names.txt'

# setup Graphical stuffs
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)
# Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


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
    for sig in add_arcad_signals(signals):
        # do not keep signals marked as display=False
        if signals[sig].get('options', {}).get('display', True):
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
        with open(WAVEFORMS_LIST) as file:
            data = file.read()

        return data.splitlines()





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
        control_room_config : PanelConfiguration
            Control room Panel Configuration

        Returns
        -------
        None.

        """
        self.signal_type = 'signals' # or  'PCS waveforms'
        self.selected_signals = []
        self.backend = 'pyqtgraph'  # currently not used
        # numerical data stored
        self.data = nested_dict()
        # widths of the left and right regions wrt central separator
        self.sizes = [70, 200]
        # color-cycle wrt pulses (True) or signal type (False)
        self.color_wrt_pulses = True
        # show the legend in panel plots?
        self.display_legend = True
        # show the cross-hair?
        self.display_crosshair = False

class Panel(QSplitter):
    def __init__(self, parent=None, config: PanelConfiguration=None):
        """
        Panel

        A Panel is a QSplitter GUI which contains a search bar at left and a plot at right

        """
        QSplitter.__init__(self, Qt.Horizontal, parent=parent)
        self.parent = parent
        
        # Panel configuration
        self.config = config or PanelConfiguration()

        # list of all the signals to display
        self.sig_list = list_signals()
        self.wf_list  = list_waveforms()

        # GUI Creation
        self.ui_create_left_side()
        self.ui_create_right_side()

        # create a vertical splitter with signal list at left and plot at right
        # self.splitter_vert = QSplitter(Qt.Horizontal)
        self.addWidget(self.panel_left)
        self.addWidget(self.panel_right)

        # Allows the vertical splitter to collapse
        self.setCollapsible(0, True)

        # set configuration
        self.ui_update_selected_signals()

    # Getter and setter of Panel properties
    @property
    def signals(self):
        return self._signals

    @signals.setter
    def signals(self, siglist):
        self._signals = siglist

    def update_plot(self, pulses: list=None):
        """
        Update panel plot for the given list of pulses.
        
        The list of signals is stored in the panel configuration.

        Parameters
        ----------
        pulses : list, optional
            WEST pulse list. The default is None.

        """           
        # For all pulses and selected signals, plot associated y(t)
        if pulses:
            # clear graph
            self.graphWidget.clear()
            # cycling automatically on linestyles
            qt_line_styles = [QtCore.Qt.SolidLine, 
                                              QtCore.Qt.DashLine, 
                                              QtCore.Qt.DotLine, 
                                              QtCore.Qt.DashDotLine, 
                                              QtCore.Qt.DashDotDotLine]
            line_styles = itertools.cycle(qt_line_styles)

            # when mouse is mouved
            self.p.scene().sigMouseMoved.connect(self.ui_plot_mouse_moved)               

            if getattr(self.config, 'display_legend', True):
                self.graphWidget.addLegend()  # addLegend() must be called BEFORE plot()
                
            units, titles = [], []
            for idx_pulse, pulse in enumerate(pulses):
                for idx_sig, (sig, line_style) in enumerate(zip(self.config.selected_signals, line_styles)):
                    
                    # colored_pulse = True
                    # - each pulse has a specific color
                    # - all signal have same linestyle
                    # if False, vice-versa        
                    if getattr(self.config, 'color_wrt_pulses', True):
                        cur_pen = pg.mkPen(color=pg.mkColor(DEFAULT_COLORS[idx_pulse]), # was pg.intColor(idx_pulse)
                                            style=qt_line_styles[0], width=2)
                    else:
                        cur_pen = pg.mkPen(color=pg.mkColor(DEFAULT_COLORS[idx_sig]), 
                                            style=line_style, width=2)

                    # retrieve data from the parent model
                    values, times = self.parent.model.data( (pulse, sig), None)
                    
                  
                    # TODO : probably better to use setData on defined PlotCurveItem ?
                        
                    # plot values only if they are both arrays
                    if (np.array(times).size > 1) and (np.array(values).size > 1):
                        name=f'{pulse}:{self.shorten_name(sig)}' 
                        self.graphWidget.plot(times, values, 
                                          name=name, 
                                          pen=cur_pen)
                        # append signal labels and units 
                        units.append(self.parent.model.signal_unit(sig))
                        titles.append(self.parent.model.signal_label(sig))
                    else:
                        print('Bad data!!!!')

                # update the unit and titles if necessary
                self.graphWidget.setLabels(left=', '.join(filter(None, units)))
                
                if self.parent.action_title.isChecked():
                    self.graphWidget.setTitle(', '.join(filter(None, titles)))
                else:
                    self.graphWidget.setTitle(None)
                

        
    def shorten_name(self, sig_name: str) -> str:
        """
        Create a shorter while meaningfull signal name, for plot legends

        Parameters
        ----------
        sig_name : str
            full signal name.

        Returns
        -------
        sig_name : str
            shorter signal name.

        """
        if sig_name.startswith('rts:'):
            sig_name = 'PCS:'+'/'.join(sig_name.split('/')[1:-1])
        else:
            sig_name = sig_name.split(':')[1]
        return sig_name

    def ui_create_right_side(self):
        'GUI: Create right side (plot window)'
        self.graphWidget = pg.PlotWidget()
        self.p = self.graphWidget.getPlotItem()
        
        self.vb = self.p.vb
        # cross-hair display
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
       
        self.panel_right = QWidget()
        self.panel_right_layout = QVBoxLayout()
        self.panel_right_layout.addWidget(self.graphWidget)
        self.panel_right.setLayout(self.panel_right_layout)

    def ui_plot_mouse_moved(self, event):
        """
        Slot for mouve moved over a PlotWidget() of a Panel
        """
        # The signal sigMouseMoved returns the coordinates in pixels 
        # with respect to the PlotWidget, not in the coordinates of the plot, 
        # so a conversion must be done using the mapSceneToView method 
        plot_pos = self.p.vb.mapSceneToView(event)
        
        # display the current mouse position on the status bar in the plot coordinates
        self.parent.qt_plot_position_label.setText(f'x={plot_pos.x():.2f}, y={plot_pos.y():.2f}')
        
        # plot cross hair if requested
        if getattr(self.config, 'display_crosshair', False):
            self.p.addItem(self.vLine, ignoreBounds=True)
            self.p.addItem(self.hLine, ignoreBounds=True)
            # update vertical lines on all plots
            self.p.scene().sigMouseMoved.connect(self.parent.ui_plot_mouse_moved_panels)
            # update horizontal line on current plot only       
            if self.p.sceneBoundingRect().contains(event):
                # index = int(mousePoint.x())
                # if index > 0 and index < len(data1):
                #     label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
                # self.vLine.setPos(mousePoint.x())
                self.hLine.setPos(plot_pos.y())

    def ui_create_left_side(self):
        'GUI; Create left side (search bar and list of signals)'
        # Search bar to search and filter signals or waveform name
        self.qt_search_bar = QLineEdit()
        self.qt_search_bar.textChanged.connect(self.ui_on_textChanged)
        # Select box for choice between standard signals or DCS settings
        self.qt_sig_type = QComboBox()
        self.qt_sig_type.addItem('PCS waveforms')
        self.qt_sig_type.addItem('signals')
        self.qt_sig_type.activated[str].connect(self.ui_setup_signal_list)
        self.qt_widget_search = QWidget()
        self.qt_widget_search_layout = QHBoxLayout()
        self.qt_widget_search_layout.addWidget(self.qt_search_bar)
        self.qt_widget_search_layout.addWidget(self.qt_sig_type)
        self.qt_widget_search.setLayout(self.qt_widget_search_layout)

        # move up/down the panel
        self.qt_move_down = QPushButton(icon=self.style().standardIcon(getattr(QStyle, 'SP_ArrowDown')), parent=self)
        self.qt_move_up = QPushButton(icon=self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')), parent=self)
        self.qt_widget_search_layout.addWidget(self.qt_move_down)
        self.qt_widget_search_layout.addWidget(self.qt_move_up)    

        ## Create the list of signals
        self.qt_signals_list = QListWidget()
        # select the default signal type as defined in the PanelConfiguration
        self.qt_sig_type.setCurrentText(self.config.signal_type)
        self.ui_setup_signal_list(self.config.signal_type)
        # allows selecting multiple number of signals
        self.qt_signals_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # define right click context menu
        self.qt_signals_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.qt_signals_list.customContextMenuRequested[QtCore.QPoint].connect(self.ui_item_context_menu_event)
        # double clik switches the selection (add/remove)
        self.qt_signals_list.itemDoubleClicked.connect(self.ui_item_switch_state)
        # change default selection color
        self.qt_signals_list.setStyleSheet("selection-background-color: gray")
        
    
        ## Creating the panel
        self.panel_left = QWidget()
        self.panel_left_layout = QVBoxLayout()

        self.panel_left_layout.addWidget(self.qt_widget_search)
        self.panel_left_layout.addWidget(self.qt_signals_list)

        self.panel_left.setLayout(self.panel_left_layout)

    @Slot(str)
    def ui_on_textChanged(self, text):
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
    def ui_setup_signal_list(self, kind: str):
        """
        Display the signal list according to the kind of list

        Parameters
        ----------
        kind : str
            Kind of signal to display in the list: 'signals' or 'PCS waveforms'

        """
        if kind == 'signals':
            self.qt_sig_list = self.sig_list
        elif kind == 'PCS waveforms':
            self.qt_sig_list = self.wf_list
        else:
            raise ValueError('Incorrect signal kind: should be "signals" or "PCS waveforms"')
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
        # color the selected signals
        self.ui_update_selected_signals()

    def ui_item_context_menu_event(self, event):
        'GUI: signal list context menu'
        right_menu = QtWidgets.QMenu(self.qt_signals_list)
        action_add = QtWidgets.QAction("Add", self, triggered=self.ui_add_selected_signals)
        action_rem = QtWidgets.QAction("Remove", self, triggered=self.ui_remove_selected_signals)
        right_menu.addAction(action_add)
        right_menu.addAction(action_rem)
        right_menu.exec_(QtGui.QCursor.pos())

    def ui_update_selected_signals(self):
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

    @property
    def ui_selected_signals(self):
        '''
        List of selected signal names

        Returns
        -------
        selected_signals: list
            list of selected signal names

        '''
        selected_signals = [item.text() for item in self.qt_signals_list.selectedItems()]
        return selected_signals
    
    def ui_item_switch_state(self, event):
        '''
        Switch the signal state from not selected to selected or vice-versa
        '''
        for sig in self.ui_selected_signals:
            if sig:
                # signal already selected -> unselect it
                # and vice-versa
                if sig in self.config.selected_signals:
                    self.config.selected_signals.remove(sig)
                else:
                    self.config.selected_signals.append(sig)
        # update selected signals list
        self.ui_update_selected_signals()
        
    def ui_add_selected_signals(self, event):
        '''
        Add a list signals to the list of signals to be plotted
        '''
        for sig in self.ui_selected_signals:
            if sig:
                # add the signals to the list of signals to be plotted
                self.config.selected_signals.append(sig)

        print('selected signals are now:', self.config.selected_signals)
        # update selected signals list
        self.ui_update_selected_signals()


    def ui_remove_selected_signals(self, event):
        '''
        Remove a list of signal of the list of signals to be plotted
        '''
        for sig in self.ui_selected_signals:
            if sig in self.config.selected_signals:
                # remove the signame from the list of signals to be plotted
                self.config.selected_signals.remove(sig)

        print('selected signals are now:', self.config.selected_signals)
        # update selected signals list
        self.ui_update_selected_signals()


class DataViewer(QMainWindow):
    def __init__(self, parent=None):
        super(DataViewer, self).__init__(parent)
        
        self.qt_tree = QtWidgets.QTreeView()
        
        self.qt_tree.setModel(ControlRoomDataModel())
        self.setWindowTitle('Control Room Data Viewer [WEST]')
        
        self.central_widget_layout = QVBoxLayout()
        self.central_widget_layout.addWidget(self.qt_tree)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_widget_layout)
        self.setCentralWidget(self.central_widget)

    def columnCount(self):
        pass
    
    def rowCount(self):
        pass
    def flags(self):
        pass
    def data(self):
        pass
    def headerData(self):
        pass

class ControlRoom(QMainWindow):
    """
    Central GUI class which also serves as main Controller
    """
    def __init__(self, parent=None, config_file: str=None):
        """
        Control Room Application

        Parameters
        ----------
        parent : TYPE, optional
            DESCRIPTION. The default is None.

        config_file : str, optional
            ControlRoom configuration file. The default is None (->default config).

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

        self.model = ControlRoomDataModel()
        
        # self.left =
        # self.top =
        # self.width =
        # self.height =
        # self.setGeometry(self.left, self.top, self.width, self.height)


        # setup window size to 90% of avail. screen height
        rec = QApplication.desktop().availableGeometry()
        self.resize(MINIMUM_WIDTH, .9*rec.height())

        ###################### Menu Bar
        self.ui_menu_bar()

        ###################### create pulse number edit bar
        self.ui_pulses()
        # TODO : make a validator
        # .setValidator(QIntValidator())

        ###################### tabs
        # create tabs. Panels are defined inside each tab
        # self.tab = TabBarPlus()
        self.qt_tabs = QTabWidget()

        self.qt_tabs.setTabsClosable(True)
        self.qt_tabs.setMovable(True)
        self.qt_tabs.tabCloseRequested.connect(self.ui_close_tab)
        
        ###################### status bar
        self.qt_status_bar = QStatusBar()
        self.setStatusBar(self.qt_status_bar)        
        # progress bar
        self.qt_progress_bar = QProgressBar(self.qt_status_bar)
        self.qt_progress_bar.setMinimumWidth(300)
        
        # mouse position indicator
        self.qt_plot_position_label = QLabel(self.qt_status_bar)
        self.qt_plot_position_label.setMinimumWidth(100)
        
        # dummy spacer to align one stuff at the left and the other at the right 
        # (is there better way??)
        spacer = QLabel()        
        self.qt_status_bar.addPermanentWidget(self.qt_progress_bar)
        self.qt_status_bar.addPermanentWidget(spacer, 1)
        self.qt_status_bar.addPermanentWidget(self.qt_plot_position_label)
        
        ###################### Data Viewer (separate windows)
        self.qt_data_viewer = DataViewer()
        
        ###################### Central Widget
        self.qt_central = QWidget()
        self.qt_central_layout = QVBoxLayout()
        self.qt_central_layout.addWidget(self.qt_pulses)
        self.qt_central_layout.addWidget(self.qt_tabs)
        self.qt_central.setLayout(self.qt_central_layout)
        self.setCentralWidget(self.qt_central)

        # setup UI from configuration if passed, or default config otherwise
        if config_file:
            self.config = self.load_config(config_file)
        else:
            self.config =  self.default_configuration()

        # setup the GUI (pulse list, tabs and panels and selected signals)
        self.ui_setup_from_config()

    def ui_plot_mouse_moved_panels(self, event):
        """
        Slot called uo update *all* PlotWidget() (all Panel) of the current Tab
        """
        # NB : the points values are passed to the statusbar
        # the callback is defined in the panel ui_plot_mouse_moved method
        
        # update the vertical lines on all plots (time)      
        cur_tab = self.tabs[self.current_selected_tab_index]
        for panel in cur_tab.panels:
            if panel.p.sceneBoundingRect().contains(event):
                mousePoint = panel.vb.mapSceneToView(event)
                panel.vLine.setPos(mousePoint.x())

    def ui_synchronize_panels(self, sharex: bool=True, sharey: bool=False):
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

##################################################
#
#               GUI stuffs
#
##################################################

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

    def ui_format_pulse_line_edit(self, pulses_str: str):
        """
        Format the pulse edit (colors, etc)

        Parameters
        ----------
        pulses_str : str
            pulse edit line string

        """
        # format the qt_pulse_line_edit
        self.qt_pulse_line_edit.setStyleSheet("QLineEdit"
                        "{"
                        "color : black;"
                        "}")


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
        # if not passed uses default panel configuration
        panel_configs = panel_configs or self.panel_configs_default()
        # tab configuration. Setup default values if arguments are None
        tab_config = self.tab_config(label=label, panel_configs=panel_configs)
        # list of Panel object to be stored into the Qt Tab object
        panels = []
        # Add the panels vertically in a Splitter and create Tab
        page = QSplitter(Qt.Vertical)
        for panel_config in tab_config['panel_configs']:
            panel = Panel(config=panel_config, parent=self)
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
        
        # synchronize x-axis between panels
        self.ui_synchronize_panels()

    def ui_rename_current_tab(self):
        '''
        display a dialog to rename the current tab
        '''
        new_label, ok = QInputDialog.getText(self, "New Tab Label", "Tab Label:",
                                 QLineEdit.Normal,
                                 self.qt_tabs.tabText(self.current_selected_tab_index))
        if ok:
            self.qt_tabs.setTabText(self.current_selected_tab_index, new_label)

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
    def ui_qtabwidget_currentchanged(self, index):
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

        action_open = QAction('&Open Configuration', self)
        action_open.triggered.connect(self.ui_open_configuration)
        menu_file.addAction(action_open)

        action_save = QAction('&Save Configuration', self)
        action_save.triggered.connect(self.ui_save_configuration)
        menu_file.addAction(action_save)

        action_save_as = QAction('Save Configuration &As', self)
        action_save_as.triggered.connect(self.ui_save_configuration_as)
        menu_file.addAction(action_save_as)

        menu_file.addSeparator()
        
        action_clean_data = QAction('Clean All Downloaded Data', self)
        action_clean_data.triggered.connect(self.ui_clean_data)
        menu_file.addAction(action_clean_data)

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

        action_remove_panel = QAction('&Remove Last Panel', self)
        action_remove_panel.triggered.connect(self.ui_remove_panel)
        menu_panels.addAction(action_remove_panel)

        menu_panels.addSeparator()

        action_hide_search_bars = QAction('&Hide All Search Bars', self)
        action_hide_search_bars.triggered.connect(self.ui_hide_panels_search_bars)
        menu_panels.addAction(action_hide_search_bars)

        action_show_search_bars = QAction('&Show All Search Bars', self)
        action_show_search_bars.triggered.connect(self.ui_show_panels_search_bars)
        menu_panels.addAction(action_show_search_bars)
        
        # Configuration
        menu_config = self.menuBar.addMenu('&Configuration')
        
        self.action_switch_plot_style = QAction('&Cycle colors with pulse numbers', self)
        self.action_switch_plot_style.setCheckable(True)
        self.action_switch_plot_style.setChecked(True)
        self.action_switch_plot_style.triggered.connect(self.ui_switch_plot_color_cycle_style)
        menu_config.addAction(self.action_switch_plot_style)
 
        self.action_legends = QAction('&Legends', self)
        self.action_legends.setCheckable(True)
        self.action_legends.setChecked(True)
        self.action_legends.triggered.connect(self.ui_legends)
        menu_config.addAction(self.action_legends)

        self.action_crosshair = QAction('Crosshair', self)
        self.action_crosshair.setCheckable(True)
        self.action_crosshair.setChecked(False)
        self.action_crosshair.triggered.connect(self.ui_crosshair)
        menu_config.addAction(self.action_crosshair)
        
        self.action_handle = QAction('&Handles', self)
        self.action_handle.setCheckable(True)
        self.action_handle.setChecked(True)
        self.action_handle.triggered.connect(self.ui_handles)
        menu_config.addAction(self.action_handle)

        self.action_title = QAction('&Titles', self)
        self.action_title.setCheckable(True)
        self.action_title.setChecked(True)
        self.action_title.triggered.connect(self.ui_titles)
        menu_config.addAction(self.action_title)
        
        menu_config.addSeparator()
        
        self.action_view_data = QAction('Data Viewer', self)
        self.action_view_data.setCheckable(True)
        self.action_view_data.setChecked(False)
        self.action_view_data.triggered.connect(self.ui_data_viewer)
        menu_config.addAction(self.action_view_data)
 
    def ui_handles(self):
        """
        Toggle Splitter Handles
        
        TODO: dosesn't work well yet. Should I subclass the QSplitterHandle?
        """
        state = self.action_handle.isChecked()
        if state:
            for tab in self.tabs:
                tab.setHandleWidth(QSplitter().handleWidth())
        else:
             for tab in self.tabs:
                tab.setHandleWidth(0)


    def ui_titles(self):
        """
        Toggle Titles in plotWidgets
        """
        # update drawings
        self.update()
                

    def ui_clean_data(self):
        """
        Clear all downloaded data
        """
        self.model.clean()
 
    def ui_crosshair(self):
        """
        Toggle crosshair in panel plots
        """
        state = self.action_crosshair.isChecked()
        # copy this value to all panels
        for tab in self.tabs:
            for panel in tab.panels:
                panel.config.display_crosshair = state
        # update plots
        self.update_plots()        
 
    def ui_data_viewer(self):
        """
        Open the data viewer window
        """
        state = self.action_view_data.isChecked()
        if state:
            self.qt_data_viewer.show()
        else:
            self.qt_data_viewer.hide()
            
    
    def ui_switch_plot_color_cycle_style(self):
        """
        Switch the plot color cycle style to either:
                - color cycle with pulse numbers
                - color cycle with signal types
        """
        state = self.action_switch_plot_style.isChecked()
        # copy this value to all panels
        for tab in self.tabs:
            for panel in tab.panels:
                panel.config.color_wrt_pulses = state
        # update plots
        self.update_plots()

    def ui_legends(self):
        """
        Turn on/off legends in panel plots
        """
        state = self.action_legends.isChecked()
        # copy this values to all panels
        for tab in self.tabs:
            for panel in tab.panels:
                panel.config.display_legend = state

    def ui_hide_panels_search_bars(self):
        """
        Hide all panel search bars (move separator to the extreme left)
        """
        for idx_tab in range(self.qt_tabs.count()):
            tab = self.qt_tabs.widget(idx_tab)
            for panel in tab.panels:
                panel.setSizes([0,100])

    def ui_show_panels_search_bars(self):
        """
        Show all panel search bars (move separator to the default location)
        """
        for idx_tab in range(self.qt_tabs.count()):
            tab = self.qt_tabs.widget(idx_tab)
            for panel in tab.panels:
                panel.setSizes([70,400])


    def ui_add_panel(self, tab_index: int=None, panel=None):
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
        # use the passed one or the default panel
        new_panel = panel or Panel(parent=self)

        tab_index = tab_index or self.qt_tabs.currentIndex()

        # get the tab page (which is a QSplitter)
        # and add the new Panel() widget to it
        page = self.qt_tabs.widget(tab_index)
        page.addWidget(new_panel)
        page.panels.append(new_panel)
        # update the tab's panels configuration
        page.panel_configs.append(new_panel.config)
        
        # resynchornize panels
        self.ui_synchronize_panels()
        print(page.panel_configs)


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
        tab_index = tab_index or self.qt_tabs.currentIndex()

        # get the tab page (which is a QSplitter)
        # and remove the new Panel() widget to it.
        #  Many things in Qt cannot be "traditionally" removed. Instead call hide() on it and destruct it. From QSplitter documentation:
        # When you hide() a child its space will be distributed among the other children. It will be reinstated when you show() it again.
        page = self.qt_tabs.widget(tab_index)
        if not panel_index:
            # last element
            panel_index = page.count() - 1
            # removed_panel = page.panels.pop()
        panel_to_remove = page.widget(panel_index)
        panel_to_remove.hide()
        panel_to_remove.deleteLater()
        removed_panel = page.panels.pop(panel_index)
        
        # update the tab's panels configuration
        page.panel_configs.pop(panel_index)
        # resynchornize panels
        
        self.ui_synchronize_panels()
        print(page.panel_configs)


    def ui_open_configuration(self):
        """
        Open a File Dialog to open a Control Room configuration (.config)
        """
        file_name, selected_filter = QFileDialog.getOpenFileName(self,
                                               "Open Configuration File",
                                               "", "Config file (*.config)")
        try:
            # load the new configuration and setup the GUI accordingly
            self.config['config_file'] = file_name
            self.config = self.load_config(file_name)
            self.ui_setup_from_config()
        except IOError as e:
            print(e)


    def ui_save_configuration(self):
        """
        Save the current Control Room configuration.

        If not saved before, open a File Dialog to save a Control Room configuration (.config)
        """
        if not self.config['config_file']:
            self.ui_save_configuration_as()
        else:
            # try if the file path exists first. If not, open a saveas instead
            if os.path.exists(self.config['config_file']):
                self.export_config(self.config['config_file'])
            else:
                self.ui_save_configuration_as()


    def ui_save_configuration_as(self):
        """
        Open a File Dialog to save a Control Room configuration (.config)
        """
        fdialog = QFileDialog()
        fdialog.setWindowTitle("Save Configuration to a File")
        fdialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        fdialog.setNameFilter('Configuration files (*.config)')
        fdialog.setDefaultSuffix('config')
        
        if fdialog.exec_() == QtGui.QFileDialog.Accepted:
            file_name = fdialog.selectedFiles()[0]

            print(f'Saving configuration to {file_name}...')
            self.config['config_file'] = file_name
            self.export_config(self.config['config_file'])

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
        # format the string (add colors etc)
        self.ui_format_pulse_line_edit(self.pulses_str())

        # eventually clear all the tabs
        if clear:
            self.qt_tabs.clear()

        # create the tab and panels
        for tab in self.config['tabs']:
            self.ui_add_tab(panel_configs=tab['panel_configs'], label=tab['label'])

        # resize panel (width wrt central separator)
        for idx_tab, tab in enumerate(self.tabs):
            for panel_config, panel in zip(self.panel_configs(idx_tab), self.panels(idx_tab)):
                panel.setSizes(panel_config.sizes)

        # synchronize x-axis between panels
        self.ui_synchronize_panels()

##################################################
#
#               Configuration Stuffs
#
##################################################

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
            print(f'Configuration loaded: {config}')
        return config



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





##################################################
#
#               Tab stuffs
#
##################################################

    @property
    def tab_configs(self) -> list:
        """
        Tab configurations

        Returns
        -------
        tab_configs: list
            list of dict. Each dict contains the configuration of a Tab.

        """
        tab_configs = []
        for tab_index, tab in enumerate(self.tabs):
            tab_config = self.tab_config(label=self.qt_tabs.tabText(tab_index),
                                         panel_configs=tab.panel_configs)
            tab_configs.append(tab_config)
        return tab_configs

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
        # default list of Panels if not provided
        panel_configs = panel_configs or self.panel_configs_default()

        return {'label': label,
                'panel_configs': panel_configs,
                'layout': layout}

    @property
    def tabs(self) -> list:
        """
        List of tab widgets (aka "page") .
        """
        tabs = []
        for idx_tab in range(self.qt_tabs.count()):
            tabs.append(self.qt_tabs.widget(idx_tab))
        return tabs
    
    @property
    def current_selected_tab_index(self) -> int:
        """
        Index of the tab currently selected in the GUI.

        Returns
        -------
        current_tab_index: int
            Selected tab index
        """
        return self.qt_tabs.currentIndex()
        
##################################################
#
#               panel stuffs
#
##################################################

    def panel_configs_default(self) -> list:
        """
        Default list of PanelConfiguration objets

        Returns
        -------
        panels: list:
            list of PanelConfiguration()

        """
        panel1_config = PanelConfiguration()
        panel1_config.signal_type = 'signals' # or 'PCS waveforms'
        panel1_config.selected_signals = []
        return [panel1_config]
        # panel2_config = PanelConfiguration()
        # panel2_config.signal_type = 'signals'
        # panel2_config.selected_signals = ['']

        # return [panel1_config, panel2_config]

    def panels(self, tab_index: int=None) -> list:
        """
        List of Panel() objects in a given tab

        Parameters
        ----------
        tab_index: int, optional
            index of the tab to retriveve panels from. Default is None (current selected tab)

        Returns
        -------
        panels: list
            List of Panel() objects contained in the tab.

        """
        if not tab_index:
            tab_index = self.current_selected_tab_index

        page = self.qt_tabs.widget(tab_index)
        return page.panels

    def panel_configs(self, tab_index: int=None) -> list:
        """
        List of PanelConfiguration() objects for a given tab

        Parameters
        ----------
        tab_index: int, optional
            index of the tab to retriveve panel configs from. Default is None (current selected tab)

        Returns
        -------
        panels: list
            List of PanelConfiguration() objects contained in the tab.

        """
        if not tab_index:
            tab_index = self.current_selected_tab_index

        page = self.qt_tabs.widget(tab_index)
        return page.panel_configs

    def update_config(self):
        """
        Update the internal configuration from all the elements of the UI

        Returns
        -------
        None.

        """
        # update pulse list config
        self.update_config_pulses()
        # update tab configurations
        self.config['tabs'] = self.tab_configs

        # get Splitter sizes
        panel_sizes = []
        for idx_tab, tab in enumerate(self.tabs):
            for (panel_config, panel) in zip(self.panel_configs(idx_tab), self.panels(idx_tab)):
                panel_sizes.append(panel.sizes())
        self.config['panel_sizes'] = panel_sizes

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
        west_pulses = translate_pulse_numbers(self.config['pulses'])
        
        # determine the number of signal to update
        plot_numbers = 0
        for tab in self.tabs:
            for panel in tab.panels:
                for pulse in west_pulses:
                    for signal in panel.config.selected_signals:
                        plot_numbers += 1
        
        # update data (if needed)
        counter = 0
        with wait_cursor():
            for tab in self.tabs:
                for panel in tab.panels:
                    for pulse in west_pulses:
                        for signal in panel.config.selected_signals:
                            print(f'Updating {signal} for {pulse}')
                            self.model.update_data(pulse, signal)
                            counter += 1
                            self.qt_progress_bar.setValue(counter/plot_numbers*100)
        
        # once done reset the progress bar
        self.qt_progress_bar.reset()

        # then update plots
        self.update_plots()
        
    def update_plots(self):
        """
        Update all panel plots (for all pulses and selected signals)
        """
        for tab in self.tabs:
            for panel in tab.panels:
                panel.update_plot(self.config['pulses'])

    def strip_html_tags(self, html: str) -> str:
        """
        Strip html tags to a string

        Parameters
        ----------
        html : str
            string with html tags 

        Returns
        -------
        str : cleaned_string
            string without html tags

        """
        return html.fromstring(self.qt_pulse_line_edit.text()).text_content().strip()

                        
class ControlRoomDataModel(QtGui.QStandardItemModel):
    """
    Control Room Data Model
    
    Store the data retrieved and present them to the GUI.
    """
    def __init__(self, *args, **kwargs):
        super(ControlRoomDataModel, self).__init__(*args, **kwargs)
        self._data = nested_dict()
    
    def data(self, index, role):
        """
        return y(t) for a signals at a given pulse. 
    
        Data are stored in this model and downloaded if not available. 

        Parameters
        ----------
        index : tuple (pulse: int, signal: str)
            WEST pulse number and signal name.
        role:

        Returns
        -------
        y: array
            magnitude
        t: array
            time vector
        """
        pulse, signal = index
        
        # if the data do not exist yet, download it
        if not self._data[pulse][signal]:
            # self.update_data(pulse, signal)
            return np.NaN, np.NaN
        # 
        return self._data[pulse][signal]['values'], self._data[pulse][signal]['times']

    def signal_label(self, signal) -> str:
        """
        Return the signal label of a given signal

        Parameters
        ----------
        signal : str
            signal name.

        Returns
        -------
        label : str
            signal label

        """
        if not self._data[signal]:
            return 'Not found'
        else:
            return self._data[signal]['label']

    def signal_unit(self, signal) -> str:
        """
        Return the signal unit of a given signal

        Parameters
        ----------
        signal : str
            signal name.

        Returns
        -------
        label : str
            signal unit

        """
        if not self._data[signal]:
            return 'Not found'
        else:
            return self._data[signal]['unit']
        
    def update_data(self, pulse, signal):
        print(f'Updating data for pulses {pulse}')
        if not self._data[pulse]['PulseSetting']:
            self._data[pulse]['PulseSetting'] = PulseSettings(pulse)
            
        if self._data[pulse][signal]:
            print(f'{signal} for #{pulse} already downloaded. Skipping...')
        else:
            print(f'Retrieve {signal} for #{pulse}...')
            if signal.startswith('rts:'):
                wf = get_waveform(signal, self._data[pulse]['PulseSetting'].waveforms)
                # remove 40 seconds to match pulses
                self._data[pulse][signal]['times'] = wf.times - 40
                self._data[pulse][signal]['values'] = wf.values
                self._data[signal]['label'] = wf.name
                self._data[signal]['unit'] = '' # units are not passed in XML file...
            else:
                print(signal)
                signame = signal.split(':')[0]
                _y, _t = get_sig(pulse, signals[signame])
                self._data[pulse][signal]['times'] = _t
                self._data[pulse][signal]['values'] = _y
                self._data[signal]['label'] = signals[signame]['label']
                self._data[signal]['unit'] = signals[signame]['unit']                


    def clean(self):
        """
        Clean all data stored.
        """
        self._data = nested_dict()

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
