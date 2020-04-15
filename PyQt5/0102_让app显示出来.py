# https://www.learnpyqt.com/courses/start/creating-your-first-window/

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class MainWindow(QMainWindow):
    pass

app = QApplication(sys.argv)

window = MainWindow()
window.show()   # 这句很重要 不写就看不到窗口

app.exec_()