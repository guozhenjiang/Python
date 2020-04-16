# https://www.learnpyqt.com/courses/start/basic-widgets/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QStatusBar, QAction, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QProgressBar, QRadioButton, QSlider, QSpinBox, QTimeEdit, QFontComboBox, QListWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle('My Awesom App')
        
        widget = QDoubleSpinBox()
        # widget.setMinimum(-10)
        # widget.setMaximum(3)
        widget.setRange(-10, 100)
        widget.setPrefix('$')
        widget.setSuffix('c')
        widget.setSingleStep(0.5)
        widget.valueChanged.connect(self.value_changed)
        widget.valueChanged[str].connect(self.value_changed_str)
        self.setCentralWidget(widget)
        
    def value_changed(self, i):
        print('val:', i)
        
    def value_changed_str(self, s):
        print('str:', s)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) is fine.
app = QApplication(sys.argv)

window = MainWindow()
window.show()                   # IMPORTANT!!!!! Windows are hidden by default.

app.exec_()                     # Start the event loop.