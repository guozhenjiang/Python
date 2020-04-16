# https://www.learnpyqt.com/courses/start/layouts/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QStatusBar, QAction, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QProgressBar, QRadioButton, QSlider, QSpinBox, QTimeEdit, QFontComboBox, QListWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QPalette, QColor

class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle('My Awesom App')
        
        layout = QGridLayout()
        
        layout.addWidget(Color('red'), 0, 0)
        layout.addWidget(Color('green'), 1, 0)
        layout.addWidget(Color('blue'), 1, 1)
        layout.addWidget(Color('purple'), 2, 1)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) is fine.
app = QApplication(sys.argv)

window = MainWindow()
window.show()                   # IMPORTANT!!!!! Windows are hidden by default.

app.exec_()                     # Start the event loop.