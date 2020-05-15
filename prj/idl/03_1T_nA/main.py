from PySide2 import QtGui, QtWidgets, QtCore

from PySide2.QtWidgets import QApplication, QComboBox, QTabWidget, QTableWidgetItem, QFileDialog
from PySide2.QtGui import QTextCursor, QTextFormat, QBrush, QColor
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
import csv


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


def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

# 基站
class Anchor():
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
    
    # 显示基站信息
    def show(self):
        print('A%02d(%+4d, %+4d, %+4d)' %(self.id, self.x, self.y, self.z))

# 标签
class Tag():
    def __init__(self):
        super().__init__()
        self.id = 0      # 便签编号
        self.d = []      # 标签和基站的距离
        self.r = []      # 标签和基站的信号强度
        self.x = 0
        self.y = 0
        self.z = 0
'''
    record 1T3A:
        stamp(2020-05-14 16:30:31.247),
        tag[(x0, y0, z0)],
        distance(d0, d1, d2)
        rssi(r0, r1, r2)
        pkg( FF 02 ...),
        anchor[(x0, y0, z0), (x1, y1, z1), (x2, y2, z2)]
'''

class Record():
    def __init__(self):
        self.recording = False
        self.start()
    
    def start(self):
        self.len = 0
        self.record = ''
    
class Pkg_WZK_1T3A():
    '''
    00 01 02 03 04 05 06 07 08 09  10  11  12  13   14   15   16   17   18   19        20        21        22        23        24        25 26 27 28 29 30 31
    FF 02 XX XX XX XX XX XX XX x_H x_L y_H y_L d0_H d0_L d1_H d1_L d2_H d2_L rssi_a0_H rssi_a0_L rssi_a1_H rssi_a1_L rssi_a2_H rssi_a2_L XX XX XX XX XX XX XX
    (x, y)                          标签坐标
    (d0, d1, d2)                    标签到 3 个基站的距离 单位 cm
    (rssi_a0, rssi_a1, rssi_a2)     便签到三个基站的信号强度
    '''
    def __init__(self):
        super().__init__()
        self.len = 32               # 包长
        self.anchor_num = 3         # 单个数据包种有多少个基站
        self.tag_num = 1            # 包中标签个数
        self.tags = []              # 当前包中的标签信息
        self.info_str = ''          # 记录到文件的字符串
        
        self.info_stamp = ''        # 时间戳
        self.info_tag = ''          # 标签坐标
        self.info_distance = ''     # 标签到基站的距离
        self.info_rssi = ''         # 标签到基站的信号强度
        self.info_pkg = ''          # 串口收到的数据包
    
    def update(self, raw_bytes):
        if (0xFF == raw_bytes[0]) and (0x02 == raw_bytes[1]):
            # 解析信息值
            for i in range(self.tag_num):
                self.tags.append(Tag())
                self.tags[i].x = int(np.int16((raw_bytes[9 + 4*i + 0]  << 8) | raw_bytes[9 + 4*i + 1]))
                self.tags[i].y = int(np.int16((raw_bytes[9 + 4*i + 2]  << 8) | raw_bytes[9 + 4*i + 3]))
                
                for j in range(self.anchor_num):
                    self.tags[i].d.append((raw_bytes[13 + 2*j + 0] << 8) | raw_bytes[13 + 2*j + 1])
                    self.tags[i].r.append(int(np.int16((raw_bytes[19 + 2*j + 0] << 8) | raw_bytes[19 + 2*j + 1])) / 100)
            
            # 更新信息字符串
            self.info_stamp = time_stamp_ms()
            
            for i in range(self.tag_num):
                # 坐标
                self.info_tag = ' T(%4d, %4d)' %(self.tags[i].x, self.tags[i].y)
                
                # 距离
                self.info_distance = ' D('
                for j in range(self.anchor_num):
                    self.info_distance += '%3d' %(self.tags[i].d[j])
                    if j != self.anchor_num-1:
                        self.info_distance += ', '
                self.info_distance += ')'
                
                # 信号强度
                self.info_rssi = ' R('
                for j in range(self.anchor_num):
                    self.info_rssi += '%3d' %(self.tags[i].r[j])
                    if j != self.anchor_num-1:
                        self.info_rssi += ', '
                self.info_rssi += ')'
                
            # 原始包
            self.info_pkg = ''
            for b in  raw_bytes:
                self.info_pkg += ' %02X' %(b)
            
            self.info_str = self.info_stamp + self.info_tag + self.info_distance + self.info_rssi + self.info_pkg
            
            return True
        else:
            return False

class IndoorLocation(QObject):
    anchors = []
    anchors.append(Anchor(0, 0, 0, 200))
    anchors.append(Anchor(1, 0, 200, 0))
    anchors.append(Anchor(2, 200, 0, 0))
    
    for anchor in anchors:
        anchor.show()
    
    pkg_wzk = Pkg_WZK_1T3A()
    pkgs = []
    
    drawing_idx = 0
    drawing_auto = True
    stamp_record_start = 0
    
    def __init__(self):
        self.record = Record()                              # 数据记录
        self.ui_cnt_recording = 0
        
        log_file_loc = './log.txt'
        print('以读写打开 %s' %(log_file_loc))
        log_file = QFile(log_file_loc)
        log_file.open(QFile.ReadWrite | QFile.Truncate)
        
        self.log_stamp_last = time.perf_counter()
        self.log_stream = QTextStream(log_file)
        self.log_stream.setCodec('UTF-8')
        self.log_stream.seek(log_file.size())
        
        file_loc_ui_main = './ui_main_1T_nA.ui'
        self.ui_main = QUiLoader().load(file_loc_ui_main)
        self.log('载入 %s' %(file_loc_ui_main))
        self.port = Port()                              # 实例化
        
        # 初始化
        self.init_ui()
        
        original_size = self.ui_main.dockWidget_Hex.size()
        # print()
        # print('************************')
        # print(type(original_size))
        # print(original_size)
        # print(original_size.width(), original_size.height())
        # print('************************')
        # print()
        
        self.ui_main.dockWidget_Hex.resize(100, original_size.height())     # resize 对 DockWidget 无效
        
        for i in range(len(self.anchors)):
            self.ui_main.tableWidget_DataInfo.setItem(i, 0, QTableWidgetItem(str(self.anchors[i].x)))
            self.ui_main.tableWidget_DataInfo.setItem(i, 1, QTableWidgetItem(str(self.anchors[i].y)))
            self.ui_main.tableWidget_DataInfo.setItem(i, 2, QTableWidgetItem(str(self.anchors[i].z)))
        
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
        print(new_log_str)
        pass
    
    def init_ui(self):
        self.log('初始化 UI')
        ui = self.ui_main
        
        # self.ui_main.setWindowIcon(QtGui.QPixmap(r'.\ico\map_128x128.ico'))
        # self.ui_main.setWindowIcon(QtGui.QPixmap(r'.\ico\location_1'))
        # self.ui_main.setWindowIcon(QtGui.QPixmap(r'.\ico\location_2'))
        self.ui_main.setWindowIcon(QtGui.QPixmap(r'.\ico\social_media'))
        
        self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_1'))
        self.ui_main.pushButton_RecordSave.setIcon(QtGui.QPixmap(r'.\ico\save'))
        self.ui_main.pushButton_RecordPlay.setIcon(QtGui.QPixmap(r'.\ico\play'))
        self.ui_main.pushButton_RecordDelete.setIcon(QtGui.QPixmap(r'.\ico\delete'))
        self.ui_main.pushButton_RecordDir.setIcon(QtGui.QPixmap(r'.\ico\open_dir'))
        self.ui_main.pushButton_RecordRefresh.setIcon(QtGui.QPixmap(r'.\ico\refresh'))
        
        ui.comboBox_name_raw.deleteLater()  # 删掉 UI 生成的端口选择下拉框控件
        ui.comboBox_name = PortComboBox()   # 用自己重写的下拉框控件替换被删的
        # ui.comboBox_name.setMaximumWidth(150)
        
        ui.gridLayout_port_set_select.addWidget(ui.comboBox_name, 0, 1) # 添加到原来的布局框中相同位置
        
        # 将 Matlabplotlib 2D 图像嵌入界面
        layout = self.ui_main.horizontalLayout_2D_          # <class 'PySide2.QtWidgets.QHBoxLayout'>
        
        self.canvas_2d_matplotlib = FigureCanvas(Figure())  # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        layout.addWidget(self.canvas_2d_matplotlib)
        
        self.axes_2d_static = self.canvas_2d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_2d_static.grid(True)
        
        self.update_2d_matplotlib_limit()
        
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
        
        ui.action_ViewSet.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Set, ui.action_ViewSet.isChecked()))
        ui.action_ViewLog.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Log, ui.action_ViewLog.isChecked()))
        ui.action_ViewHex.changed.connect(  lambda:self.slot_dock_show_hide(ui.dockWidget_Hex, ui.action_ViewHex.isChecked()))
        ui.action_ViewInfo.changed.connect( lambda:self.slot_dock_show_hide(ui.dockWidget_Info, ui.action_ViewInfo.isChecked()))
        
        ui.dockWidget_Set.visibilityChanged.connect(    lambda visable:self.slot_win_set_visibility_changed(visable))
        ui.dockWidget_Log.visibilityChanged.connect(    lambda visable:self.slot_win_log_visibility_changed(visable))
        ui.dockWidget_Hex.visibilityChanged.connect(    lambda visable:self.slot_win_hex_visibility_changed(visable))
        ui.dockWidget_Info.visibilityChanged.connect(   lambda visable:self.slot_win_info_visibility_changed(visable))
        
        ui.comboBox_name.signal_PortComboBox_showPopup.connect(self.slot_PortComboBox_showPopup)
        ui.comboBox_name.currentTextChanged.connect(    lambda:self.slot_port_name())
        
        ui.comboBox_name.activated.connect(             lambda:self.slot_port_name_activated())
        ui.comboBox_name.currentIndexChanged.connect(   lambda idx:self.slot_port_name_currentIndexChanged(idx))
        ui.comboBox_name.editTextChanged.connect(       lambda:self.slot_port_name_editTextChanged())
        ui.comboBox_name.highlighted.connect(           lambda idx:self.slot_port_name_highlighted(idx))
        ui.comboBox_name.textActivated.connect(         lambda:self.slot_port_name_textActivated())
        ui.comboBox_name.textHighlighted.connect(       lambda:self.slot_port_name_textHighlighted())
        
        ui.comboBox_baud.currentTextChanged.connect(            lambda:self.slot_port_baud())
        ui.comboBox_byte.currentTextChanged.connect(            lambda:self.slot_port_byte())
        ui.comboBox_parity.currentTextChanged.connect(          lambda:self.slot_port_parity())
        ui.comboBox_stop.currentTextChanged.connect(            lambda:self.slot_port_stop())
        ui.checkBox_xonxoff.stateChanged.connect(               lambda:self.slot_port_xonxoff())
        ui.checkBox_rtscts.stateChanged.connect(                lambda:self.slot_port_rtscts())
        ui.checkBox_dsrdtr.stateChanged.connect(                lambda:self.slot_port_dsrdtr())
        ui.pushButton_PortOpenClose.clicked.connect(            lambda:self.slot_port_open_close())
        ui.pushButton_CleanReceive.clicked.connect(             lambda:self.slot_clean_receive())
        ui.pushButton_StartSend.clicked.connect(                lambda:self.slot_send())
        ui.tableWidget_DataInfo.itemChanged.connect(            lambda:self.slot_tableWidget_Anchor_changed())
        ui.comboBox_Mode.currentTextChanged.connect(            lambda:self.slot_mode_changed())
        ui.pushButton_RecordStart.clicked.connect(              lambda:self.slot_record_start_stop())
        ui.horizontalSlider_Graphic.sliderPressed.connect(      lambda:self.slot_graphic_slider_pressed())
        ui.horizontalSlider_Graphic.sliderReleased.connect(     lambda:self.slot_graphic_slider_released())
        ui.horizontalSlider_Graphic.valueChanged.connect(       lambda:self.slot_graphic_slider_changed())
        
        ui.pushButton_RecordSave.clicked.connect(               lambda:self.slot_save_record())
        ui.pushButton_RecordSave.clicked.connect(               lambda:self.slot_open_record())
        
        ui.pushButton_RecordDir.clicked.connect(                lambda:self.slot_open_record_dir())
    
    # 更新需要动态显示的 UI
    def update_dynamic_ui_500ms(self):
        self.ui_cnt_recording += 1
        if(self.record.recording):
            if(1 == self.ui_cnt_recording % 2):
                self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_2'))
            elif(0 == self.ui_cnt_recording % 2):
                self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_1'))
    
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
        self.draw_circle(self.anchors[0].x, self.anchors[0].y, self.tag.d0, 'r')
        self.draw_circle(self.anchors[1].x, self.anchors[1].y, self.tag.d1, 'g')
        self.draw_circle(self.anchors[2].x, self.anchors[2].y, self.tag.d2, 'b')
    
    def draw_rssi_circles(self):
        # self.draw_circle(self.anchors[0].x, self.anchors[0].y, self.tag.rssi_a0, 'gray')
        # self.draw_circle(self.anchors[1].x, self.anchors[1].y, self.tag.rssi_a1, 'gray')
        # self.draw_circle(self.anchors[2].x, self.anchors[2].y, self.tag.rssi_a2, 'gray')
        
        self.draw_circle(self.anchors[0].x, self.anchors[0].y, 100, 'gray')
        self.draw_circle(self.anchors[1].x, self.anchors[1].y, 100, 'gray')
        self.draw_circle(self.anchors[2].x, self.anchors[2].y, 100, 'gray')
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
    
    def draw_anchor_points(self):
        circle = plt.Circle((self.anchors[0].x, self.anchors[0].y), radius=5, color='r', ec='c', alpha=1, picker=5)
        self.axes_2d_static.add_artist(circle)
        circle = plt.Circle((self.anchors[1].x, self.anchors[1].y), radius=5, color='g', ec='c', alpha=1, picker=5)
        self.axes_2d_static.add_artist(circle)
        circle = plt.Circle((self.anchors[2].x, self.anchors[2].y), radius=5, color='b', ec='c', alpha=1, picker=5)
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
    
    def slot_record_start_stop(self):
        self.record.recording = not self.record.recording
        
        # 开始记录
        if(self.record.recording):
            self.record.start()
            self.ui_main.pushButton_RecordStart.setText('结束')
            self.ui_main.pushButton_RecordStart.setStyleSheet('background-color:gray')
            
            # self.tags.clear()
            self.drawing_idx = 0
            self.stamp_record_start = time.perf_counter()
            self.ui_main.horizontalSlider_Graphic.setValue(0)
            self.ui_main.horizontalSlider_Graphic.setRange(0, 0)
            self.ui_main.plainTextEdit_Hex.clear()
            
        # 结束记录
        else:
            self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_1'))
            self.ui_main.pushButton_RecordStart.setText('开始')
            self.ui_main.pushButton_RecordStart.setStyleSheet('background-color:rgb(255, 255, 255)')
            
    def slot_graphic_slider_pressed(self):
        self.drawing_auto = False
    
    def slot_graphic_slider_released(self):
        self.drawing_auto = True
        
        if self.port.isopen:
            if self.drawing_idx < len(self.tags):
                self.ui_main.horizontalSlider_Graphic.setValue(len(self.tags))
        else:
            self.drawing_idx = self.ui_main.horizontalSlider_Graphic.value()
    
    def slot_graphic_slider_changed(self):
        idx = self.ui_main.horizontalSlider_Graphic.value()
        if not self.drawing_auto:
            if idx < len(self.tags):
                self.clear_display_2d_matplotlib()
                self.draw_a_pkg(idx)
                self.axes_2d_static.figure.canvas.draw()
    
    def slot_save_record(self):
        save_path = '.\\record\\'
        save_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        save_type = '.cvs'
        save_info = save_path + save_name + save_type
        # save_info = save_name + save_type
        print(save_info)
        
        file_w = open(save_info, 'w', newline='')
        writer = csv.writer(file_w)
        # writer.writerow([save_name, time.localtime(), 'hello'])
        
        writer.writerow([self.ui_main.plainTextEdit_Hex.toPlainText()])
        
        file_w.close()
    
    def slot_open_record(self):
        self.log('点击了打开记录按钮')
        
    def slot_open_record_dir(self):
        print()
        print('打开记录路径')
        record_dir = QFileDialog.getExistingDirectory(self.ui_main, "选择记录文件路径", "./") #起始路径
        self.ui_main.lineEdit_RecordDir.setText(record_dir)
    
    def slot_win_set_visibility_changed(self, visable):
        self.ui_main.action_ViewSet.setChecked(visable)
    
    def slot_win_log_visibility_changed(self, visable):
        self.ui_main.action_ViewLog.setChecked(visable)
    
    def slot_win_hex_visibility_changed(self, visable):
        self.ui_main.action_ViewHex.setChecked(visable)
    
    def slot_win_info_visibility_changed(self, visable):
        self.ui_main.action_ViewInfo.setChecked(visable)
    
    def slot_PortComboBox_showPopup(self):
        self.log('扫描端口')
        port = self.port
        cmb = self.ui_main.comboBox_name
        
        port.name_last = cmb.currentText()
        cmb.clear()     # 会触发 Signal: ui.comboBox_name.currentTextChanged
        port.scan()
        
        if(len(port.valid) > 0):
            # cmb.addItems(port.valid)
            for i in port.valid:
                cmb.addItem(i.split(' ')[0])
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
    
    def slot_port_name_activated(self):
        # print('activated')
        pass
    def slot_port_name_currentIndexChanged(self, idx):
        if(len(self.port.valid) > 0):
            self.log(self.port.valid[idx])
    def slot_port_name_editTextChanged(self):
        # print('editTextChanged')
        pass
    def slot_port_name_highlighted(self, idx):
        # print('highlighted id = ', idx)
        if(len(self.port.valid) > 0):
            self.log(self.port.valid[idx])
    def slot_port_name_textActivated(self):
        # print('textActivated')
        pass
    def slot_port_name_textHighlighted(self):
        # print('textHighlighted')
        pass
    
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
        self.log('%s' %(self.ui_main.pushButton_PortOpenClose.text()))
        
        if(not self.port.isopen):
            self.force_update_port_parameter()
            port = self.port
            self.log('尝试打开 %s %s %s %s %s %s %s %s ' %(port.name, port.baud, port.byte, port.parity, port.stop, port.xonxoff, port.rtscts, port.dsrdtr))
        
        self.port.open_close()
        
        self.ui_main.groupBox_PortSet.setEnabled(not self.port.isopen)
        
        if(self.port.isopen):
            self.ui_main.pushButton_PortOpenClose.setText('关闭端口')
            self.ui_main.pushButton_PortOpenClose.setStyleSheet('background-color:gray')
            self.log('端口打开')
        else:
            self.ui_main.pushButton_PortOpenClose.setText('打开端口')
            self.ui_main.pushButton_PortOpenClose.setStyleSheet('background-color:rgb(240, 240, 240)')
            # self.ui_main.pushButton_PortOpenClose.setStyleSheet('background-color:#F0F0F0')
            self.log('端口关闭')
    
    def slot_clean_receive(self):
        self.ui_main.plainTextEdit_Hex.clear()
        
        self.slot_mode_changed()
        
        self.port.read_id = 0
        
        self.log('清空接收')
    
    def slot_send(self):
        if(self.port.isopen):
            send_str = self.ui_main.lineEdit_StartSend.text()
            # https://blog.csdn.net/whatday/article/details/97423901
            # print(send_str)
            # send_bytes = bytes(send_str, encoding='utf-8')
            # send_bytes = send_str.encode('hex')
            # send_bytes = codecs.encode(send_str, 'hex') #send_str.encode('hex')
            # send_bytes = send_str.codecs.encode('hex')0
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
        x_min = self.anchors[0].x
        x_max = self.anchors[0].x
        y_min = self.anchors[0].y
        y_max = self.anchors[0].y
        
        if(self.anchors[1].x < x_min):
            x_min = self.anchors[1].x
        if(self.anchors[2].x < x_min):
            x_min = self.anchors[2].x
        
        if(self.anchors[1].x > x_max):
            x_max = self.anchors[1].x
        if(self.anchors[2].x > x_max):
            x_max = self.anchors[2].x
        
        if(self.anchors[1].y < y_min):
            y_min = self.anchors[1].y
        if(self.anchors[2].y < y_min):
            y_min = self.anchors[2].y
        
        if(self.anchors[1].y > y_max):
            y_max = self.anchors[1].y
        if(self.anchors[2].y > y_max):
            y_max = self.anchors[2].y
        
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
        
        self.anchors[0].x = float(self.ui_main.tableWidget_DataInfo.item(0, 0).text())
        self.anchors[0].y = float(self.ui_main.tableWidget_DataInfo.item(0, 1).text())
        self.anchors[0].z = float(self.ui_main.tableWidget_DataInfo.item(0, 2).text())
        
        self.anchors[1].x = float(self.ui_main.tableWidget_DataInfo.item(1, 0).text())
        self.anchors[1].y = float(self.ui_main.tableWidget_DataInfo.item(1, 1).text())
        self.anchors[1].z = float(self.ui_main.tableWidget_DataInfo.item(1, 2).text())
        
        self.anchors[2].x = float(self.ui_main.tableWidget_DataInfo.item(2, 0).text())
        self.anchors[2].y = float(self.ui_main.tableWidget_DataInfo.item(2, 1).text())
        self.anchors[2].z = float(self.ui_main.tableWidget_DataInfo.item(2, 2).text())
        
        self.update_2d_matplotlib_limit()
        
        self.slot_mode_changed()
        
        pass
    
    def slot_dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
    
    def receive_port_data(self):
        if self.port.isopen:
            if('WangZeKun' == self.ui_main.comboBox_Mode.currentText()):
                self.receive_port_data_WangZeKun()
            
            elif('DongHan' == self.ui_main.comboBox_Mode.currentText()):
                pass
    
    def receive_port_data_WangZeKun(self):
        port = self.port
        pkg_info = self.ui_main.plainTextEdit_Hex
        
        if len(port.rx_cache)<32:                                   # 已缓存的数据不足一个包(不做此判断 会在每个 Byte 收到后快速、重复的进入 导致卡顿)
            try:
                num = port.port.in_waiting              
                if(num > 0):                                        # 有数据待读取
                    new_bytes = port.port.read(num)                 # 读取接收缓冲区全部数据
                    port.rx_cache += new_bytes                      # 追加到接收缓存(此处不能用 append 方法)
                    port.read_id += 1                               # read_id 端口打开后第几次读取
                    
                    while (len(port.rx_cache) >= 32):               # 缓存区至少有一个包
                        if(self.pkg_wzk.update(port.rx_cache[0:32])):           # 尝试按照指定格式提取一个包
                            port.rx_cache = port.rx_cache[32:]                  # 移除已处理部分
                            pkg_info.appendPlainText(self.pkg_wzk.info_str)     # 更新显示
                            
                            if(self.record.recording):                          # 更新记录缓存
                                self.record.len += 1
                                # self.record.record[]
                                # pass
                            
                            # !!! 这里必须使用 copy 否则缓存的数据总是最后一个包 !!!
                            # ref: https://www.iteye.com/blog/greybeard-1442259
                            # self.tags.append(copy.copy(self.tag))
                            # self.tags.append(copy.deepcopy(self.tag))
                            
                            if self.drawing_auto:
                                self.ui_main.horizontalSlider_Graphic.setRange(0, len(self.pkgs))
                                
                        else:
                            port.rx_cache = port.rx_cache[1:]       # 重新对其帧头
            except Exception as e:
                print('串口异常')
                print(e)
    
    def draw_a_pkg(self, idx):
        # # 显示解析后的包信息
        # str_pkg_info = ''
        
        # if idx < len(self.tags):
        #     tag_pkg = self.tags[idx]
            
        #     str_pkg_info += tag_pkg.stamp
        #     str_pkg_info += ' P(%+3d, %+3d)' %(tag_pkg.x, tag_pkg.y)
        #     str_pkg_info += ' D(%3d, %3d, %3d)' %(tag_pkg.d0, tag_pkg.d1, tag_pkg.d2)
        #     str_pkg_info += ' R(%+3d, %+3d, %+3d)' %(tag_pkg.rssi_a0, tag_pkg.rssi_a1, tag_pkg.rssi_a2)
        #     # print('设置包信息', str_pkg_info, time.time())
        #     self.ui_main.lineEdit_PkgInfo.setText(str_pkg_info)
            
        #     # # 开始图形化
        #     # self.clear_display_2d_matplotlib()
            
        #     # draw tag_pkg point
        #     circle = plt.Circle((tag_pkg.x, tag_pkg.y), 3, color='c', ec='c', alpha=0.8, picker=5)
        #     self.axes_2d_static.add_artist(circle)
            
        #     # draw anchors points
        #     circle = plt.Circle((self.anchors[0].x, self.anchors[0].y), radius=5, color='r', ec='c', alpha=1, picker=5)
        #     self.axes_2d_static.add_artist(circle)
        #     circle = plt.Circle((self.anchors[1].x, self.anchors[1].y), radius=5, color='g', ec='c', alpha=1, picker=5)
        #     self.axes_2d_static.add_artist(circle)
        #     circle = plt.Circle((self.anchors[2].x, self.anchors[2].y), radius=5, color='b', ec='c', alpha=1, picker=5)
        #     self.axes_2d_static.add_artist(circle)
            
        #     # draw distance circles
        #     circle = plt.Circle((self.anchors[0].x, self.anchors[0].y), tag_pkg.d0, color='r', ec='c', alpha=0.2, picker=5)
        #     self.axes_2d_static.add_artist(circle)
        #     circle = plt.Circle((self.anchors[1].x, self.anchors[1].y), tag_pkg.d1, color='g', ec='c', alpha=0.2, picker=5)
        #     self.axes_2d_static.add_artist(circle)
        #     circle = plt.Circle((self.anchors[2].x, self.anchors[2].y), tag_pkg.d2, color='b', ec='c', alpha=0.2, picker=5)
        #     self.axes_2d_static.add_artist(circle)
            
        #     # draw rssi circle
        #     circle = plt.Circle((self.anchors[0].x, self.anchors[0].y), tag_pkg.rssi_a0, color='gray', ec='c', alpha=0.2, picker=5)
        #     self.axes_2d_static.add_artist(circle)
        #     circle = plt.Circle((self.anchors[1].x, self.anchors[1].y), tag_pkg.rssi_a1, color='gray', ec='c', alpha=0.2, picker=5)
        #     self.axes_2d_static.add_artist(circle)
        #     circle = plt.Circle((self.anchors[2].x, self.anchors[2].y), tag_pkg.rssi_a2, color='gray', ec='c', alpha=0.2, picker=5)
        #     self.axes_2d_static.add_artist(circle)
            
        #     # circle = plt.Circle((self.anchors[0].x, self.anchors[0].y), 100, color='gray', ec='c', alpha=0.2, picker=5)
        #     # self.axes_2d_static.add_artist(circle)
        #     # circle = plt.Circle((self.anchors[1].x, self.anchors[1].y), 100, color='gray', ec='c', alpha=0.2, picker=5)
        #     # self.axes_2d_static.add_artist(circle)
        #     # circle = plt.Circle((self.anchors[2].x, self.anchors[2].y), 100, color='gray', ec='c', alpha=0.2, picker=5)
        #     # self.axes_2d_static.add_artist(circle)
            
        #     # self.axes_2d_static.figure.canvas.draw()
        pass
        
    
    def update_graphic(self):
        # if self.drawing_idx < len(self.tags):
        #     # 取出数据包
        #     if self.drawing_auto and self.port.isopen:
                
        #         # 开始图形化
        #         self.clear_display_2d_matplotlib()
        #         self.draw_a_pkg(self.drawing_idx)
        #         self.axes_2d_static.figure.canvas.draw()
                
        #         self.ui_main.horizontalSlider_Graphic.setValue(self.drawing_idx + 1)
                
        #         self.drawing_idx += 1
        pass

if __name__ == '__main__':
    app = QApplication([])
    
    idl = IndoorLocation()
    idl.ui_main.show()

    timer_SerialRx = QTimer()
    timer_SerialRx.timeout.connect(idl.receive_port_data)
    timer_SerialRx.start(1)

    timer_UpdateGraphic = QTimer()
    timer_UpdateGraphic.timeout.connect(idl.update_graphic)
    timer_UpdateGraphic.start(100)

    timer_UpdateDynamicUI = QTimer()
    timer_UpdateDynamicUI.timeout.connect(idl.update_dynamic_ui_500ms)
    timer_UpdateDynamicUI.start(500)
    
    sys.exit(app.exec_())