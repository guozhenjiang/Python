from PySide2.QtWidgets import QApplication, QComboBox, QTabWidget
from PySide2.QtGui import QTextCursor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QTextStream, QTimer, Signal, Slot
from lib_comport import *
from lib_comport_ComboBox import *

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
        Tag_t = {'name':'Tag', 'r0':0.0, 'r1':0.0, 'r2':0.0,'x':50, 'y':50, 'z':0.0}
        
        self.Anchor0 = Anchor_t.copy()
        self.Anchor1 = Anchor_t.copy()
        self.Anchor2 = Anchor_t.copy()
        
        self.Tag = Tag_t.copy()
        
        self.Anchor0['name'] = 'Anchor0'
        self.Anchor0['color'] = 'r'
        self.Anchor0['x'] = 0
        self.Anchor0['y'] = 0
        self.Anchor0['z'] = 0.0
        self.Anchor0['r'] = 50.0
        
        self.Anchor1['name'] = 'Anchor1'
        self.Anchor1['color'] = 'g'
        self.Anchor1['x'] = 300.0
        self.Anchor1['y'] = 0.0
        self.Anchor1['z'] = 0.0
        self.Anchor1['r'] = 100.0
        
        self.Anchor2['name'] = 'Anchor2'
        self.Anchor2['color'] = 'b'
        self.Anchor2['x'] = 0.0
        self.Anchor2['y'] = 300.0
        self.Anchor2['z'] = 0.0
        self.Anchor2['r'] = 80
        
        self.pkg_id = 0
        self.pkg_byte_id = 0
        self.uart_pkg = np.zeros(100, dtype=int, order='C')         # 新包缓存
        
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
        
        ui.comboBox_name_raw.deleteLater()  # 删掉 UI 生成的端口选择下拉框控件
        ui.comboBox_name = PortComboBox()   # 用自己重写的下拉框控件替换被删的
        ui.gridLayout_port_set_select.addWidget(ui.comboBox_name, 0, 1) # 添加到原来的布局框中相同位置
        
        # 将 Matlabplotlib 2D 图像嵌入界面
        layout = self.ui_main.horizontalLayout_2D_          # <class 'PySide2.QtWidgets.QHBoxLayout'>
        
        self.canvas_2d_matplotlib = FigureCanvas(Figure())  # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        layout.addWidget(self.canvas_2d_matplotlib)
        
        self.axes_2d_static = self.canvas_2d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_2d_static.grid(True)
        
        # str_item = str(self.Anchor0['x'])
        # newItem = QTabWidgetItem(str_item)
        # self.ui_main.tableWidget_DataInfo.setItem(0, 0, newItem)
        # print(str_item)
        # item = self.ui_main.tableWidget_DataInfo.item(0, 0)
        # print(type(item))
        # item.setTabText.setText('hello')
        # self.ui_main.tableWidget_DataInfo.item(0, 0).setItem('hello')
        # item = self.ui_main.tableWidget_DataInfo.setTabText(0, 0)
        # self.ui_main.tableWidget_DataInfo.setTabText(0, 0, 'hello')
        
        self.update_2d_matplotlib_limit()
        
        self.timer_2d_matplotlib = self.canvas_2d_matplotlib.new_timer(100, [(self.update_display, (), {})])
        self.timer_2d_matplotlib.start()
        
        # 将 Matlabplotlib 3D 图像嵌入界面
        layout = self.ui_main.horizontalLayout_3D_Matplotlib    # <class 'PySide2.QtWidgets.QHBoxLayout'>
        self.canvas_3d_matplotlib = FigureCanvas(Figure())      # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        layout.addWidget(self.canvas_3d_matplotlib)
        self.axes_3d_static = self.canvas_3d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_3d_static.grid(True)
        
        self.ui_main.tableWidget_DataInfo.setHorizontalHeaderLabels(['x', 'y', 'z'])
    
    def update_display(self):
        if(self.port.isopen):
            if('DongHan' == self.ui_main.comboBox_Mode.currentText()):
                self.update_display_DongHan()
                pass
            elif('WangZeKun' == self.ui_main.comboBox_Mode.currentText()):
                self.update_display_WangZeKun()
                pass
        pass
        
    def update_display_DongHan(self):
        self.clear_display_2d_matplotlib()
        
        self.draw_anchor_circle(self.Anchor0)
        self.draw_anchor_circle(self.Anchor1)
        self.draw_anchor_circle(self.Anchor2)
        
        self.draw_anchor_to_anchor_line(self.Anchor0, self.Anchor1)
        self.draw_anchor_to_anchor_line(self.Anchor0, self.Anchor2)
        self.draw_anchor_to_anchor_line(self.Anchor1, self.Anchor2)
        
        self.axes_2d_static.figure.canvas.draw()
        pass
        
    def update_display_WangZeKun(self):
        # self.clear_display_2d_matplotlib()
        
        self.draw_tag_point()
        self.axes_2d_static.figure.canvas.draw()
        pass
    
    def draw_ref_line(self):
        x_s = [100, 300, 300, 100, 100]
        y_s = [100, 100, 300, 300, 100]
        
        self.axes_2d_static.plot(x_s, y_s, '-', c='k', alpha=0.8, lw=1)
        pass
    
    def draw_tag_point(self):
        self.circle = plt.Circle((self.Tag['x'], self.Tag['y']), 3, color='c', ec='c', alpha=0.2, picker=5)
        self.axes_2d_static.add_artist(self.circle)
        pass
        
    def draw_anchor_circle(self, anchor):
        self.circle = plt.Circle((anchor['x'], anchor['y']), anchor['r'], color=anchor['color'], ec='c', alpha=0.5, picker=5)
        self.axes_2d_static.add_artist(self.circle)
        pass
        
    def draw_anchor_to_anchor_line(self, anchor_0, anchor_1):
        x0 = anchor_0['x']
        y0 = anchor_0['y']
        
        x1 = anchor_1['x']
        y1 = anchor_1['y']
        
        x_s = [x0, x1]
        y_s = [y0, y1]
        
        self.axes_2d_static.plot(x_s, y_s, '-', c='c', alpha=0.3, lw=0.5)
        pass
    
    def draw_anchor_point(self, anchor, color):
        circle = plt.Circle((anchor['x'], anchor['y']), radius=5, color=color, ec='c', alpha=1, picker=5)
        self.axes_2d_static.add_artist(circle)
        pass
    
    def draw_Tag_to_3_Anchor_(self, d1, d2, d3):
        pass
    
    def init_signal_slot(self):
        self.log('初始化 Signal Slot')
        ui = self.ui_main
        
        ui.comboBox_name.signal_PortComboBox_showPopup.connect(self.slot_PortComboBox_showPopup)
        ui.comboBox_name.currentTextChanged.connect(    lambda:self.slot_port_name())
        ui.comboBox_baud.currentTextChanged.connect(    lambda:self.slot_port_baud())
        ui.comboBox_byte.currentTextChanged.connect(    lambda:self.slot_port_byte())
        ui.comboBox_parity.currentTextChanged.connect(  lambda:self.slot_port_parity())
        ui.comboBox_stop.currentTextChanged.connect(    lambda:self.slot_port_stop())
        ui.checkBox_xonxoff.stateChanged.connect(       lambda:self.slot_port_xonxoff())
        ui.checkBox_rtscts.stateChanged.connect(        lambda:self.slot_port_rtscts())
        ui.checkBox_dsrdtr.stateChanged.connect(        lambda:self.slot_port_dsrdtr())
        ui.pushButton_open_close.clicked.connect(       lambda:self.slot_port_open_close())
        ui.pushButton_CleanReceive.clicked.connect(     lambda:self.slot_clean_receive())
        ui.pushButton_StartSend.clicked.connect(        lambda:self.slot_send())
        ui.tableWidget_DataInfo.itemChanged.connect(    lambda:self.slot_tableWidget_Anchor_changed())
        ui.comboBox_Mode.currentTextChanged.connect(    lambda:self.slot_mode_changed())
    
    def clear_display_2d_matplotlib(self):
        self.log('清除当前显示')
        self.axes_2d_static.clear()                             # 清除当前显示
        self.axes_2d_static.grid(True)                          # 显示网格
        self.axes_2d_static.set_xlim(self.x_min, self.x_max)    # 设置坐标轴显示范围
        self.axes_2d_static.set_ylim(self.y_min, self.y_max)
        # self.axes_2d_static.figure.canvas.draw()
        pass
    
    def slot_mode_changed(self):
        self.log('模式切换到 %s' %(self.ui_main.comboBox_Mode.currentText()))
        
        # 清除当前显示
        self.clear_display_2d_matplotlib()
        
        if('DongHan' == self.ui_main.comboBox_Mode.currentText()):
            pass
        elif('WangZeKun' == self.ui_main.comboBox_Mode.currentText()):
            # 绘制基站坐标点
            self.log('画坐标点')
            self.draw_anchor_point(self.Anchor0, 'r')
            self.draw_anchor_point(self.Anchor1, 'g')
            self.draw_anchor_point(self.Anchor2, 'b')
            
            # 绘制期望轨迹线
            self.draw_ref_line()
            pass
        pass
    
    def slot_PortComboBox_showPopup(self):
        self.log('扫描端口')
        port = self.port
        cmb = self.ui_main.comboBox_name
        
        port.name_last = cmb.currentText()
        cmb.clear()     # 会触发 Signal: ui.comboBox_name.currentTextChanged
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
        self.port.name = self.ui_main.comboBox_name.currentText()
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
        else:
            self.ui_main.pushButton_open_close.setText('打开端口')
            self.log('端口关闭')
    
    def slot_clean_receive(self):
        self.ui_main.plainTextEdit_Hex.clear()
        self.ui_main.plainTextEdit_Ascii.clear()
        self.clear_display_2d_matplotlib()
        self.axes_2d_static.figure.canvas.draw()
        
        self.pkg_byte_id = 0
        
        self.log('清空接收')
    
    def slot_send(self):
        if(self.port.isopen):
            send_str = self.ui_main.lineEdit_StartSend.text()
            # https://blog.csdn.net/whatday/article/details/97423901
            # print(send_str)
            # send_bytes = bytes(send_str, encoding='utf-8')
            # send_bytes = send_str.encode('hex')
            # send_bytes = codecs.encode(send_str, 'hex') #send_str.encode('hex')
            # send_bytes = send_str.codecs.encode('hex')
            send_bytes = bytes.fromhex(send_str)
            # print(send_bytes)
            # self.log(send_str)
            self.log('即将发送 %s' %(send_bytes))
            self.port.port.write(send_bytes)
            pass
        else:
            self.log('端口未打开！')
            pass
        pass
    
    def update_2d_matplotlib_limit(self):
        x_min = self.Anchor0['x']
        x_max = self.Anchor0['x']
        y_min = self.Anchor0['y']
        y_max = self.Anchor0['y']
        
        if(self.Anchor1['x'] < x_min):
            x_min = self.Anchor1['x']
        if(self.Anchor2['x'] < x_min):
            x_min = self.Anchor2['x']
        
        if(self.Anchor1['x'] > x_max):
            x_max = self.Anchor1['x']
        if(self.Anchor2['x'] > x_max):
            x_max = self.Anchor2['x']
        
        if(self.Anchor1['y'] < y_min):
            y_min = self.Anchor1['y']
        if(self.Anchor2['y'] < y_min):
            y_min = self.Anchor2['y']
        
        if(self.Anchor1['y'] > y_max):
            y_max = self.Anchor1['y']
        if(self.Anchor2['y'] > y_max):
            y_max = self.Anchor2['y']
        
        self.keep_out = 100
        
        self.x_min = x_min - self.keep_out
        self.x_max = x_max + self.keep_out
        self.y_min = y_min - self.keep_out
        self.y_max = y_max + self.keep_out
        self.axes_2d_static.set_xlim(self.x_min, self.x_max)
        self.axes_2d_static.set_ylim(self.y_min, self.y_max)
        pass
    
    def slot_tableWidget_Anchor_changed(self):
        
        # a0_x = float(self.ui_main.tableWidget_DataInfo.item(0, 0).text())
        # print(a0_x)
        
        self.Anchor0['x'] = float(self.ui_main.tableWidget_DataInfo.item(0, 0).text())
        self.Anchor0['y'] = float(self.ui_main.tableWidget_DataInfo.item(0, 1).text())
        self.Anchor0['z'] = float(self.ui_main.tableWidget_DataInfo.item(0, 2).text())
        
        self.Anchor1['x'] = float(self.ui_main.tableWidget_DataInfo.item(1, 0).text())
        self.Anchor1['y'] = float(self.ui_main.tableWidget_DataInfo.item(1, 1).text())
        self.Anchor1['z'] = float(self.ui_main.tableWidget_DataInfo.item(1, 2).text())
        
        self.Anchor2['x'] = float(self.ui_main.tableWidget_DataInfo.item(2, 0).text())
        self.Anchor2['y'] = float(self.ui_main.tableWidget_DataInfo.item(2, 1).text())
        self.Anchor2['z'] = float(self.ui_main.tableWidget_DataInfo.item(2, 2).text())
        
        self.update_2d_matplotlib_limit()
        
        pass
    
    def slot_dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
    
    def receive_port_data(self):
        if('debug_rx' == self.ui_main.comboBox_Mode.currentText()):
            self.receive_port_data_debug()
            pass
        elif(self.port.isopen):
            if('DongHan' == self.ui_main.comboBox_Mode.currentText()):
                self.receive_port_data_DongHan()
                pass
            elif('WangZeKun' == self.ui_main.comboBox_Mode.currentText()):
                self.receive_port_data_WangZeKun()
                pass
        pass
    
    def receive_port_data_DongHan(self):
        port = self.port
        data_text = self.ui_main.plainTextEdit_Hex
        
        if(self.port.isopen):
            try:
                if(port.port.in_waiting > 0):           # inWaiting()
                    new_bytes = port.port.read()
                    new_str = new_bytes.hex()
                    new_bytes_0 = new_bytes[0]
                    # print(type(new_bytes_0), new_bytes_0)
                    
                    self.uart_pkg[self.pkg_byte_id] = new_bytes_0
                    
                    if(     ( 0 == self.pkg_byte_id) and (0x6D != self.uart_pkg[self.pkg_byte_id])
                        or  ( 1 == self.pkg_byte_id) and (0x72 != self.uart_pkg[self.pkg_byte_id])
                        or  ( 2 == self.pkg_byte_id) and (0x02 != self.uart_pkg[self.pkg_byte_id])
                        or  ( 3 == self.pkg_byte_id) and (0x00 != self.uart_pkg[self.pkg_byte_id])
                        or  (14 == self.pkg_byte_id) and (0x0A != self.uart_pkg[self.pkg_byte_id])
                        or  (15 == self.pkg_byte_id) and (0x0D != self.uart_pkg[self.pkg_byte_id]) ):
                        self.pkg_byte_id = 0
                    else:
                        self.pkg_byte_id += 1
                        if(self.pkg_byte_id >= 16):
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
                            
                            self.pkg_byte_id = 0
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
    
    def receive_port_data_WangZeKun(self):
        port = self.port
        data_text = self.ui_main.plainTextEdit_Hex
        
        if(self.port.isopen):
            try:
                if(port.port.in_waiting > 0):
                    new_bytes = port.port.read()
                    # self.log('%02d : %s' %(self.pkg_byte_id, new_bytes))
                    new_str = new_bytes.hex()
                    new_bytes_0 = new_bytes[0]
                    # print(type(new_bytes_0), new_bytes_0)
                    
                    self.uart_pkg[self.pkg_byte_id] = new_bytes_0
                    
                    if(     ( 0 == self.pkg_byte_id) and (0xFF != self.uart_pkg[self.pkg_byte_id])
                        or  ( 1 == self.pkg_byte_id) and (0x02 != self.uart_pkg[self.pkg_byte_id])
                        or  ( 2 == self.pkg_byte_id) and (0x00 != self.uart_pkg[self.pkg_byte_id])
                        or  ( 3 == self.pkg_byte_id) and (0x04 != self.uart_pkg[self.pkg_byte_id]) ):
                        self.pkg_byte_id = 0
                    else:
                        self.pkg_byte_id += 1
                        if(self.pkg_byte_id >= 32):
                            X_H = self.uart_pkg[9]
                            X_L = self.uart_pkg[10]
                            Tag_x = (X_H << 8) | X_L
                            self.Tag['x'] = Tag_x
                            
                            Y_H = self.uart_pkg[11]
                            Y_L = self.uart_pkg[12]
                            Tag_y = (Y_H << 8) | Y_L
                            self.Tag['y'] = Tag_y
                            
                            R0_H = self.uart_pkg[13]
                            R0_L = self.uart_pkg[14]
                            r0 = (R0_H << 8) | R0_L
                            self.Tag['r0'] = r0
                            
                            R1_H = self.uart_pkg[15]
                            R1_L = self.uart_pkg[16]
                            r1 = (R1_H << 8) | R1_L
                            self.Tag['r1'] = r1
                            
                            R2_H = self.uart_pkg[17]
                            R2_L = self.uart_pkg[18]
                            r2 = (R2_H << 8) | R2_L
                            self.Tag['r2'] = r2
                            
                            # print('X:[0x%02X 0x%02X -> 0x%04X(%+ 6d)] Y:[0x%02X 0x%02X -> 0x%04X(%+ 6d)] D0:[0x%02X 0x%02X -> 0x%04X(%+ 6d)] D1:[0x%02X 0x%02X -> 0x%04X(%+ 6d)] D2:[0x%02X 0x%02X -> 0x%04X(%+ 6d)]'\
                            #         %(  X_H, X_L, Tag_x, Tag_x,\
                                        # Y_H, Y_L, Tag_y, Tag_y,\
                                        # R0_H, R0_L, r0, r0,\
                                        # R1_H, R1_L, r1, r1,\
                                        # R2_H, R2_L, r2, r2)   )
                            
                            # print('(%+ 6d, %+ 6d)  [D0:%+ 6d]  [D1:%+ 6d]  [D2:%+ 6d]' %(Tag_x, Tag_y, r0, r1, r2))
                            self.log('%s' %('(%+ 6d, %+ 6d)  [D0:%+ 6d]  [D1:%+ 6d]  [D2:%+ 6d]' %(Tag_x, Tag_y, r0, r1, r2)))
                            
                            self.pkg_byte_id = 0
                            
                    # print(type(new_bytes), new_bytes)
                    # print(type(new_str), new_str)
                    
                    # data_text.appendPlainText(new_str)                # 追加方式会导致每项换行
                    
                    data_text.moveCursor(QTextCursor.End)               # 手动在末尾插入
                    data_text.insertPlainText(new_str.upper() + ' ')
            except:
                pass
    
    def receive_port_data_debug(self):
        self.pkg_id += 1
        port = self.port
        
        if(port.isopen):
            try:
                num = port.port.in_waiting
                if(num > 0):
                    new_bytes = port.port.read(num)
                    # print(new_bytes)
                    print('% 6d-% 4dbyte: ' %(self.pkg_id, num), new_bytes)
                    
                    # new_str = new_bytes.hex()
                    
                    if(     (0xFF == new_bytes[0])
                       and  (0x02 == new_bytes[1])  ):
                        print('new_pkg')
                        pass
            except:
                pass
        pass
    
app = QApplication([])

idl = IndoorLocation()
idl.ui_main.show()

timer = QTimer()
timer.timeout.connect(idl.receive_port_data)
timer.start(1)

app.exec_()