from PySide2.QtWidgets import QApplication, QComboBox
from PySide2.QtGui import QTextCursor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QTextStream, QTimer
from lib_comport import *
from lib_comport_ComboBox import *
from PySide2.QtCore import Signal, Slot
import time
import datetime
import _thread, threading

'''
    QComboBox
        https://doc.qt.io/qtforpython/PySide2/QtWidgets/QComboBox.html
    QFile
        https://doc.qt.io/qt-5/qfile.html
    QTextStream
        https://doc.qt.io/qtforpython/PySide2/QtCore/QTextStream.html
    QGridLayout
        https://doc.qt.io/qtforpython/PySide2/QtWidgets/QGridLayout.html
'''

class IndoorLocation(QObject):
    # 实例化
    def __init__(self):
        self.name = 'IDL'
        
        log_file_loc = './log.txt'
        print('以读写打开 %s' %(log_file_loc))
        log_file = QFile(log_file_loc)
        log_file.open(QFile.ReadWrite | QFile.Truncate)
        
        self.log_stamp_last = time.perf_counter()
        self.log_stream = QTextStream(log_file)
        self.log_stream.setCodec('UTF-8')
        self.log_stream.seek(log_file.size())
        
        # print(self.log_stream.readAll())
        
        # print('%s 每行内容' %(log_file_loc))
        # while(not log_file.atEnd()):
        #     line = log_file.readLine()
        #     print(line)
        
        # print('使用 QTextStream 写 log')
        # self.log_stream.seek(log_file.size())
        # time.sleep(0.5)
        # self.log_stream << self.log_stream.pos() << '|' << datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') << '\r\n'
        
        file_loc_ui_main = './ui_idl_main.ui'
        self.ui_main = QUiLoader().load(file_loc_ui_main)
        self.log('载入 %s' %(file_loc_ui_main))
        self.port = Port()                              # 实例化
        
        # 初始化
        self.init_ui()
        self.init_signal_slot()
        # self.slot_port_scan()
        self.slot_PortComboBox_showPopup()
    
    # Log 功能
    def log(self, log):
        # print(time.perf_counter(), ' --- ', time.process_time())
        self.log_stamp = time.perf_counter()    # time.clock()  time.process_time()
        log_stamp_det = self.log_stamp - self.log_stamp_last
        self.log_stamp_last = self.log_stamp
        
        if(log_stamp_det > 0.1):
            new_line = '\r\n'
        else:
            new_line = ''
        
        # print(log_stamp_det)
        
        # stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # stamp = time.strftime("%H:%M:%S ", time.localtime())
        stamp = ''
        new_log_str = new_line + stamp + log
        
        self.log_stream << new_log_str << '\r\n'
        self.ui_main.plainTextEdit_Log.appendPlainText(new_log_str)
        # self.ui_main.plainTextEdit_Log.moveCursor(QTextCursor.End)
        # self.ui_main.plainTextEdit.setSelection()
        print(new_log_str)
        
        
        pass
    
    def init_ui(self):
        self.log('初始化 UI')
        ui = self.ui_main
        ui.action_ViewSet.checked = True
        ui.action_ViewLog.checked = True
        ui.action_ViewHex.checked = True
        ui.action_ViewAscii.checked = False
        
        ui.dockWidget_Set.show()
        ui.dockWidget_Log.show()
        ui.dockWidget_Hex.show()
        ui.dockWidget_Ascii.hide()
        
        ui.action_ViewSet.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Set, ui.action_ViewSet.isChecked()))
        ui.action_ViewLog.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Log, ui.action_ViewLog.isChecked()))
        ui.action_ViewHex.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Hex, ui.action_ViewHex.isChecked()))
        ui.action_ViewAscii.changed.connect(lambda:self.slot_dock_show_hide(ui.dockWidget_Ascii, ui.action_ViewAscii.isChecked()))
        
        ui.comboBox_name.deleteLater()          # 删掉 UI 生成的端口选择下拉框控件
        ui.PortComboBox_name = PortComboBox()   # 用自己重写的下拉框控件替换被删的
        ui.gridLayout_port_set_select.addWidget(ui.PortComboBox_name, 0, 1) # 添加到原来的布局框中相同位置
        # ui.PortComboBox_name.show()             # 显示控件
    
    def init_signal_slot(self):
        self.log('初始化 Signal Slot')
        ui = self.ui_main
        
        ui.PortComboBox_name.signal_PortComboBox_showPopup.connect(self.slot_PortComboBox_showPopup)
        ui.PortComboBox_name.currentTextChanged.connect(    lambda:self.slot_port_name())
        ui.comboBox_baud.currentTextChanged.connect(    lambda:self.slot_port_baud())
        ui.comboBox_byte.currentTextChanged.connect(    lambda:self.slot_port_byte())
        ui.comboBox_parity.currentTextChanged.connect(  lambda:self.slot_port_parity())
        ui.comboBox_stop.currentTextChanged.connect(    lambda:self.slot_port_stop())
        ui.checkBox_xonxoff.stateChanged.connect(       lambda:self.slot_port_xonxoff())
        ui.checkBox_rtscts.stateChanged.connect(        lambda:self.slot_port_rtscts())
        ui.checkBox_dsrdtr.stateChanged.connect(        lambda:self.slot_port_dsrdtr())
        ui.pushButton_open_close.clicked.connect(       lambda:self.slot_port_open_close())
        ui.pushButton_CleanReceive.clicked.connect(     lambda:self.slot_clean_receive())
    
    def slot_PortComboBox_showPopup(self):
        print('slot_PortComboBox_showPopup')
        self.log('扫描端口')
        port = self.port
        cmb = self.ui_main.PortComboBox_name
        
        port.name_last = cmb.currentText()
        cmb.clear()     # 会触发 Signal: ui.PortComboBox_name.currentTextChanged
        port.scan()
        
        if(len(port.valid) > 0):
            cmb.addItems(port.valid)
        else:
            cmb.addItem('无可用端口')
        
        idx = cmb.findText(port.name_last)
        
        if(idx >= 0):
            cmb.setCurrentIndex(idx)
        else:
            cmb.setCurrentIndex(0)
    
    def slot_port_name(self):
        self.port.name = self.ui_main.PortComboBox_name.currentText()
        self.log('端口 %s' %(self.port.name))
    
    def slot_port_baud(self):
        self.port.baud = int(self.ui_main.comboBox_baud.currentText(), 10)
        self.log('波特率 %s' %(self.port.baud))
    
    def slot_port_byte(self):
        self.port.byte = int(self.ui_main.comboBox_byte.currentText(), 10)
        self.log('字节宽度 %s' %(self.port.byte))
    
    def slot_port_parity(self):
        self.port.set_parity(self.ui_main.comboBox_parity.currentText())
        self.log('校验 %s' %(self.port.parity))
    
    def slot_port_stop(self):
        self.port.set_stop(self.ui_main.comboBox_stop.currentText())
        self.log('停止位 %s' %(self.port.stop))
    
    def slot_port_xonxoff(self):
        self.port.xonxoff = self.ui_main.checkBox_xonxoff.isChecked()
        self.log('软件流控 %s' %(self.port.xonxoff))
    
    def slot_port_rtscts(self):
        self.port.rtscts = self.ui_main.checkBox_rtscts.isChecked()
        self.log('RTS/CTS %s' %(self.port.rtscts))
    
    def slot_port_dsrdtr(self):
        self.port.dsrdtr = self.ui_main.checkBox_dsrdtr.isChecked()
        self.log('DSR/DTR %s' %(self.port.dsrdtr))
    
    def force_update_port_parameter(self):
        self.log('从 UI 获取端口设置')
        self.slot_port_name()
        self.slot_port_baud()
        self.slot_port_byte()
        self.slot_port_parity()
        self.slot_port_stop()
        self.slot_port_xonxoff()
        self.slot_port_rtscts()
        self.slot_port_dsrdtr()
    
    def slot_port_open_close(self):
        self.log('%s' %(self.ui_main.pushButton_open_close.text()))
        
        if(not self.port.isopen):
            self.force_update_port_parameter()
            port = self.port
            self.log('尝试打开 %s %s %s %s %s %s %s %s ' %(port.name, port.baud, port.byte, port.parity, port.stop, port.xonxoff, port.rtscts, port.dsrdtr))
        
        self.port.open_close()
        
        self.ui_main.groupBox_PortSet.setEnabled(not self.port.isopen)
        
        if(self.port.isopen):
            self.ui_main.pushButton_open_close.setText('关闭端口')
            self.log('端口打开')
            # self.idl_rx_process_start()
        else:
            self.ui_main.pushButton_open_close.setText('打开端口')
            self.log('端口关闭')
            # self.idl_rx_process_stop()
    
    def slot_clean_receive(self):
        self.ui_main.plainTextEdit_Hex.clear()
        self.ui_main.plainTextEdit_Ascii.clear()
    
    # 槽函数
    def slot_dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
    
    def receive_port_data(self):
        port = self.port
        data_text = self.ui_main.plainTextEdit_Hex
        
        if(self.port.isopen):
            if(port.port.in_waiting > 0):           # inWaiting()
                new_bytes = port.port.read()
                new_str = new_bytes.hex()
                
                print()
                print(type(new_bytes), new_bytes)
                print(type(new_str), new_str)
                
                # data_text.appendPlainText(new_str)                # 追加方式会导致每项换行
                
                data_text.moveCursor(QTextCursor.End)               # 手动在末尾插入
                data_text.insertPlainText(new_str + ' ')
    
    def idl_rx_process_start(self):
        self.t_rx = threading.Thread(target=IndoorLocation.receive_port_data, args=(self,))
        self.t_rx.start()
        self.t_rx.join()
    
    def idl_rx_process_stop(self):
        self.t_rx.stop()

# class Thread_UartRx(threading.Thread):
#     def __init__(self, name):
#         threading.Thread.__init__(self)
#         self.name = name
    
#     def run(self):
#         print()
        

app = QApplication([])

idl = IndoorLocation()
idl.ui_main.show()

timer = QTimer()
timer.timeout.connect(idl.receive_port_data)
timer.start(0)

# idl.idl_rx_process_start()

app.exec_()