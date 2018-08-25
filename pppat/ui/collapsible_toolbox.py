# -*- coding: utf-8 -*-
"""
A collapsible toolbox widget, 

directly inspired from https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt

"""
# taken from https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
import sys
from qtpy.QtWidgets import (QWidget, QScrollArea, QFrame, QToolButton,
                            QGridLayout, QSizePolicy, QApplication, 
                            QVBoxLayout, QTextEdit, QLabel, QHBoxLayout)
from qtpy.QtCore import (QParallelAnimationGroup, QPropertyAnimation,
                         QAbstractAnimation)
from qtpy.QtCore import Qt


class QCollapsibleToolbox(QWidget):
    """
    References:
    # Adapted from c++ version
    http://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
    """
    def __init__(self, parent=None, child=None, title='', animationDuration=300):
        super(QCollapsibleToolbox, self).__init__(parent=parent)
        
        self.animationDuration = animationDuration
        self.toggleAnimation = QParallelAnimationGroup()
        self.contentArea = QScrollArea()
        self.headerLine = QFrame()
        self.toggleButton = QToolButton()
        self.mainLayout = QGridLayout()

        toggleButton = self.toggleButton
        toggleButton.setStyleSheet("QToolButton { border: none; }")
        toggleButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toggleButton.setArrowType(Qt.RightArrow)
        toggleButton.setText(str(title))
        toggleButton.setCheckable(True)
        toggleButton.setChecked(False)

        headerLine = self.headerLine
        headerLine.setFrameShape(QFrame.HLine)
        headerLine.setFrameShadow(QFrame.Sunken)
        headerLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.contentArea.setStyleSheet("QScrollArea { background-color: white; border: none; }")
        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(QPropertyAnimation(self.contentArea, b"maximumHeight"))
        # don't waste space
        mainLayout = self.mainLayout
        mainLayout.setVerticalSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        row = 0
        mainLayout.addWidget(self.toggleButton, row, 0, 1, 1, Qt.AlignLeft)
        mainLayout.addWidget(self.headerLine, row, 2, 1, 1)
        row += 1
        mainLayout.addWidget(self.contentArea, row, 0, 1, 3)
        self.setLayout(self.mainLayout)

        def start_animation(checked):
            arrow_type = Qt.DownArrow if checked else Qt.RightArrow
            direction = QAbstractAnimation.Forward if checked else QAbstractAnimation.Backward
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.clicked.connect(start_animation)

        # If a QWidget is passed as child, add this child inside 
        # a default layout. Convenient function        
        if child:
            default_layout = QHBoxLayout()
            default_layout.addWidget(child)
            self.widget = child
            self.setContentLayout(default_layout)

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount()-1):
            spoilerAnimation = self.toggleAnimation.animationAt(i)
            spoilerAnimation.setDuration(self.animationDuration)
            spoilerAnimation.setStartValue(collapsedHeight)
            spoilerAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(self.toggleAnimation.animationCount() - 1)
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

    def setChecked(self, checked=False):
        pass
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # creating a first spoiler
    vbl1 = QVBoxLayout()
    vbl1.addWidget(QLabel('salut'))
    vbl1.addWidget(QTextEdit())
    spoiler1 = QCollapsibleToolbox(title='coucou')
    spoiler1.setContentLayout(vbl1)
    # creating a second spoiler
    vbl2 = QVBoxLayout()
    vbl2.addWidget(QLabel('hop'))
    vbl2.addWidget(QTextEdit())
    spoiler2 = QCollapsibleToolbox(title='et voilà')
    spoiler2.setContentLayout(vbl2)
    # main window contains the two spoilers    
    vbox = QVBoxLayout()
    vbox.addWidget(spoiler1)
    vbox.addWidget(spoiler2)
    window = QWidget()    
    window.setLayout(vbox)
    window.show()
    
    sys.exit(app.exec_())    
