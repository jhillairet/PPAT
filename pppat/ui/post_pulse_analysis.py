# -*- coding: utf-8 -*-
"""
PPPAT - Post pulse analysis ui
"""
from qtpy.QtWidgets import (QWidget, QGridLayout, QRadioButton, QGroupBox,
                            QVBoxLayout, QTextBrowser, QLabel, QPushButton,
                            QFormLayout, QLineEdit, QFileDialog, QComboBox,
                            QErrorMessage, QTableView, QAbstractItemView,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from qtpy.QtGui import QIntValidator, QFont
from qtpy.QtCore import Slot

import logging
logger = logging.getLogger(__name__)




TABLE_HEADER_FONT_SIZE = 10
TABLE_ROW_FONT_SIZE = 8
TABLE_ROW_SIZE = 30

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
        self.radio_shot = QRadioButton('Pulse number')

        self.edit_shot = QLineEdit()
        self.edit_shot.setPlaceholderText('Pulse Number')
        self.edit_shot.textChanged.connect(self._validate_radio_shot)
        self.edit_shot.setValidator(QIntValidator())  # only integer for shot#

        layout = QGridLayout()
        layout.addWidget(self.radio_last_pulse, 0, 0)
        layout.addWidget(self.radio_shot, 1, 0)
        layout.addWidget(self.edit_shot, 1, 1)
        top_left_group.setLayout(layout)

        return top_left_group

    @Slot()
    def _validate_radio_shot(self):
        self.radio_shot.setChecked(True)

    def _create_top_right_group(self):
        """
        Top Right widgets group
        """
        top_right_group = QGroupBox('Pulse informations')

        self.pulse_number = QLabel()
        self.push_check = QPushButton('Post pulse analysis - all')

        layout0 = QVBoxLayout()
        layout1 = QFormLayout()
        layout1.addRow(QLabel('Pulse number:'), self.pulse_number)
        layout0.addLayout(layout1)
        layout0.addWidget(self.push_check)

        top_right_group.setLayout(layout0)

        return top_right_group

    def _create_bottom_group(self):
        """
        Bottom widgets group
        """
        bottom_group = QGroupBox('Check results')
        layout = QVBoxLayout()

        self.check_table = QTableWidget(12, 4)
        self.check_table.setHorizontalHeaderLabels(['State', 'Check', 
                                                    'Result',
                                                    'Result description'])
        # # Columns config
        # resize the column widths
        self.check_table.horizontalHeader().resizeSection(0, 20)
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

    def _fill_table(self):
        """
        Fill the post test table 
        """
    