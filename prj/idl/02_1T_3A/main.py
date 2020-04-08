from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QComboBox
from PySide2.QtGui import QTextCursor
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
from PySide2.QtCore import QFile, QTextStream, QTimer
from lib_comport import *
from lib_comport_ComboBox import *
from PySide2.QtCore import Signal, Slot
import time
import datetime
import _thread, threading
import sys
# import pyglet

# Matplotlib 图像嵌入
import matplotlib
from matplotlib.pyplot import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import matplotlib.pyplot as plt

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
        
        Anchor_t = {'name':'Anchor', 'color':'g', 'x':0.0, 'y':0.0, 'z':0.0, 'r':0.0}
        Tag_t = {'name':'Tag', 'r0':0.0, 'r1':0.0, 'r2':0.0,'x':0.0, 'y':0.0, 'z':0.0}
        
        self.Anchor0 = Anchor_t.copy()
        self.Anchor1 = Anchor_t.copy()
        self.Anchor2 = Anchor_t.copy()
        
        self.Tag = Tag_t.copy()
        
        self.Anchor0['name'] = 'Anchor0'
        self.Anchor0['color'] = 'r'
        self.Anchor0['x'] = 0.0
        self.Anchor0['y'] = 0.0
        self.Anchor0['z'] = 0.0
        self.Anchor0['r'] = 5.0
        
        self.Anchor1['name'] = 'Anchor1'
        self.Anchor1['color'] = 'g'
        self.Anchor1['x'] = 10.0
        self.Anchor1['y'] = 0.0
        self.Anchor1['z'] = 0.0
        self.Anchor1['r'] = 5.0
        
        self.Anchor2['name'] = 'Anchor2'
        self.Anchor2['color'] = 'b'
        self.Anchor2['x'] = 10.0
        self.Anchor2['y'] = 10.0
        self.Anchor2['z'] = 0.0
        self.Anchor2['r'] = 5.0
        
        self.index_in_pkg = 0
        self.uart_pkg = np.zeros(16, dtype=int, order='C')         # 新包缓存
        
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
        
        # 将 Matlabplotlib 2D 图像嵌入界面
        layout = self.ui_main.horizontalLayout_2D_Static                # <class 'PySide2.QtWidgets.QHBoxLayout'>
        
        self.canvas_2d_static = FigureCanvas(Figure())                  # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        layout.addWidget(self.canvas_2d_static)
        
        self.circle = plt.Circle((-30, 30), 20, color='b', alpha=0.5)
        
        self.axes_2d_static = self.canvas_2d_static.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_2d_static.add_artist(self.circle)
        
        self.axes_2d_static.grid(True)
        self.axes_2d_static.set_xlim(-150, 150)
        self.axes_2d_static.set_ylim(-150, 150)
        
        self._timer = self.canvas_2d_static.new_timer(50, [(self.update_2D_Dynamic, (), {})])
        self._timer.start()
        
        # t = np.linspace(0, 10, 501)
        # self.axes_2d_static.plot(t, np.tan(t), t, 20*t-100, "-", label='tanx_and_line', lw=1, markersize=10)
        # self.axes_2d_static.plot(t, -3*t, "-", label='-3t', lw=1)
        # self.axes_2d_static.plot(3, -125, "b.", label='point(3, -125)')
        # self.axes_2d_static.scatter(x=2, y=0, color='tab:blue', s=7000, label='ball', alpha=0.3, edgecolors='r', lw=1)
        # self.axes_2d_static.plot(3, 25, color='tab:blue', label='ball', alpha=1.0, lw=1)
        # matplotlib.pyplot.scatter(x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=<deprecated parameter>, edgecolors=None, *, plotnonfinite=False, data=None, **kwargs)
        # self.axes_2d_static.scatter(x=3, y=25, c='tab:blue', label='ball', alpha=0.5, lw=1, edgecolors='r')
        
        # self.axes_2d_static.scatter(x=0, y=0, c='tab:blue', label='ball', s=100, alpha=0.5, lw=1, edgecolors='r')
        
        # self.axes_2d_static.clear()
        # self.axes_2d_static.grid(True)
        # self.axes_2d_static.set_xlim(-150, 150)
        # self.axes_2d_static.set_ylim(-150, 150)
        
        self.axes_2d_static.plot([0],[0], c='g', marker="o",  markersize=10, alpha=0.2)
        self.axes_2d_static.plot([50],[50], c='g', marker="o",  markersize=60, alpha=0.2)
        
        self.update_2D_Dynamic()
        
    def update_2D_Dynamic(self):
        # print('update_2d_dynamic')
        self.axes_2d_static.clear()
        self.axes_2d_static.grid(True)
        self.axes_2d_static.set_xlim(-20, 20)
        self.axes_2d_static.set_ylim(-20, 20)
        
        self.update_Anchor(self.Anchor0)
        self.update_Anchor(self.Anchor1)
        self.update_Anchor(self.Anchor2)
        
        self.axes_2d_static.figure.canvas.draw()
        pass
        
    def update_Anchor(self, anchor):
        self.circle = plt.Circle((anchor['x'], anchor['y']), anchor['r'], color=anchor['color'], alpha=0.5, picker=5)
        self.axes_2d_static.add_artist(self.circle)
        pass
    
    def draw_Circle(self, x, y, r):
        pass
    
    def draw_Anchor(self, x, y, r, name=None):
        pass
    
    def draw_Tag_to_3_Anchor_(self, d1, d2, d3):
        pass
    
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
        self.axes_2d_static.clear()
        self.axes_2d_static.figure.canvas.draw()
        self.log('清空接收')
    
    def slot_dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
    
    def receive_port_data(self):
        port = self.port
        data_text = self.ui_main.plainTextEdit_Hex
        
        if(self.port.isopen):
            try:
                if(port.port.in_waiting > 0):           # inWaiting()
                    new_bytes = port.port.read()
                    new_str = new_bytes.hex()
                    new_bytes_0 = new_bytes[0]
                    # print(type(new_bytes_0), new_bytes_0)
                    # new_int = int.from_bytes(new_bytes_0, byteorder='big', signed=False)
                    
                    # print(type(new_int), new_int)
                    self.uart_pkg[self.index_in_pkg] = new_bytes_0
                    # # print('self.uart_pkg[self.index_in_pkg] = ', self.uart_pkg[self.index_in_pkg])
                    # print('hello')
                    
                    if(     ( 0 == self.index_in_pkg) and (0x6D != self.uart_pkg[self.index_in_pkg])
                        or  ( 1 == self.index_in_pkg) and (0x72 != self.uart_pkg[self.index_in_pkg])
                        or  ( 2 == self.index_in_pkg) and (0x02 != self.uart_pkg[self.index_in_pkg])
                        or  ( 3 == self.index_in_pkg) and (0x00 != self.uart_pkg[self.index_in_pkg])
                        or  (14 == self.index_in_pkg) and (0x0A != self.uart_pkg[self.index_in_pkg])
                        or  (15 == self.index_in_pkg) and (0x0D != self.uart_pkg[self.index_in_pkg]) ):
                        self.index_in_pkg = 0
                    else:
                        self.index_in_pkg += 1
                        if(self.index_in_pkg >= 16):
                            DL = self.uart_pkg[6]
                            DH = self.uart_pkg[7]
                            distance = (DH << 8) | DL
                            self.Anchor0['r'] = distance
                            
                            DL = self.uart_pkg[8]
                            DH = self.uart_pkg[9]
                            distance = (DH << 8) | DL
                            self.Anchor1['r'] = distance
                            
                            DL = self.uart_pkg[10]
                            DH = self.uart_pkg[11]
                            distance = (DH << 8) | DL
                            self.Anchor2['r'] = distance
                            
                            self.log('%s' %('r0: %03d, r1: %03d, r2: %03d' %(self.Anchor0['r'], self.Anchor1['r'], self.Anchor2['r'])))
                            
                            self.index_in_pkg = 0
                            pass
                        pass
                    
                    # print()
                    # print(type(new_bytes), new_bytes)
                    # print(type(new_str), new_str)
                    
                    # data_text.appendPlainText(new_str)                # 追加方式会导致每项换行
                    
                    data_text.moveCursor(QTextCursor.End)               # 手动在末尾插入
                    data_text.insertPlainText(new_str.upper() + ' ')
            except:
                pass
    
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
# idl.ui_main.MainWindow.addToolBar(NavigationToolbar(idl.canvas_2d_static.toolBar, app))

timer = QTimer()
timer.timeout.connect(idl.receive_port_data)
timer.start(0)

# idl.idl_rx_process_start()

app.exec_()