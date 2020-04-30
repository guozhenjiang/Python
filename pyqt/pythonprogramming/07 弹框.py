import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

class Window(QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('PyQT tuts!')
        
        extractAction = QAction('&GET TO THE CHOOOHA!!!', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        
        self.home()
    
    def home(self):
        btn = QPushButton('Quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(0,100)

        extractAction = QAction('Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)
        
        self.toolBar = self.addToolBar('1')
        self.addToolBar("2")
        self.addToolBar("3")
        self.toolBar.addAction(extractAction)
        
        self.show()
    
    def close_application(self):
        choice = QMessageBox.question(self, 'Extract!', 'Get into the chopper?', QMessageBox.Yes | QMessageBox.No)
        
        print(choice)
        
        if choice == QMessageBox.Yes:
            print('Yes')
            print('Extracting Naaaaaa999ww!!!!')
            sys.exit()
        else:
            print('No')
            pass
        
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()