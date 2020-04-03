from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

# import sys
# sys.path.append('D:\\study\\python\\prj\idl\\02_一个标签三个基站')
from lib_comport import *
from lib_comport_ComboBox import *

from PySide2.QtCore import Signal, Slot

class IndoorLocation(QObject):
    # 实例化
    def __init__(self):
        # 从文件中加载 UI
        str_ui_main = './ui_idl_main.ui'
        qfile_ui = QFile(str_ui_main)
        qfile_ui.open(QFile.ReadOnly)
        qfile_ui.close()
        
        self.Port = ComPort()
        self.ui_main = QUiLoader().load(str_ui_main)
        
        ui = self.ui_main
        
        ui.plainTextEdit_Log.clear()
        
        # self.ui_main.comboBox_PortSelect = ComPort_ComboBox()   # 替换界面中的端口选择下拉框 未实现
        
        # Dock 窗口显示隐藏设置
        self.log('隐藏 ASCII 窗口')
        ui.action_ViewSet.checked = True
        ui.action_ViewLog.checked = True
        ui.action_ViewHex.checked = True
        ui.action_ViewAscii.checked = False
        
        ui.dockWidget_Set.show()
        ui.dockWidget_Log.show()
        ui.dockWidget_Hex.show()
        ui.dockWidget_Ascii.hide()
        
        # 菜单控制 Dock 窗口是否显示
        self.log('信号与槽 Dock 显示隐藏')
        ui.action_ViewSet.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Set, ui.action_ViewSet.isChecked()))
        ui.action_ViewLog.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Log, ui.action_ViewLog.isChecked()))
        ui.action_ViewHex.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Hex, ui.action_ViewHex.isChecked()))
        ui.action_ViewAscii.changed.connect(lambda:self.dock_show_hide(ui.dockWidget_Ascii, ui.action_ViewAscii.isChecked()))
        
        # 信号与槽 设置
        self.log('信号与槽 设置 扫描端口')
        ui.pushButton_PortScan.clicked.connect(lambda:self.Port.scan(self.ui_main.comboBox_PortSelect))
        
        self.log('信号与槽 设置 选择端口')
        ui.comboBox_PortSelect.currentTextChanged.connect(lambda:self.Port.set_com(ui.comboBox_PortSelect.currentText()))
        
        self.log('信号与槽 设置 波特率')
        ui.comboBox_BaudSelect.currentTextChanged.connect(lambda:self.Port.set_baud(ui.comboBox_BaudSelect.currentText()))
        
        self.log('信号与槽 设置 数据位')
        ui.comboBox_DataBitSelect.currentTextChanged.connect(lambda:self.Port.set_data_bit(ui.comboBox_DataBitSelect.currentText()))
        
        self.log('信号与槽 设置 校验')
        ui.comboBox_ParityBitSelect.currentTextChanged.connect(lambda:self.Port.set_parity(ui.comboBox_ParityBitSelect.currentText()))
        
        self.log('信号与槽 设置 停止位')
        ui.comboBox_StopBitSelect.currentTextChanged.connect(lambda:self.Port.set_stop_bit(ui.comboBox_StopBitSelect.currentText()))
        
        self.log('信号与槽 设置 流控 XonXoff')
        ui.checkBox_XonXoff.stateChanged.connect(lambda:self.Port.set_XonXoff(ui.checkBox_XonXoff.isChecked()))
        
        self.log('信号与槽 设置 流控 RtsCts')
        ui.checkBox_RtsCts.stateChanged.connect(lambda:self.Port.set_RtsCts(ui.checkBox_RtsCts.isChecked()))
        
        self.log('信号与槽 设置 流控 XoDsrDtrnXoff')
        ui.checkBox_DsrDtr.stateChanged.connect(lambda:self.Port.set_DsrDtr(ui.checkBox_DsrDtr.isChecked()))
        
        self.log('信号与槽 设置 打开端口')
        ui.pushButton_PortOpenClose.clicked.connect(lambda:self.Port.open_close())
        
        # self.log('信号与槽 设置 打开端口 根据状态改变按键')
        '''
            注意:
                如果下面的 connect 中的 slot 函数带括号 后面就不会触发了！
        '''
        self.Port.signal_PortOpenClose.connect(self.slot_button_update)
        
        # 初始化
        self.log('初始化 UI')
        self.init_ui(self.ui_main)   # 初始化 UI
        self.Port.scan(self.ui_main.comboBox_PortSelect)
        
        # print('测试修改按键文字 开始')
        # # self.ui_main.good.setText = 'a'     # AttributeError: 'PySide2.QtWidgets.QMainWindow' object has no attribute 'good'
        # self.ui_main.pushButton_PortOpenClose.abcdefg = 'a'
        # print('测试修改按键文字 结束')

    # def set_button_text(self, new_text):
    #     self.ui_main.pushButo
    
    # @Slot()
    @Slot(bool)
    def slot_button_update(self, is_open):
        print('进入 slot')
        if(is_open):
            self.ui_main.pushButton_PortOpenClose.setText('关闭端口')
            
        else:
            self.ui_main.pushButton_PortOpenClose.setText('打开端口')
        
        self.ui_main.groupBox_PortSet.setEnabled(not is_open)
    
    # Log 功能
    def log(self, log_str):
        print(log_str)
        self.ui_main.plainTextEdit_Log.appendPlainText(log_str)
        
        # # 将光标移动到末尾 未实现
        # cusor = self.ui_main.plainTextEdit_Log.textCusor()
        # cusor.movePosition(QtGui.QTextCursor.End)
        # self.ui_main.plainTextEdit_Log.setTextCusor(cusor)
        pass
    
    # 初始化 UI
    def init_ui(self, ui):
        self.log('更新端口选择下来菜单内容')
        # self.update_PortSelect_Item(ui.comboBox_PortSelect)
    
    # 槽函数
    def dock_show_hide(self, dock_set, is_checked):
        # 方法 1
        dock_set.setVisible(is_checked)
        
        # 方法 2
        # if(is_checked):
        #     dock_set.show()
        # else:
        #     dock_set.hide()
    
    def action_check_status_set(self, item, new_status):
        item.checked = new_status
        
app = QApplication([])
idl = IndoorLocation()
idl.ui_main.show()
app.exec_()