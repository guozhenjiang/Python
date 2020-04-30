import sys

from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QCheckBox, QProgressBar, QLabel, QComboBox, QTextEdit
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMessageBox, QFontDialog, QColorDialog, QFileDialog

class Window(QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('PyQT tuts!')
        
        extractAction = QAction('&GET TO THE CHOOOHA!!!', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)
        
        openEditor = QAction('&Editor', self)
        openEditor.setShortcut('Ctrl+E')
        openEditor.setStatusTip('Open Editor')
        openEditor.triggered.connect(self.editor)
        
        openFile = QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        
        saveFile = QAction('&Save File', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        
        editorMenu = mainMenu.addMenu('&Editor')
        editorMenu.addAction(openEditor)
        
        self.home()
    
    def home(self):
        btn = QPushButton('Quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(0,100)

        extractAction = QAction('Flee the Scene', self)
        extractAction.triggered.connect(self.close_application)
        
        self.toolBar = self.addToolBar('1')
        self.toolBar.addAction(extractAction)
        self.addToolBar("2")
        self.addToolBar("3")
        
        fontChoice = QAction('Font', self)
        fontChoice.triggered.connect(self.font_choice)
        self.toolBar.addAction(fontChoice)
        
        fontColor = QAction('Font bg Color', self)
        fontColor.triggered.connect(self.color_picker)
        
        self.toolBar.addAction(fontColor)
        
        checkBox = QCheckBox('Enlarge Window', self)
        checkBox.move(150, 50)
        checkBox.stateChanged.connect(self.enlarge_window)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        
        self.btn = QPushButton('Dwonload', self)
        self.btn.move(200, 120)
        self.btn.clicked.connect(self.download)
        
        print(self.style().objectName())
        self.styleChoice = QLabel('Windows Vista', self)
        
        comboBox = QComboBox(self)
        comboBox.move(20, 50)
        comboBox.addItem('motif')
        comboBox.addItem('Windows')
        comboBox.addItem('cde')
        comboBox.addItem('Plastique')
        comboBox.addItem('Cleanlooks')
        comboBox.addItem('windowsvista')
        
        self.styleChoice.move(50, 150)
        comboBox.activated[str].connect(self.style_choice)
        
        self.show()
    
    def file_open(self)    :
        name, filters = QFileDialog.getOpenFileName(self, 'Open File')
        print()
        print(name)
        print()
        
        file = open(name, 'r', encoding='utf-8')
        
        self.editor()
        
        with file:
            text = file.read()
            print(text)
            self.textEdit.setText(text)
    
    def file_save(self):
        name, filters = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w', encoding='utf-8')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
    
    def color_picker(self):
        color = QColorDialog.getColor()
        self.styleChoice.setStyleSheet('QWidget { background-color: %s}' %(color.name()))
    
    def editor(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
    
    def font_choice(self):
        font, valid = QFontDialog.getFont()
        
        if valid:
            self.styleChoice.setFont(font)
    
    def style_choice(self, text):
        self.styleChoice.setText(text)
        QApplication.setStyle(QStyleFactory.create(text))
    
    def download(self):
        self.completed = 0
        
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
    
    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)
    
    def close_application(self):
        print('clicked')
        choice = QMessageBox.question(self,
                                      'Extract!',
                                      'Get into the chopper?',
                                      QMessageBox.Yes | QMessageBox.No)
        
        if choice == QMessageBox.Yes:
            print('Extracting Naaaaaa999ww!!!!')
            sys.exit()
        else:
            print('选择了 No')
            pass
        
def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()