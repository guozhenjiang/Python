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
        btn.clicked.connect(self.close_application)
        # btn.resize(100, 100)
        # btn.move(100, 100)
        self.show()
    
    def close_application(self):
        print('whooaaaaa so custom!!!')
        sys.exit()
        
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()