"""
Control Room

@authors: J.Hillairet
"""
# Running this script will launch control room's graphical user interface
if __name__ == '__main__':
    import sys
    from pppat.control_room.control_room import *

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    win = ControlRoom()
    win.show()
    sys.exit(app.exec_())
    
