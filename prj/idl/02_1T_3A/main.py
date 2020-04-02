from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

# import sys
# sys.path.append('D:\\study\\python\\prj\idl\\02_一个标签三个基站')
from lib_comport import *
from lib_comport_ComboBox import *

class IndoorLocation:
    # 实例化
    def __init__(self):
        # 从文件中加载 UI
        str_ui_main = './ui_idl_main.ui'
        qfile_ui = QFile(str_ui_main)
        qfile_ui.open(QFile.ReadOnly)
        qfile_ui.close()
        
        self.ui = QUiLoader().load(str_ui_main)
        self.ui.plainTextEdit_Log.clear()
        self.Port = ComPort()
        
        # 信号与槽
        self.log('设置信号与槽：扫描端口按键')
        self.ui.pushButton_PortScan.clicked.connect(lambda:self.update_PortSelect_Item(self.ui.comboBox_PortSelect))
        
        # 初始化
        self.log('初始化 UI')
        self.init_ui(self.ui)
    
    # Log 功能
    def log(self, log_str):
        self.ui.plainTextEdit_Log.appendPlainText(log_str)
        pass
    
    # 初始化 UI
    def init_ui(self, ui):
        
        
        self.log('更新端口选择下来菜单内容')
        self.update_PortSelect_Item(self.ui.comboBox_PortSelect)
        
    def update_PortSelect_Item(self, ComboBox):
        self.log('更新可用端口')
        
        ComboBox.clear()        # 清空当前端口选择下拉菜单内容
        
        valid_ports = self.Port.scan()
        print('%d 个可用端口' %(len(valid_ports)))        
        if(len(valid_ports) > 0):
            ComboBox.addItems(valid_ports)
        else:
            ComboBox.addItem('无可用端口')
            
        
        
        
        # self.ui.button.clicked.connect(self.handleCalc)
        
app = QApplication([])
idl = IndoorLocation()
idl.ui.show()
app.exec_()