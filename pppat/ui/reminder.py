from PyQt5.QtWidgets import QFrame, QAction, QTextEdit, QToolBar, QVBoxLayout
from PyQt5.QtGui import QIcon
import os.path, time

LOGFILENAME = 'EiC_Reminder.md'

class EiCReminderWidget(QFrame):
    
    def __init__(self):
        super().__init__()
        # Pour faire joli, on encapsule le tout dans une QFrame avec bordure
        self.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.setLineWidth(1)
        self.setMidLineWidth(1)
        # reminder toolbar
        self.toolbar = QToolBar()
        self.test_action = QAction(QIcon(None), 'Last update :', self)
        self.toolbar.addAction(self.test_action)
        # reminder textbox
        self.text_edit = QTextEdit()
        self.text_edit.setMinimumWidth(0.95*self.width())
        # layout
        vbox = QVBoxLayout()
        vbox.setMenuBar(self.toolbar)
        vbox.addWidget(self.text_edit)
        self.setLayout(vbox)
        # automatically save the text as soon as it is modified
        self.text_edit.textChanged.connect(self.save_text)
        # load the text when launched
        self.load_text()
        # update the date when launched
        self.update_last_modification_date()
        
        
    def save_text(self):
        " Save the content of the text edit zone into a file. "
        text = self.text_edit.toPlainText()
        with open(LOGFILENAME, 'w') as f:
            f.write(text)      
        # update the date indicator
        self.update_last_modification_date()
    
    def load_text(self):
        " Load the content of the text file into the text edit zone. "
        try:
            with open(LOGFILENAME, 'r') as f:
                self.text_edit.setPlainText(f.read()) 
        except FileNotFoundError as e:
            # if the file does not exist (yet), fill it with nothing
            self.text_edit.setPlainText('')
    
    @property
    def last_modification_date(self):
        " Get the date of the file modification. "
        return time.ctime(os.path.getmtime(LOGFILENAME))
    
    def update_last_modification_date(self):
        " Update the date indicated above the text edit zone. "
        self.test_action.setText('Last update: ' + self.last_modification_date)
        

        