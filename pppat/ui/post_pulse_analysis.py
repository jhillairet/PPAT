# -*- coding: utf-8 -*-
"""
PPPAT - Post pulse analysis ui
"""
from qtpy.QtWidgets import (QWidget, QGridLayout, QRadioButton, QGroupBox,
                            QVBoxLayout, QTextBrowser, QLabel, QPushButton,
                            QFormLayout, QLineEdit, QFileDialog, QCheckBox,
                            QErrorMessage, QTableView, QAbstractItemView,
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QButtonGroup)
from qtpy.QtGui import QIntValidator, QFont
from qtpy.QtCore import Slot, Qt
import os
import logging
logger = logging.getLogger(__name__)

# Smaller font sizes on windows than on Linux for a better UI experience
if os.name == 'nt':  
    TABLE_HEADER_FONT_SIZE = 10
    TABLE_ROW_FONT_SIZE = 8
else:
    TABLE_HEADER_FONT_SIZE = 12
    TABLE_ROW_FONT_SIZE = 12
TABLE_ROW_SIZE = 24  # vertical height

class PostPulseAnalysisWidget(QWidget):
    """
    Pre-pulse Analysis GUI

    Create all the widgets in the Post-pulse analysis panel.
    
    At the difference of the pre pulse analysis, here the table of test is 
    setup from the startup of the application. 
    
    The list of post tests comes from the post-pulse
    """
    def __init__(self, parent=None):
        super(PostPulseAnalysisWidget, self).__init__(parent=parent)

        # construct the GUI 
        grid = QGridLayout()
        grid.setColumnStretch(1, 2) # more space for pulse informations
        grid.addWidget(self._create_top_left_group(), 0, 0)
        grid.addWidget(self._create_top_right_group(), 0, 1)
        grid.addWidget(self._create_bottom_group(), 1, 0, 1, 2)
        self.setLayout(grid)

    def _create_top_left_group(self):
        """
        Top Left widgets group
        """
        top_left_group = QGroupBox("Pulse selection:")
        
        self.radio_last_pulse = QRadioButton('Last pulse')
        self.radio_last_pulse.setChecked(True)
        self.radio_pulse_nb = QRadioButton('Pulse number')
        # put all the radio button into a group
        self.radio_buttons_group = QButtonGroup()
        self.radio_buttons_group.addButton(self.radio_last_pulse)
        self.radio_buttons_group.addButton(self.radio_pulse_nb)
        
        self.edit_pulse_nb = QLineEdit()
        self.edit_pulse_nb.setPlaceholderText('Pulse Number')
        self.edit_pulse_nb.textChanged.connect(self._validate_radio_pulse_nb)
        self.edit_pulse_nb.setValidator(QIntValidator())  # only integer for shot#
        
        layout = QGridLayout()
        layout.addWidget(self.radio_last_pulse, 0, 0)
        layout.addWidget(self.radio_pulse_nb, 1, 0)
        layout.addWidget(self.edit_pulse_nb, 1, 1)
        top_left_group.setLayout(layout)

        return top_left_group

    @Slot()
    def _validate_radio_pulse_nb(self):
        self.radio_pulse_nb.setChecked(True)

    def _create_top_right_group(self):
        """
        Top Right widgets group
        """
        top_right_group = QGroupBox('Pulse informations')

        self.pulse_number_label = QLabel()
        self.button_check_all = QPushButton('Post pulse analysis - all')

        layout0 = QVBoxLayout()
        layout1 = QFormLayout()
        layout1.addRow(QLabel('Pulse number:'), self.pulse_number_label)
        layout0.addLayout(layout1)
        layout0.addWidget(self.button_check_all)

        top_right_group.setLayout(layout0)

        return top_right_group

    def _create_bottom_group(self):
        """
        Bottom widgets group
        """
        bottom_group = QGroupBox('Check results')
        layout = QVBoxLayout()

        self.check_table = QTableWidget(0, 4)
        self.check_table.setHorizontalHeaderLabels(['Do', 'Test Name',
                                                    'Result',  # TODO : result should be a button to click for display
                                                    'Result description'])
        # # Columns config
        # resize the column widths
        self.check_table.horizontalHeader().resizeSection(0, 15)
        self.check_table.horizontalHeader().resizeSection(1, 200)
        self.check_table.horizontalHeader().resizeSection(2, 100)
        # Strech last column to fill the remaining space
        self.check_table.horizontalHeader().setStretchLastSection(True)

        # # Rows config
        self.check_table.verticalHeader().hide()
        self.check_table.verticalHeader().setDefaultSectionSize(TABLE_ROW_SIZE)
        # font size of the header
        header_font = self.check_table.horizontalHeader().font()
        header_font.setPointSize(TABLE_HEADER_FONT_SIZE)
        self.check_table.horizontalHeader().setFont(header_font)
        # font size of the table
        font = self.check_table.font()
        font.setPointSize(TABLE_ROW_FONT_SIZE)
        self.check_table.setFont(font)

        layout.addWidget(self.check_table)
        bottom_group.setLayout(layout)
        return bottom_group


