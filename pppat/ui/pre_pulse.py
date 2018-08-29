# -*- coding: utf-8 -*-
"""
PPPAT - Pre pulse analysis ui
"""
from qtpy.QtWidgets import (QWidget, QGridLayout, QRadioButton, QGroupBox,
                            QVBoxLayout, QTextBrowser, QLabel, QPushButton,
                            QFormLayout, QLineEdit, QFileDialog, QComboBox,
                            QErrorMessage)
from qtpy.QtGui import QIntValidator
from qtpy.QtCore import Slot

import logging
logger = logging.getLogger(__name__)


class PrePulseAnalysisWidget(QWidget):
    """
    Pre-pulse gui
    
    Create all the widgets in the Pre-pulse analysis panel.
    """
    def __init__(self, parent=None):
        super(PrePulseAnalysisWidget, self).__init__(parent=parent)
        
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
        top_left_group = QGroupBox("Load pulse setup from:")
                
        self.radio_sl = QRadioButton('Session Leader')
        self.radio_shot = QRadioButton('Shot number')
        self.radio_file = QRadioButton('File')
        #comboBox_file = QComboBox(None)
        self.push_browse = QPushButton('Browse')
        
        self.edit_shot = QLineEdit()
        self.edit_shot.setPlaceholderText('Shot Number')
        self.edit_shot.textChanged.connect(self._validate_radio_shot)
        self.edit_shot.setValidator(QIntValidator())  # only integer for shot# 
        
        self.push_load = QPushButton('Load')

        layout = QGridLayout()
        layout.addWidget(self.radio_sl, 0, 0)
        layout.addWidget(self.radio_shot, 1, 0)
        layout.addWidget(self.edit_shot, 1, 1)
        layout.addWidget(self.radio_file, 2, 0)
        layout.addWidget(self.push_browse, 2, 1)
        layout.addWidget(self.push_load, 3, 0, 1, 2)
        top_left_group.setLayout(layout)

        return top_left_group

    @Slot()
    def _validate_radio_shot(self):
        self.radio_shot.setChecked(True)
        
    def _create_top_right_group(self):
        """
        Top Right widgets group
        """
        top_right_group = QGroupBox('Pulse settings informations')
        
        self.pulse_setting_origin = QLabel()
        self.pulse_properties = QLabel()
        
        layout = QFormLayout()
        layout.addRow(QLabel('Pulse settings from:'), self.pulse_setting_origin)
        layout.addRow(QLabel('Pulse properties:'), self.pulse_properties)
        top_right_group.setLayout(layout)
        
        return top_right_group
    
    def _create_bottom_group(self):
        """
        Bottom widgets group
        
        TODO
        """
        return QTextBrowser()


            

