# -*- coding: utf-8 -*-
from qtpy.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout

import logging
# must NOT specify __name__ here, otherwise logging does not work in GUI...
logger = logging.getLogger()

# TODO : hid the IPython logs into this log console !!


class LoggerHandler(logging.Handler):
    """
    Logging handler associated to QPlainTextEditLogger widget
    """
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        # only display into the widget the date/nature/message (not %(module))
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s',
                                      "%Y-%m-%d %H:%M:%S")
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        # color the display message depending of its nature
        if "ERROR" in msg:
            html_msg = "<font color='Red'>"+msg+"</font>"
        elif "WARNING" in msg:
            html_msg = "<font color='Orange'>"+msg+"</font>"
        elif "UNAVAILABLE" in msg:
            html_msg = "<font color='Purple'>"+msg+"</font>"
        elif "OK" in msg:
            html_msg = "<font color='Green'>"+msg+"</font>"
        else:
            html_msg = "<font color='Black'>"+msg+"</font>"

        self.widget.appendHtml(html_msg)


class QPlainTextEditLogger(QWidget):
    """
    QtWidget consisting in a QPlainTextEdit which display logging logs
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.zoomOut(2)

        log_handler = LoggerHandler(self.log_widget)

        logger.addHandler(log_handler)
        logger.addFilter(NoDebugFilter())

        layout = QVBoxLayout()
        layout.addWidget(self.log_widget)
        self.setLayout(layout)

#class NoWordFilter(logging.Filter):
#    """ Filter logging message containing a specific word """
#    def filter(self, record):
#        return not ('word' in record.getMessage())

class NoDebugFilter(logging.Filter):
    def filter(self, record):
        """
        Filter logging message (LogRecord) is they are of DEBUG level.
        This function has been made to filter pywed DEBUG messages, which are
        generated at the root level of logging and make at lot of noise...

        Returns
        -------
        do_filter: Boolean
            Is the specified record to be logged?
            Returns zero for no, nonzero for yes.
        """
        return not record.levelno == logging.DEBUG
