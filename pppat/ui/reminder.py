from PyQt5.QtWidgets import QFrame, QAction, QTextEdit, QToolBar, QVBoxLayout
from PyQt5.QtGui import QIcon

class EiCReminderWidget(QFrame):
    
    def __init__(self):
        super().__init__()
        # Pour faire joli, on encapsule le tout dans une QFrame avec bordure
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)
        # reminder toolbar
        self.toolbar = QToolBar()
        test_action = QAction(QIcon(None), 'test', self)
        self.toolbar.addAction(test_action)
        # reminder textbox
        self.text_edit = QTextEdit()
        self.text_edit.setMinimumWidth(0.95*self.width())
        # layout
        vbox = QVBoxLayout()
        vbox.setMenuBar(self.toolbar)
        vbox.addWidget(self.text_edit)
        self.setLayout(vbox)