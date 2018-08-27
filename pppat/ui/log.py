# -*- coding: utf-8 -*-
"""
Logging Qt widget

@author: JH218595
"""
from qtpy.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout

import logging
# must NOT specify __name__ here, otherwise logging does not work in GUI...
# TODO : hid the IPython logs into this log console !!
logger = logging.getLogger()


class LoggerHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        # color the display message depending of its nature
        if "ERROR" in msg:
            html_msg = "<font color='Red'>"+msg+"</font>"
        elif "WARNING" in msg:
            html_msg = "<font color='Yellow'>"+msg+"</font>"
        else:
            html_msg = "<font color='Black'>"+msg+"</font>"

        self.widget.appendHtml(html_msg)


class QPlainTextEditLogger(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.zoomOut(2)

        log_handler = LoggerHandler(self.log_widget)

        logger.addHandler(log_handler)

        layout = QVBoxLayout()
        layout.addWidget(self.log_widget)
        self.setLayout(layout)
