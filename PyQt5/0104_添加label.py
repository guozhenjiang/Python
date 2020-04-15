# https://www.learnpyqt.com/courses/start/creating-your-first-window/

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle('My Awesom App')
        
        label = QLabel('THIS IS AWESOM!!!')
        label.setAlignment(Qt.AlignCenter)
        
        self.setCentralWidget(label)

app = QApplication(sys.argv)

window = MainWindow()
window.show()   # 这句很重要 不写就看不到窗口

app.exec_()