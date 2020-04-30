import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import QtCore

class Window(QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('PyQT tuts!')
        self.home()
    
    def home(self):
        btn = QPushButton('Quit', self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        # btn.resize(100, 100)
        # btn.move(100, 100)
        self.show()
        
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()