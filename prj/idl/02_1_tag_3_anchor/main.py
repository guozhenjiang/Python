from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import sys
# sys.path.append('D:\\study\\python\\prj\idl\\02_一个标签三个基站')
from lib_comport import *
from lib_comport_ComboBox import *

class IndoorLocation:
    def __init__(self):
        # 从文件中加载 UI
        qfile_ui = QFile('ui_室内定位_01.ui')
        qfile_ui.open(QFile.ReadOnly)
        qfile_ui.close()
        
        self.ui = QUiLoader().load('./ui_室内定位_01.ui')
        
        # self.ui.button.clicked.connect(self.handleCalc)

app = QApplication([])
stats = IndoorLocation()
stats.ui.show()
app.exec_()