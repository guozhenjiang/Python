from PySide2.QtWidgets import QApplication, QComboBox, QTabWidget
from PySide2.QtGui import QTextCursor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QTextStream, QTimer, Signal, Slot
from lib_comport import *
from lib_comport_ComboBox import *

import time
import datetime
import threading
import sys

# import pyglet

# Matplotlib 图像嵌入
import matplotlib
from matplotlib.pyplot import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import matplotlib.pyplot as plt

import struct

import copy


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

class Anchor():
    x = 0
    y = 0
    z = 0
    
    def __init__(self):
        pass

class Tag():
    x = 0
    y = 0
    z = 0
    
    stamp = ''
    idx = 0
    raw_data = b''
    
    d0 = 0
    d1 = 0
    d2 = 0
    
    rssi_a0 = 0
    rssi_a1 = 0
    rssi_a2 = 0
    
    def __init__(self):
        pass

class IndoorLocation(QObject):
    anchor0 = Anchor()
    anchor1 = Anchor()
    anchor2 = Anchor()
    tag = Tag()
    
    tags = []   # 存储接收到的每个点
    auto_drawing_idx = 0
    drawing_auto = True
    stamp_record_start = 0
    
    # 实例化
    def __init__(self):
        self.name = 'IDL'
        
        self.anchor0.x = 0
        self.anchor0.y = 0
        self.anchor0.z = 0.0
        
        self.anchor1.x = 300.0
        self.anchor1.y = 0.0
        self.anchor1.z = 0.0
        
        self.anchor2.x = 0.0
        self.anchor2.y = 300.0
        self.anchor2.z = 0.0
        
        self.pkg_byte_id = 0
        self.uart_pkg = np.zeros(100, dtype=int, order='C')         # 新包缓存
        
        self.enter_qtimer_gap = 0
        self.enter_qtimer_stamp = time.perf_counter()
        self.enter_qtimer_stamp_last = self.enter_qtimer_stamp
        
        self.read_serial_gap = 0
        self.read_serial_stamp = time.perf_counter()
        self.read_serial_stamp_last = self.read_serial_stamp
        
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
        # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 2020-04-17 14:21:40
        
        # print(time.perf_counter(), ' --- ', time.process_time())
        self.log_stamp = time.perf_counter()    # time.clock()  time.process_time()
        log_stamp_det = self.log_stamp - self.log_stamp_last
        self.log_stamp_last = self.log_stamp
        
        if(log_stamp_det > 0.1):
            new_line = ''   #'\r\n'
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
        
        ui.action_ViewSet.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Set, ui.action_ViewSet.isChecked()))
        ui.action_ViewLog.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Log, ui.action_ViewLog.isChecked()))
        ui.action_ViewHex.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Hex, ui.action_ViewHex.isChecked()))
        
        ui.comboBox_name_raw.deleteLater()  # 删掉 UI 生成的端口选择下拉框控件
        ui.comboBox_name = PortComboBox()   # 用自己重写的下拉框控件替换被删的
        ui.gridLayout_port_set_select.addWidget(ui.comboBox_name, 0, 1) # 添加到原来的布局框中相同位置
        
        # 将 Matlabplotlib 2D 图像嵌入界面
        layout = self.ui_main.horizontalLayout_2D_          # <class 'PySide2.QtWidgets.QHBoxLayout'>
        
        self.canvas_2d_matplotlib = FigureCanvas(Figure())  # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        layout.addWidget(self.canvas_2d_matplotlib)
        
        self.axes_2d_static = self.canvas_2d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_2d_static.grid(True)
        
        # str_item = str(self.anchor0.x)
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
        
        # self.timer_2d_matplotlib = self.canvas_2d_matplotlib.new_timer(100, [(self.update_display, (), {})])
        # self.timer_2d_matplotlib.start()
        
        self.ui_main.horizontalSlider_Graphic.setRange(0, 0)
        self.ui_main.horizontalSlider_Graphic.setSingleStep(1)
        
        # 将 Matlabplotlib 3D 图像嵌入界面
        layout = self.ui_main.horizontalLayout_3D_Matplotlib    # <class 'PySide2.QtWidgets.QHBoxLayout'>
        self.canvas_3d_matplotlib = FigureCanvas(Figure())      # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        layout.addWidget(self.canvas_3d_matplotlib)
        self.axes_3d_static = self.canvas_3d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_3d_static.grid(True)
        
        self.ui_main.tableWidget_DataInfo.setHorizontalHeaderLabels(['x', 'y', 'z'])
        
        self.slot_mode_changed()
    
    def init_signal_slot(self):
        self.log('初始化 Signal Slot')
        ui = self.ui_main
        
        ui.comboBox_name.signal_PortComboBox_showPopup.connect(self.slot_PortComboBox_showPopup)
        ui.comboBox_name.currentTextChanged.connect(            lambda:self.slot_port_name())
        ui.comboBox_baud.currentTextChanged.connect(            lambda:self.slot_port_baud())
        ui.comboBox_byte.currentTextChanged.connect(            lambda:self.slot_port_byte())
        ui.comboBox_parity.currentTextChanged.connect(          lambda:self.slot_port_parity())
        ui.comboBox_stop.currentTextChanged.connect(            lambda:self.slot_port_stop())
        ui.checkBox_xonxoff.stateChanged.connect(               lambda:self.slot_port_xonxoff())
        ui.checkBox_rtscts.stateChanged.connect(                lambda:self.slot_port_rtscts())
        ui.checkBox_dsrdtr.stateChanged.connect(                lambda:self.slot_port_dsrdtr())
        ui.pushButton_open_close.clicked.connect(               lambda:self.slot_port_open_close())
        ui.pushButton_CleanReceive.clicked.connect(             lambda:self.slot_clean_receive())
        ui.pushButton_StartSend.clicked.connect(                lambda:self.slot_send())
        ui.tableWidget_DataInfo.itemChanged.connect(            lambda:self.slot_tableWidget_Anchor_changed())
        ui.comboBox_Mode.currentTextChanged.connect(            lambda:self.slot_mode_changed())
        ui.pushButton_StartRecord.clicked.connect(              lambda:self.slot_start_record())
        ui.horizontalSlider_Graphic.sliderPressed.connect(      lambda:self.slot_graphic_slider_pressed())
        ui.horizontalSlider_Graphic.sliderReleased.connect(     lambda:self.slot_graphic_slider_released())
        ui.horizontalSlider_Graphic.valueChanged.connect(       lambda:self.slot_graphic_slider_changed())
        
    
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
        circle = plt.Circle((self.tag.x, self.tag.y), 3, color='c', ec='c', alpha=0.8, picker=5)
        self.axes_2d_static.add_artist(circle)
    
    def draw_circle(self, x, y, r, c):
        circle = plt.Circle((x, y), r, color=c, ec='c', alpha=0.2, picker=5)
        self.axes_2d_static.add_artist(circle)
    
    def draw_distance_circles(self):
        self.draw_circle(self.anchor0.x, self.anchor0.y, self.tag.d0, 'r')
        self.draw_circle(self.anchor1.x, self.anchor1.y, self.tag.d1, 'g')
        self.draw_circle(self.anchor2.x, self.anchor2.y, self.tag.d2, 'b')
    
    def draw_rssi_circles(self):
        # self.draw_circle(self.anchor0.x, self.anchor0.y, self.tag.rssi_a0, 'gray')
        # self.draw_circle(self.anchor1.x, self.anchor1.y, self.tag.rssi_a1, 'gray')
        # self.draw_circle(self.anchor2.x, self.anchor2.y, self.tag.rssi_a2, 'gray')
        
        self.draw_circle(self.anchor0.x, self.anchor0.y, 100, 'gray')
        self.draw_circle(self.anchor1.x, self.anchor1.y, 100, 'gray')
        self.draw_circle(self.anchor2.x, self.anchor2.y, 100, 'gray')
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
    
    def draw_anchor_points(self):
        circle = plt.Circle((self.anchor0.x, self.anchor0.y), radius=5, color='r', ec='c', alpha=1, picker=5)
        self.axes_2d_static.add_artist(circle)
        circle = plt.Circle((self.anchor1.x, self.anchor1.y), radius=5, color='g', ec='c', alpha=1, picker=5)
        self.axes_2d_static.add_artist(circle)
        circle = plt.Circle((self.anchor2.x, self.anchor2.y), radius=5, color='b', ec='c', alpha=1, picker=5)
        self.axes_2d_static.add_artist(circle)
    
    def draw_Tag_to_3_Anchor_(self, d1, d2, d3):
        pass
    
    def clear_display_2d_matplotlib(self):
        # self.log('清除当前显示')
        self.axes_2d_static.clear()                             # 清除当前显示
        self.axes_2d_static.grid(True)                          # 显示网格
        self.axes_2d_static.set_xlim(self.x_min, self.x_max)    # 设置坐标轴显示范围
        self.axes_2d_static.set_ylim(self.y_min, self.y_max)
    
    def slot_mode_changed(self):
        self.log('模式切换到 %s' %(self.ui_main.comboBox_Mode.currentText()))
        
        if('debug_rx' == self.ui_main.comboBox_Mode.currentText()):
            self.clear_display_2d_matplotlib()
            self.draw_anchor_points()
            self.draw_distance_circles()
            self.axes_2d_static.figure.canvas.draw()
            pass
        
        elif('DongHan' == self.ui_main.comboBox_Mode.currentText()):
            self.clear_display_2d_matplotlib()
            self.draw_anchor_points()
            self.axes_2d_static.figure.canvas.draw()
            pass
        elif('WangZeKun' == self.ui_main.comboBox_Mode.currentText()):
            self.clear_display_2d_matplotlib()
            self.draw_anchor_points()
            self.draw_ref_line()
            self.axes_2d_static.figure.canvas.draw()
            pass
        else:
            pass
    
    def slot_start_record(self):
        self.tags.clear()
        self.auto_drawing_idx = 0
        self.stamp_record_start = time.perf_counter()
        self.ui_main.horizontalSlider_Graphic.setValue(0)
        self.ui_main.horizontalSlider_Graphic.setRange(0, 0)
        self.ui_main.plainTextEdit_Hex.clear()
    
    def slot_graphic_slider_pressed(self):
        self.drawing_auto = False
    
    def slot_graphic_slider_released(self):
        self.drawing_auto = True
        self.auto_drawing_idx = self.ui_main.horizontalSlider_Graphic.value()
    
    def slot_graphic_slider_changed(self):
        idx = self.ui_main.horizontalSlider_Graphic.value()
        if not self.drawing_auto:
            if idx < len(self.tags):
                self.clear_display_2d_matplotlib()
                self.draw_a_pkg(idx)
                self.axes_2d_static.figure.canvas.draw()
    
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
        
        self.slot_mode_changed()
        
        self.port.read_id = 0
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
        x_min = self.anchor0.x
        x_max = self.anchor0.x
        y_min = self.anchor0.y
        y_max = self.anchor0.y
        
        if(self.anchor1.x < x_min):
            x_min = self.anchor1.x
        if(self.anchor2.x < x_min):
            x_min = self.anchor2.x
        
        if(self.anchor1.x > x_max):
            x_max = self.anchor1.x
        if(self.anchor2.x > x_max):
            x_max = self.anchor2.x
        
        if(self.anchor1.y < y_min):
            y_min = self.anchor1.y
        if(self.anchor2.y < y_min):
            y_min = self.anchor2.y
        
        if(self.anchor1.y > y_max):
            y_max = self.anchor1.y
        if(self.anchor2.y > y_max):
            y_max = self.anchor2.y
        
        self.keep_out = 200
        
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
        
        self.anchor0.x = float(self.ui_main.tableWidget_DataInfo.item(0, 0).text())
        self.anchor0.y = float(self.ui_main.tableWidget_DataInfo.item(0, 1).text())
        self.anchor0.z = float(self.ui_main.tableWidget_DataInfo.item(0, 2).text())
        
        self.anchor1.x = float(self.ui_main.tableWidget_DataInfo.item(1, 0).text())
        self.anchor1.y = float(self.ui_main.tableWidget_DataInfo.item(1, 1).text())
        self.anchor1.z = float(self.ui_main.tableWidget_DataInfo.item(1, 2).text())
        
        self.anchor2.x = float(self.ui_main.tableWidget_DataInfo.item(2, 0).text())
        self.anchor2.y = float(self.ui_main.tableWidget_DataInfo.item(2, 1).text())
        self.anchor2.z = float(self.ui_main.tableWidget_DataInfo.item(2, 2).text())
        
        self.update_2d_matplotlib_limit()
        
        self.slot_mode_changed()
        
        pass
    
    def slot_dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
    
    def receive_port_data(self):
        if('WangZeKun' == self.ui_main.comboBox_Mode.currentText()):
            self.receive_port_data_WangZeKun()
            pass
        
        elif('DongHan' == self.ui_main.comboBox_Mode.currentText()):
            if(self.port.isopen):
                self.receive_port_data_DongHan()
    
    def receive_port_data_DongHan(self):
        port = self.port
        data_text = self.ui_main.plainTextEdit_Hex
        
        if(self.port.isopen):
            try:
                if(port.port.in_waiting > 0):           # inWaiting()
                    new_bytes = port.port.read()
                    str_new_pkg = new_bytes.hex()
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
                            
                            self.log('%s' %('d0: %03d, d1: %03d, d2: %03d' %(self.Anchor0['r'], self.Anchor1['r'], self.Anchor2['r'])))
                            
                            self.pkg_byte_id = 0
                            pass
                        pass
                    
                    # print()
                    # print(type(new_bytes), new_bytes)
                    # print(type(str_new_pkg), str_new_pkg)
                    
                    # data_text.appendPlainText(str_new_pkg)                # 追加方式会导致每项换行
                    
                    data_text.moveCursor(QTextCursor.End)               # 手动在末尾插入
                    data_text.insertPlainText(str_new_pkg.upper() + ' ')
            except:
                pass
    
    def receive_port_data_WangZeKun(self):
        port = self.port
        data_text = self.ui_main.plainTextEdit_Hex
        
        self.enter_qtimer_stamp = time.perf_counter()           # 测量读取时间间隔 time.perf_counter() 返回浮点数 表示程序持续运行的秒数
        self.enter_qtimer_gap = self.enter_qtimer_stamp - self.enter_qtimer_stamp_last
        self.enter_qtimer_stamp_last = self.enter_qtimer_stamp
        rx_cache_len = len(port.rx_cache)
        
        # print(  '\r\n % 12.6fs after:%10.3fms rx:%03dB ' %(\
        #         self.enter_qtimer_stamp,
        #         (self.enter_qtimer_gap * 1000),
        #         rx_cache_len),
        #         end='' )
        
        if port.isopen and rx_cache_len<32:
            try:
                num = port.port.in_waiting
                
                if(num > 0):
                    # new_bytes = b'\xFF\x02\x00\x04\x00\x00\x00\x00\x00\x00\x09\x00\x10\x01\x15\x01\x16\x01\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAA\x55'
                    new_bytes = port.port.read(num)                 # 读取串口接收缓冲区的数据 读到的类型是 bytes
                    port.rx_cache += new_bytes                      # 添加到串口接收缓存中
                    rx_cache_len = len(port.rx_cache)
                    port.read_id += 1                               # read_id 端口打开后第几次读取
                    
                    self.read_serial_stamp = time.perf_counter()
                    self.read_serial_gap = self.read_serial_stamp - self.read_serial_stamp_last
                    self.read_serial_stamp_last = self.read_serial_stamp
                    
                    # print(  'after[%10.3f]ms read[%03d]B rx:%03dB ' %(\
                    #         (self.read_serial_gap * 1000),
                    #         num,
                    #         rx_cache_len),
                    #         end='' )
                    
                    while (len(port.rx_cache) >= 32):                 # 至少收到了一个包
                        if((0xFF == port.rx_cache[0]) and (0x02 == port.rx_cache[1])):
                            # 处理一个包
                            new_pkg = port.rx_cache[0:32]
                            port.rx_cache = port.rx_cache[32:]  # 移除已处理部分
                            
                            self.tag.stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            self.tag.stamp += ' %12.6f' %(time.perf_counter() - self.stamp_record_start)
                            self.tag.raw_data = new_pkg
                            self.tag.x = int(np.int16((new_pkg[9]  << 8) | new_pkg[10]))
                            self.tag.y = int(np.int16((new_pkg[11] << 8) | new_pkg[12]))
                            self.tag.d0 = (new_pkg[13] << 8) | new_pkg[14]
                            self.tag.d1 = (new_pkg[15] << 8) | new_pkg[16]
                            self.tag.d2 = (new_pkg[17] << 8) | new_pkg[18]
                            self.tag.rssi_a0 = int(np.int16((new_pkg[19] << 8) | new_pkg[20]))
                            self.tag.rssi_a1 = int(np.int16((new_pkg[21] << 8) | new_pkg[22]))
                            self.tag.rssi_a2 = int(np.int16((new_pkg[23] << 8) | new_pkg[24]))
                            
                            # !!! 这里必须使用 copy 否则缓存的数据总是最后一个包 !!!
                            # ref: https://www.iteye.com/blog/greybeard-1442259
                            # self.tags.append(copy.copy(self.tag))
                            self.tags.append(copy.deepcopy(self.tag))
                            
                            if self.drawing_auto:
                                self.ui_main.horizontalSlider_Graphic.setRange(0, len(self.tags))
                            
                            str_pkg_info = ''
                            str_pkg_info += ' P(%+3d, %+3d)' %(self.tag.x, self.tag.y)
                            str_pkg_info += ' D(%3d, %3d, %3d)' %(self.tag.d0, self.tag.d1, self.tag.d2)
                            str_pkg_info += ' R(%+3d, %+3d, %+3d)' %(self.tag.rssi_a0, self.tag.rssi_a1, self.tag.rssi_a2)
                            
                            str_new_pkg_hex = ''
                            
                            for b in new_pkg:
                                str_new_pkg_hex += ' %02X' %(b)
                            
                            str_new_pkg = self.tag.stamp
                            str_new_pkg += str_pkg_info
                            str_new_pkg += str_new_pkg_hex
                            
                            data_text.appendPlainText(str_new_pkg)
                            
                            # self.log(   '[% 8.3fs][id:% 8d][+% 4dB = % 4dB] => (% 4d, % 4d) [% 4d, % 4d, % 4d] [% 4dB]'\
                            #             %(  gap,
                            #                 port.read_id,
                            #                 num,
                            #                 len(port.rx_cache),
                            #                 self.tag.x,
                            #                 self.tag.y,
                            #                 self.Tag['d0'],
                            #                 self.Tag['d1'],
                            #                 self.Tag['d2'],
                            #                 len(port.rx_cache)  )   )
                        else:
                            self.log('%s' %(port.rx_cache))
                            print('finding_header...')
                            port.rx_cache = port.rx_cache[1:]       # 重新对其帧头
            except Exception as e:
                print('发生异常:')
                print(e)
    
    def draw_a_pkg(self, idx):
        # 显示解析后的包信息
        str_pkg_info = ''
        
        if idx < len(self.tags):
            tag_pkg = self.tags[idx]
            
            str_pkg_info += tag_pkg.stamp
            str_pkg_info += ' P(%+3d, %+3d)' %(tag_pkg.x, tag_pkg.y)
            str_pkg_info += ' D(%3d, %3d, %3d)' %(tag_pkg.d0, tag_pkg.d1, tag_pkg.d2)
            str_pkg_info += ' R(%+3d, %+3d, %+3d)' %(tag_pkg.rssi_a0, tag_pkg.rssi_a1, tag_pkg.rssi_a2)
            # print('设置包信息', str_pkg_info, time.time())
            self.ui_main.lineEdit_PkgInfo.setText(str_pkg_info)
            
            # # 开始图形化
            # self.clear_display_2d_matplotlib()
            
            # draw tag_pkg point
            circle = plt.Circle((tag_pkg.x, tag_pkg.y), 3, color='c', ec='c', alpha=0.8, picker=5)
            self.axes_2d_static.add_artist(circle)
            
            # draw anchor points
            circle = plt.Circle((self.anchor0.x, self.anchor0.y), radius=5, color='r', ec='c', alpha=1, picker=5)
            self.axes_2d_static.add_artist(circle)
            circle = plt.Circle((self.anchor1.x, self.anchor1.y), radius=5, color='g', ec='c', alpha=1, picker=5)
            self.axes_2d_static.add_artist(circle)
            circle = plt.Circle((self.anchor2.x, self.anchor2.y), radius=5, color='b', ec='c', alpha=1, picker=5)
            self.axes_2d_static.add_artist(circle)
            
            # draw distance circles
            circle = plt.Circle((self.anchor0.x, self.anchor0.y), tag_pkg.d0, color='r', ec='c', alpha=0.2, picker=5)
            self.axes_2d_static.add_artist(circle)
            circle = plt.Circle((self.anchor1.x, self.anchor1.y), tag_pkg.d1, color='g', ec='c', alpha=0.2, picker=5)
            self.axes_2d_static.add_artist(circle)
            circle = plt.Circle((self.anchor2.x, self.anchor2.y), tag_pkg.d2, color='b', ec='c', alpha=0.2, picker=5)
            self.axes_2d_static.add_artist(circle)
            
            # # draw rssi circle
            # circle = plt.Circle((self.anchor0.x, self.anchor0.y), tag_pkg.d0, color='gray', ec='c', alpha=0.2, picker=5)
            # self.axes_2d_static.add_artist(circle)
            # circle = plt.Circle((self.anchor1.x, self.anchor1.y), tag_pkg.d1, color='gray', ec='c', alpha=0.2, picker=5)
            # self.axes_2d_static.add_artist(circle)
            # circle = plt.Circle((self.anchor2.x, self.anchor2.y), tag_pkg.d2, color='gray', ec='c', alpha=0.2, picker=5)
            # self.axes_2d_static.add_artist(circle)
            
            circle = plt.Circle((self.anchor0.x, self.anchor0.y), 100, color='gray', ec='c', alpha=0.2, picker=5)
            self.axes_2d_static.add_artist(circle)
            circle = plt.Circle((self.anchor1.x, self.anchor1.y), 100, color='gray', ec='c', alpha=0.2, picker=5)
            self.axes_2d_static.add_artist(circle)
            circle = plt.Circle((self.anchor2.x, self.anchor2.y), 100, color='gray', ec='c', alpha=0.2, picker=5)
            self.axes_2d_static.add_artist(circle)
            
            # self.axes_2d_static.figure.canvas.draw()
        
    
    def update_graphic(self):
        if self.auto_drawing_idx < len(self.tags):
            # 取出数据包
            if self.drawing_auto and self.port.isopen:
                
                # 开始图形化
                self.clear_display_2d_matplotlib()
                self.draw_a_pkg(self.auto_drawing_idx)
                self.axes_2d_static.figure.canvas.draw()
                self.ui_main.horizontalSlider_Graphic.setValue(self.auto_drawing_idx)
                
                self.auto_drawing_idx += 1

if __name__ == '__main__':
    app = QApplication([])

    idl = IndoorLocation()
    idl.ui_main.show()

    timer_SerialRx = QTimer()
    timer_SerialRx.timeout.connect(idl.receive_port_data)
    timer_SerialRx.start(0)

    timer_UpdateGraphic = QTimer()
    timer_UpdateGraphic.timeout.connect(idl.update_graphic)
    timer_UpdateGraphic.start(100)

    sys.exit(app.exec_())