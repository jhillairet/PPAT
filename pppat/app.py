from qtpy.QtWidgets import QApplication
from pppat.ui.mainwindow import MainWindow


def run(argv):
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    return app.exec_()
