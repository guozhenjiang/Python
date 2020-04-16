# https://www.learnpyqt.com/courses/start/dialogs/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QStatusBar, QAction, QHBoxLayout, QVBoxLayout, QGridLayout, QStackedLayout, QTabWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QLCDNumber, QLineEdit
from PyQt5.QtWidgets import QProgressBar, QRadioButton, QSlider, QSpinBox, QTimeEdit, QFontComboBox, QListWidget, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QPalette, QColor

class CustomDialog(QDialog):
    
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        
        self.setWindowTitle('My custom dialog!')
        
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle('My Awesom App')
        
        label = QLabel('THIS IS AWESOM!!!')
        
        label.setAlignment(Qt.AlignCenter)
        
        self.setCentralWidget(label)
        
        toolbar = QToolBar('My main toolbar')
        self.addToolBar(toolbar)
        
        button_action = QAction(QIcon(r'.\icons\bug_16x16.png'), 'Your button', self)
        button_action.setStatusTip('This is your button')
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        
        toolbar.addSeparator()
        
        button_action2 = QAction(QIcon(r'.\icons\bug_16x16.png'), 'Your button2', self)
        button_action2.setStatusTip('This is your button2')
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        
        toolbar.addWidget(QLabel('Hello'))
        toolbar.addWidget(QCheckBox())
        
        self.setStatusBar(QStatusBar(self))
        
        menu = self.menuBar()
        menu.setNativeMenuBar(False)    # Disables the global menu bar on MacOS
        
        file_menu = menu.addMenu('&File')
        file_menu.addAction(button_action)
        
        file_menu.addSeparator()
        
        file_menu.addAction(button_action2)
    
    def onMyToolBarButtonClick(self, s):
        print('click', s)
        
        dlg = CustomDialog(self)
        if dlg.exec_():
            print('Success!')

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) is fine.
app = QApplication(sys.argv)

window = MainWindow()
window.show()                   # IMPORTANT!!!!! Windows are hidden by default.

app.exec_()                     # Start the event loop.