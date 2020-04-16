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
        
        widget = QLineEdit()
        widget.setPlaceholderText('Enter your text')
        widget.returnPressed.connect(self.return_pressed)   # 单行输入按下回车时
        widget.selectionChanged.connect(self.selection_changed)
        widget.textChanged.connect(self.text_changed)
        widget.textEdited.connect(self.text_edited)
        self.setCentralWidget(widget)
    
    def return_pressed(self):
        print('Return pressed!')
    
    def selection_changed(self):
        print('Selection changed')
        print(self.centralWidget().selectedText())
        
    def text_changed(self, s):
        print('Text changed...')
        print(s)
    
    def text_edited(self, s):
        print('Text edited...')
        print(s)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) is fine.
app = QApplication(sys.argv)

window = MainWindow()
window.show()   # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()