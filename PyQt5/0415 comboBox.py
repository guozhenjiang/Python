# https://www.learnpyqt.com/courses/start/basic-widgets/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QStatusBar, QAction, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QProgressBar, QRadioButton, QSlider, QSpinBox, QTimeEdit, QFontComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle('My Awesom App')
        
        widget = QComboBox()
        self.setCentralWidget(widget)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) is fine.
app = QApplication(sys.argv)

window = MainWindow()
window.show()   # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()