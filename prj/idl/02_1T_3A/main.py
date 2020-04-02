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
        
        self.ui_main = QUiLoader().load(str_ui_main)
        self.ui_main.plainTextEdit_Log.clear()
        
        self.Port = ComPort()
        
        # 菜单栏勾选项
        ui = self.ui_main
        ui.action_ViewAscii.checked = False
        ui.dockWidget_Ascii.hide()
        
        # 菜单控制 Dock 窗口是否显示
        ui.action_ViewSet.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Set, ui.action_ViewSet.isChecked()))
        ui.action_ViewLog.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Log, ui.action_ViewLog.isChecked()))
        ui.action_ViewHex.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Hex, ui.action_ViewHex.isChecked()))
        ui.action_ViewAscii.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Ascii, ui.action_ViewAscii.isChecked()))
        
        # 信号与槽
        self.log('设置信号与槽')
        self.ui_main
        self.ui_main.pushButton_PortScan.clicked.connect(lambda:self.update_PortSelect_Item(self.ui_main.comboBox_PortSelect))
        
        # 初始化
        self.log('初始化 UI')
        self.init_ui(self.ui_main)   # 初始化 UI
    
    # Log 功能
    def log(self, log_str):
        print(log_str)
        self.ui_main.plainTextEdit_Log.appendPlainText(log_str)
        pass
    
    # 初始化 UI
    def init_ui(self, ui):
        self.log('更新端口选择下来菜单内容')
        self.update_PortSelect_Item(ui.comboBox_PortSelect)
    
    # 槽函数
    def dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
        
        # if(is_checked):
        #     dock_set.show()
        # else:
        #     dock_set.hide()
    
    def action_check_status_set(self, item, new_status):
        item.checked = new_status
    
    # 更新可用端口项
    def update_PortSelect_Item(self, ComboBox):
        self.log('更新可用端口')
        
        ComboBox.clear()        # 清空当前端口选择下拉菜单内容
        
        valid_ports = self.Port.scan()
        print('%d 个可用端口' %(len(valid_ports)))        
        if(len(valid_ports) > 0):
            ComboBox.addItems(valid_ports)
        else:
            ComboBox.addItem('无可用端口')
            
        
        
        
        # self.ui_main.button.clicked.connect(self.handleCalc)
        
app = QApplication([])
idl = IndoorLocation()
idl.ui_main.show()
app.exec_()