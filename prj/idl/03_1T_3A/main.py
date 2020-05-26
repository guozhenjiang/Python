#!/usr/bin/python
# -*- coding: utf-8 -*-

# region import
from PySide2 import QtGui, QtWidgets, QtCore

from PySide2.QtWidgets import QApplication, QComboBox, QTabWidget, QTableWidgetItem, QFileDialog, QInputDialog, QScrollBar, QLabel, QCheckBox
from PySide2.QtGui import QTextCursor, QTextFormat, QBrush, QColor
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QTextStream, QTimer, Signal, Slot, Qt
from lib_comport import *
from lib_comport_ComboBox import *

import time
import datetime
import threading
import sys
import os
import copy

import matplotlib
from matplotlib.pyplot import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import matplotlib.pyplot as plt

import csv
# endregion

# region 基本公共方法
def time_stamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

def dict_to_csv(data_dicts, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, data_dicts[0].keys())
        w.writeheader()
        
        if(len(data_dicts) > 1):
            w.writerows(data_dicts)
        else:
            w.writerow(data_dicts[0])
#endregion

class Anchor():
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        
        self.show()
        
    def show(self):
        print('A%02d(%+4d, %+4d, %+4d)' %(self.id, self.x, self.y, self.z))

class Tag():
    def __init__(self):
        super().__init__()
        self.id = 0      # 便签编号
        self.d = []      # 标签和基站的距离
        self.r = []      # 标签和基站的信号强度
        self.x = 0
        self.y = 0
        self.z = 0

class Record():
    def __init__(self):
        self.dir = './record'       # 记录文件保存路径
        self.is_recording = False   # 是否正在记录
        self.f_path_name = ''       # 被选中要操作的文件(路径+文件名+后缀)
        
        self.view_min = 0           # 开始
        self.view_len = 0           # 实际长度
        self.view_len_set = 1       # 设置的长度
        self.view_max = 0           # 结束
        
        self.start()
    
    def start(self):
        self.items_list = []        # 以列表方式存储记录信息(记录结束后有可能保存到文件 有可能丢弃)
        self.item_dict = {}         # 以字典方式存储新的记录项
    
    def push_new_item(self):
        self.items_list.append(copy.copy(self.item_dict))
    
    def len(self):
        return len(self.items_list)
    
class Pkg_1T3A():
    '''
    Kingfar协议: https://docs.qq.com/sheet/DTExxWE9BZ0draFNY?tab=q9au4t&c=A1A0A0
    00 01 02 03 04 05 06 07 08 09  10  11  12  13   14   15   16   17   18   19        20        21        22        23        24        25 26 27 28 29 30 31
    FF 02 XX XX XX XX XX XX XX x_H x_L y_H y_L d0_H d0_L d1_H d1_L d2_H d2_L rssi_a0_H rssi_a0_L rssi_a1_H rssi_a1_L rssi_a2_H rssi_a2_L XX XX XX XX XX XX XX
    (x, y)          标签坐标
    (d0, d1, d2)    标签到 3 个基站的距离 单位 cm
    (r0, r1, r2)    便签到三个基站的信号强度
    '''
    
    def __init__(self):
        self.init()
        
    def init(self):
        self.x = 0
        self.y = 0
        
        self.d0 = 0
        self.d1 = 0
        self.d2 = 0
        
        self.r0 = 0
        self.r1 = 0
        self.r2 = 0
        
        self.raw = bytes()
    
    def update(self, raw_bytes):
        if (0xFF == raw_bytes[0]) and (0x02 == raw_bytes[1]):
            self.x = int(np.int16((raw_bytes[ 9]  << 8) | raw_bytes[10]))
            self.y = int(np.int16((raw_bytes[11]  << 8) | raw_bytes[12]))
            
            self.d0 =             (raw_bytes[13]  << 8) | raw_bytes[14]
            self.d1 =             (raw_bytes[15]  << 8) | raw_bytes[16]
            self.d2 =             (raw_bytes[17]  << 8) | raw_bytes[18]
            
            self.r0 = int(np.int16((raw_bytes[19]  << 8) | raw_bytes[20]))
            self.r1 = int(np.int16((raw_bytes[21]  << 8) | raw_bytes[11]))
            self.r2 = int(np.int16((raw_bytes[23]  << 8) | raw_bytes[24]))
            
            self.raw = raw_bytes
            
            return True
        else:
            return False

class CustomQScrollBar(QScrollBar):
    signal_scrollbar_ctrl_wheel = Signal(int)
    
    def __init__(self, parent = None):
        super(CustomQScrollBar, self).__init__(parent)
    
    def keyPressEvent(self, key):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
            print('Ctrl 按下')
    
    def wheelEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
            print('Ctrl + Wheel:', event.delta())
            
            self.signal_scrollbar_ctrl_wheel.emit(event.delta() / 120)
            
        if modifiers == QtCore.Qt.ShiftModifier:
            print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
            print('Shift + Wheel:', event.delta())
            
class IndoorLocation(QObject):
    # region 基站
    anchors = []
    anchors.append(Anchor(0, 0, 0, 200))
    anchors.append(Anchor(1, 0, 200, 0))
    anchors.append(Anchor(2, 200, 0, 0))
    # endregion
    
    new_pkg = Pkg_1T3A()
    drawing_auto = True
    
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
        
        # original_size = self.ui_main.dockWidget_Pkg.size()
        # # print()
        # # print('************************')
        # # print(type(original_size))
        # # print(original_size)
        # # print(original_size.width(), original_size.height())
        # # print('************************')
        # # print()
        
        # self.ui_main.dockWidget_Pkg.resize(100, original_size.height())     # resize 对 DockWidget 无效
        
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
        
        self.ui_main.setWindowIcon(QtGui.QPixmap(r'.\ico\location_256x256.png'))
        
        self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_128x128_red_dot.png'))
        self.ui_main.pushButton_RecordSave.setIcon(QtGui.QPixmap(r'.\ico\save_256x256.png'))
        self.ui_main.pushButton_RecordPlay.setIcon(QtGui.QPixmap(r'.\ico\play_256x256.png'))
        self.ui_main.pushButton_RecordDelete.setIcon(QtGui.QPixmap(r'.\ico\delete_128x128.png'))
        self.ui_main.pushButton_RecordDir.setIcon(QtGui.QPixmap(r'.\ico\open_dir_256x256.png'))
        self.ui_main.pushButton_RecordRefresh.setIcon(QtGui.QPixmap(r'.\ico\refresh_256x256.png'))
        
        ui.comboBox_name_raw.deleteLater()                                  # 删掉 UI 生成的端口选择下拉框控件
        ui.comboBox_name = PortComboBox()                                   # 用自己重写的控件替换被删的
        ui.gridLayout_port_set_select.addWidget(ui.comboBox_name, 0, 1)     # 添加到原来的布局框中相同位置
        
        self.record_view_init_ui()
        
        self.slot_record_refresh()          # 更新记录目录下的文件
        
        # 将 Matlabplotlib 2D 图像嵌入界面
        # layout = self.ui_main.horizontalLayout_2D          # <class 'PySide2.QtWidgets.QHBoxLayout'>
        
        self.canvas_2d_matplotlib = FigureCanvas(Figure())  # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        ui.horizontalLayout_2D.addWidget(self.canvas_2d_matplotlib)
        
        self.axes_2d_static = self.canvas_2d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_2d_static.grid(True)
        
        self.update_2d_matplotlib_limit()
        
        # 将 Matlabplotlib 3D 图像嵌入界面
        # self.canvas_3d_matplotlib = FigureCanvas(Figure())      # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        self.canvas_3d_matplotlib = FigureCanvas(Figure())
        ui.horizontalLayout_3D_Matplotlib.addWidget(self.canvas_3d_matplotlib)
        self.axes_3d_static = self.canvas_3d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_3d_static.grid(True)
        
        # 添加 matplotlib 工具栏是有效的 只不过添加后部分功能没有
        # self.ui_main.toolbar = NavigationToolbar(self.canvas_3d_matplotlib, self.ui_main)
        # self.ui_main.verticalLayout_2D_Matplotlib.addWidget(self.ui_main.toolbar)
        
        self.slot_mode_changed()
    
    def record_view_init_ui(self):
        ui = self.ui_main
        
        # 删掉 Designer 生成的滑块 重写一个 占据相同的位置
        ui.horizontalScrollBar_GraphicRaw.deleteLater()
        ui.horizontalScrollBar_Graphic = CustomQScrollBar(Qt.Horizontal)
        ui.horizontalScrollBar_Graphic.setPageStep(1)
        ui.horizontalScrollBar_Graphic.setSingleStep(1)
        
        # record label
        ui.label_record_min = QLabel('min:0')       # 最小是 0 表示没有收到数据包
        ui.label_record_idx = QLabel('idx:0')
        ui.label_record_max = QLabel('max:0')
        
        self.update_record_value_and_label(0, 0, 0)
        
        # record_view label
        ui.label_view_min = QLabel('min:%d' %(self.record.view_min))
        ui.label_view_len = QLabel('len:%d(%d)' %(self.record.view_len, self.record.view_len_set))
        ui.label_view_max = QLabel('max:%d' %(self.record.view_max))
        
        ui.checkbox_graphic_all = QCheckBox('All')
        
        # 高度固定
        ui.label_record_min.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        ui.label_record_idx.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        ui.label_record_max.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        ui.label_view_min.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        ui.label_view_len.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        ui.label_view_max.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        ui.checkbox_graphic_all.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        # 齐方式
        ui.label_record_min.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        ui.label_record_idx.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        ui.label_record_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        ui.label_view_min.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        ui.label_view_len.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        ui.label_view_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # record label 水平布局
        layout_record = QtWidgets.QHBoxLayout()
        layout_record_view = QtWidgets.QHBoxLayout()
        
        layout_record.addWidget(ui.label_record_min)
        layout_record.addWidget(ui.label_record_idx)
        layout_record.addWidget(ui.label_record_max)
        
        layout_record_view.addWidget(ui.checkbox_graphic_all)
        layout_record_view.addWidget(ui.label_view_min)
        layout_record_view.addWidget(ui.label_view_len)
        layout_record_view.addWidget(ui.label_view_max)
        
        ui.verticalLayout_2D_Matplotlib.addItem(layout_record)
        ui.verticalLayout_2D_Matplotlib.addWidget(ui.horizontalScrollBar_Graphic)
        ui.verticalLayout_2D_Matplotlib.addItem(layout_record_view)
        
        # 如果添加的全部是 Wiedget 则无需此操作(上面添加了 layout)
        ui.tab_2D_Matplotlib.setLayout(ui.verticalLayout_2D_Matplotlib)
    
    def update_record_len_scrollbar_and_label(self):
        record_len = self.record.len()
        
        if (0 == self.ui_main.horizontalScrollBar_Graphic.minimum()) and (record_len > 0):
            self.ui_main.horizontalScrollBar_Graphic.setMinimum(1)
            self.ui_main.label_record_min.setText('min:%d' %(self.ui_main.horizontalScrollBar_Graphic.minimum()))
            
        self.ui_main.horizontalScrollBar_Graphic.setMaximum(record_len)
        self.ui_main.label_record_max.setText('max:%d' %(record_len))
    
    def update_record_value_and_label(self, min, idx, max):
        self.ui_main.horizontalScrollBar_Graphic.setMinimum(min)
        self.ui_main.horizontalScrollBar_Graphic.setMaximum(max)
        self.ui_main.horizontalScrollBar_Graphic.setValue(idx)
        
        self.ui_main.label_record_min.setText('min:%d' %(min))
        self.ui_main.label_record_idx.setText('idx:%d' %(idx))
        self.ui_main.label_record_max.setText('max:%d' %(max))
    
    def init_signal_slot(self):
        self.log('初始化 Signal Slot')
        ui = self.ui_main
        
        ui.action_ViewSet.changed.connect(                                  lambda:self.slot_dock_show_hide(ui.dockWidget_Set, ui.action_ViewSet.isChecked()))
        ui.action_ViewLog.changed.connect(                                  lambda:self.slot_dock_show_hide(ui.dockWidget_Log, ui.action_ViewLog.isChecked()))
        ui.action_ViewHex.changed.connect(                                  lambda:self.slot_dock_show_hide(ui.dockWidget_Pkg, ui.action_ViewHex.isChecked()))
        ui.action_ViewInfo.changed.connect(                                 lambda:self.slot_dock_show_hide(ui.dockWidget_Info, ui.action_ViewInfo.isChecked()))
        
        ui.dockWidget_Set.visibilityChanged.connect(                        lambda visable:self.slot_win_set_visibility_changed(visable))
        ui.dockWidget_Log.visibilityChanged.connect(                        lambda visable:self.slot_win_log_visibility_changed(visable))
        ui.dockWidget_Pkg.visibilityChanged.connect(                        lambda visable:self.slot_win_hex_visibility_changed(visable))
        ui.dockWidget_Info.visibilityChanged.connect(                       lambda visable:self.slot_win_info_visibility_changed(visable))
        
        ui.comboBox_name.signal_PortComboBox_showPopup.connect(             lambda:self.slot_PortComboBox_showPopup())
        ui.comboBox_name.currentTextChanged.connect(                        lambda:self.slot_port_name())
        
        ui.comboBox_name.activated.connect(                                 lambda:self.slot_port_name_activated())
        ui.comboBox_name.currentIndexChanged.connect(                       lambda idx:self.slot_port_name_currentIndexChanged(idx))
        ui.comboBox_name.editTextChanged.connect(                           lambda:self.slot_port_name_editTextChanged())
        ui.comboBox_name.highlighted.connect(                               lambda idx:self.slot_port_name_highlighted(idx))
        ui.comboBox_name.textActivated.connect(                             lambda:self.slot_port_name_textActivated())
        ui.comboBox_name.textHighlighted.connect(                           lambda:self.slot_port_name_textHighlighted())
        
        ui.comboBox_baud.currentTextChanged.connect(                        lambda:self.slot_port_baud())
        ui.comboBox_byte.currentTextChanged.connect(                        lambda:self.slot_port_byte())
        ui.comboBox_parity.currentTextChanged.connect(                      lambda:self.slot_port_parity())
        ui.comboBox_stop.currentTextChanged.connect(                        lambda:self.slot_port_stop())
        ui.checkBox_xonxoff.stateChanged.connect(                           lambda:self.slot_port_xonxoff())
        ui.checkBox_rtscts.stateChanged.connect(                            lambda:self.slot_port_rtscts())
        ui.checkBox_dsrdtr.stateChanged.connect(                            lambda:self.slot_port_dsrdtr())
        ui.pushButton_PortOpenClose.clicked.connect(                        lambda:self.slot_port_open_close())
        ui.pushButton_CleanReceive.clicked.connect(                         lambda:self.slot_clean_receive())
        ui.pushButton_StartSend.clicked.connect(                            lambda:self.slot_send())
        ui.tableWidget_DataInfo.itemChanged.connect(                        lambda:self.slot_tableWidget_Anchor_changed())
        ui.comboBox_Mode.currentTextChanged.connect(                        lambda:self.slot_mode_changed())
        
        ui.pushButton_RecordStart.clicked.connect(                          lambda:self.slot_record_start_stop())
        ui.pushButton_RecordSave.clicked.connect(                           lambda:self.slot_record_save())
        ui.pushButton_RecordRefresh.clicked.connect(                        lambda:self.slot_record_refresh())
        ui.pushButton_RecordPlay.clicked.connect(                           lambda:self.slot_record_play())
        ui.pushButton_RecordDelete.clicked.connect(                         lambda:self.slot_record_delete())
        ui.pushButton_RecordDir.clicked.connect(                            lambda:self.slot_record_open_dir())
        
        ui.listWidget_RecordFiles.currentTextChanged.connect(               lambda f_name:self.slot_record_select(f_name))
        
        # 滚动条信号与槽
        ui.horizontalScrollBar_Graphic.signal_scrollbar_ctrl_wheel.connect( lambda det:self.slot_griphic_scrollbar_ctrl_wheel(det))     # Ctrl + Wheel
        ui.horizontalScrollBar_Graphic.valueChanged.connect(                lambda val:self.slot_griphic_scrollbar_val_changed(val))    # tracking() 值发生变化
        # ui.horizontalScrollBar_Graphic.rangeChanged.connect(                lambda:self.slot_griphic_scrollbar_range_changed())
        ui.horizontalScrollBar_Graphic.sliderPressed.connect(               lambda:self.slot_griphic_scrollbar_slider_pressed()) # 按下滑块
        # ui.horizontalScrollBar_Graphic.sliderMoved.connect(                 lambda:self.slot_griphic_scrollbar_slider_moved())
        ui.horizontalScrollBar_Graphic.sliderReleased.connect(              lambda:self.slot_griphic_scrollbar_slider_released())# 释放滑块
        # ui.horizontalScrollBar_Graphic.actionTriggered.connect(             lambda:self.slot_griphic_scrollbar_action_trigged())
        
        ui.checkbox_graphic_all.stateChanged.connect(                       lambda sta:self.slot_checkbox_record_view_all_changed(sta))
    
    # 更新需要动态显示的 UI 每 500ms 调用一次
    def update_dynamic_ui(self):
        if(self.record.is_recording):
            self.ui_cnt_recording += 1
            if(1 == self.ui_cnt_recording % 2):
                self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\stop_256x256_green.png'))
            elif(0 == self.ui_cnt_recording % 2):
                self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\stop_256x256_red.png'))
    
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
        self.record.is_recording = not self.record.is_recording
        
        # 记录开始
        if(self.record.is_recording):
            self.log('开始记录')
            self.record.start()
            self.ui_main.pushButton_RecordStart.setText('结束')
            self.ui_main.pushButton_RecordStart.setStatusTip('结束记录')
            self.ui_main.pushButton_RecordSave.setEnabled(False)
            self.update_dynamic_ui()
            
            self.update_record_value_and_label(0, 0, 0)
            
            self.ui_main.plainTextEdit_Hex.clear()
            
        # 记录结束
        else:
            self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_128x128_red_dot.png'))
            self.ui_main.pushButton_RecordStart.setText('开始')
            self.ui_main.pushButton_RecordStart.setStatusTip('开始记录')
            
            len = self.record.len()
            self.log('新纪录 %d 条' %(len))
            
            if len > 0:
                self.ui_main.pushButton_RecordSave.setEnabled(True)
    
    def slot_record_save(self):
        save_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        
        # 在此弹出对话框 让用户输入记录文件名称中自定义部分
        f_name_user, ok = QInputDialog.getText(self.ui_main, '文件名-自定义部分', '请输入文件名')
        
        if f_name_user != '':                           # 若输入内容不为空 使用空格分开自动前缀和用户输入部分
            f_name_user = ' ' + f_name_user
        
        f_record = self.record.dir + '/' + save_name + f_name_user + '.csv'
        self.log('保存: %s' %(f_record))
        
        dict_to_csv(self.record.items_list, f_record)
        
        self.slot_record_refresh()
        self.ui_main.pushButton_RecordSave.setEnabled(False)
        
    def slot_record_refresh(self):
        # f_name, f_filter = QFileDialog.getOpenFileName(self.ui_main, '选择单个文件', './', '筛选条件(*.jpg *.png *.bmp)')
        # print(f_name)
        
        # f_names, f_filter = QFileDialog.getOpenFileNames(self.ui_main, '选择单个或多个文件', './', '筛选条件(*.jpg *.png *.bmp)')
        # print(f_names)
        
        self.log('刷新: %s' %(self.record.dir))
        self.ui_main.lineEdit_RecordDir.setText(self.record.dir)
        
        # fs = os.listdir(f_path)                                                                           # 列出路径下所有的文件和文件夹
        fs = [f for f in os.listdir(self.record.dir) if os.path.isfile(os.path.join(self.record.dir, f))]   # 只列出文件
        self.ui_main.listWidget_RecordFiles.clear()
        self.ui_main.listWidget_RecordFiles.addItems(fs)
        
        self.ui_main.pushButton_RecordPlay.setEnabled(False)
        self.ui_main.pushButton_RecordDelete.setEnabled(False)
        
    
    def slot_record_play(self):
        self.log('回放 %s' %(self.record.f_path_name))
    
    def slot_record_delete(self):
        self.log('删除: %s' %(self.record.f_path_name))
        os.remove(self.record.f_path_name)
        self.slot_record_refresh()
    
    def slot_record_open_dir(self):
        self.record.dir = QFileDialog.getExistingDirectory(self.ui_main, '选择记录文件路径', self.record.dir)
        self.ui_main.lineEdit_RecordDir.setText(self.record.dir)
        self.slot_record_refresh()
    
    def slot_record_select(self, f_name):
        self.record.f_path_name = self.record.dir + r'/' + f_name
        self.log(self.record.f_path_name)
        self.ui_main.pushButton_RecordPlay.setEnabled(True)
        self.ui_main.pushButton_RecordDelete.setEnabled(True)
    
    def slot_griphic_scrollbar_ctrl_wheel(self, det):
        if det > 0:
            if self.record.view_len_set < self.ui_main.horizontalScrollBar_Graphic.maximum():
                self.record.view_len_set *= 2
                if 0 == self.record.view_len_set:
                    self.record.view_len_set = 1
        elif det < 0:
            if self.record.view_len_set >= 1:
                self.record.view_len_set //= 2
            
        self.update_record_view_scrollbar_and_label()
        
    def update_record_view_scrollbar_and_label(self):
        # 记录非空
        if self.ui_main.horizontalScrollBar_Graphic.minimum() > 0:
            
            # 全部显示
            if self.ui_main.checkbox_graphic_all.isChecked():
                self.ui_main.horizontalScrollBar_Graphic.setValue(self.ui_main.horizontalScrollBar_Graphic.maximum())
                self.record.view_max = self.ui_main.horizontalScrollBar_Graphic.value()
                self.record.view_min = self.ui_main.horizontalScrollBar_Graphic.minimum()
                self.record.view_len = self.ui_main.horizontalScrollBar_Graphic.maximum()
            
            # 显示非空长度
            elif self.record.view_len_set > 0:
                self.record.view_max = self.ui_main.horizontalScrollBar_Graphic.value()
                self.record.view_min = self.record.view_max - self.record.view_len_set + 1
                if self.record.view_min < self.ui_main.horizontalScrollBar_Graphic.minimum():
                    self.record.view_min = self.ui_main.horizontalScrollBar_Graphic.minimum()
                self.record.view_len = self.record.view_max - self.record.view_min + 1
            
            # 显示关闭
            else:
                self.record.view_max = self.ui_main.horizontalScrollBar_Graphic.value()
                self.record.view_min = self.ui_main.horizontalScrollBar_Graphic.value()
                self.record.view_len = 0
        
        # 记录为空
        else:
            self.record.view_min = 0
            self.record.view_max = 0
            self.record.view_len = 0
        
        self.ui_main.horizontalScrollBar_Graphic.setPageStep(self.record.view_len)
        
        self.ui_main.label_view_min.setText('min:%d' %(self.record.view_min))
        self.ui_main.label_view_len.setText('len:%d(%d)' %(self.record.view_len, self.record.view_len_set))
        self.ui_main.label_view_max.setText('max:%d' %(self.record.view_max))
        
    def slot_griphic_scrollbar_val_changed(self, val):
        self.update_record_view_scrollbar_and_label()
        self.ui_main.label_record_idx.setText('idx:%d' %(val))
    def slot_griphic_scrollbar_slider_pressed(self):
        print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
        print('pressed:')
    def slot_griphic_scrollbar_slider_released(self):
        print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
        print('released:')
        
    def slot_checkbox_record_view_all_changed(self, sta):
        if 0 == sta:    # 不选中
            self.ui_main.checkbox_graphic_all.setStyleSheet('background-color:rgb(240, 240, 240)')
        elif 2 == sta:  # 选中
            self.ui_main.checkbox_graphic_all.setStyleSheet('background-color:gray')
        
        self.update_record_view_scrollbar_and_label()
        
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
        # self.log('端口 %s' %(self.port.name))
    
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
            self.log('发送:\r\n %s' %(send_bytes))
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
    
    def update_uart_rx(self):
        if self.port.isopen:
            self.uart_rx_handle()
    
    def update_uart_pkg_text_info(self, item_dict):
        pkg_stamp = item_dict['stamp']
        
        pkg_info = ' T(%d, %d)' %(item_dict['x'], item_dict['y'])
        pkg_info += ' D(%d, %d, %d)' %(item_dict['d0'], item_dict['d1'], item_dict['d2'])
        pkg_info += ' R(%d, %d, %d)' %(item_dict['r0'], item_dict['r1'], item_dict['r2'])
        
        pkg_raw = ''
        for v in item_dict['raw']:
            pkg_raw += ' %02X' %(v)
        
        pkg_str = pkg_stamp + pkg_info + pkg_raw
        self.ui_main.plainTextEdit_Hex.appendPlainText(pkg_str)
        self.ui_main.lineEdit_PkgRaw.setText(pkg_stamp + pkg_raw)
        self.ui_main.lineEdit_PkgInfo.setText(pkg_info)
    
    def update_record_item_dict(self):
        self.record.item_dict['stamp'] = time_stamp_ms()
        self.record.item_dict['x'] = self.new_pkg.x
        self.record.item_dict['y'] = self.new_pkg.y
        self.record.item_dict['d0'] = self.new_pkg.d0
        self.record.item_dict['d1'] = self.new_pkg.d1
        self.record.item_dict['d2'] = self.new_pkg.d2
        self.record.item_dict['r0'] = self.new_pkg.r0
        self.record.item_dict['r1'] = self.new_pkg.r1
        self.record.item_dict['r2'] = self.new_pkg.r2
        self.record.item_dict['a0.x'] = self.anchors[0].x
        self.record.item_dict['a0.y'] = self.anchors[0].y
        self.record.item_dict['a1.x'] = self.anchors[1].x
        self.record.item_dict['a1.y'] = self.anchors[1].y
        self.record.item_dict['a2.x'] = self.anchors[2].x
        self.record.item_dict['a2.y'] = self.anchors[2].y
        self.record.item_dict['raw'] = self.new_pkg.raw
    
    def uart_rx_handle(self):
        port = self.port
        
        # 已缓存的数据不足一个包(不做此判断 会在每个 Byte 收到后快速、重复的进入 导致卡顿)
        if len(port.rx_cache)<32:
            try:
                num = port.port.in_waiting
                if(num > 0):                                    # 有数据待读取
                    new_bytes = port.port.read(num)             # 读取接收缓冲区全部数据
                    port.rx_cache += new_bytes                  # 追加到接收缓存(此处不能用 append 方法)
                    port.read_id += 1                           # read_id 端口打开后第几次读取
                    
                    while (len(port.rx_cache) >= 32):           # 缓存区至少有一个包
                        
                        # 成功提取了一个数据包
                        if(self.new_pkg.update(port.rx_cache[0:32])):
                            port.rx_cache = port.rx_cache[32:]  # 移除已处理部分
                            
                            self.update_record_item_dict()
                            self.update_uart_pkg_text_info(self.record.item_dict)   # copy.copy(...)
                            
                            if(self.record.is_recording):
                                self.record.push_new_item()
                                self.update_record_len_scrollbar_and_label()
                                self.update_record_view_scrollbar_and_label()
                        
                        # 重新对齐帧头
                        else:
                            port.rx_cache = port.rx_cache[1:]
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
    
    def update_record_graphic(self):
        # if self.drawing_idx < len(self.tags):
        #     # 取出数据包
        #     if self.drawing_auto and self.port.isopen:
        #         # 开始图形化
        #         self.clear_display_2d_matplotlib()
        #         self.draw_a_pkg(self.drawing_idx)
        #         self.axes_2d_static.figure.canvas.draw()
        #         self.drawing_idx += 1
        pass

if __name__ == '__main__':
    app = QApplication([])
    
    idl = IndoorLocation()
    idl.ui_main.show()

    timer_SerialRx = QTimer()
    timer_SerialRx.timeout.connect(idl.update_uart_rx)
    timer_SerialRx.start(1)

    timer_UpdateGraphic = QTimer()
    timer_UpdateGraphic.timeout.connect(idl.update_record_graphic)
    timer_UpdateGraphic.start(100)

    timer_UpdateDynamicUI = QTimer()
    timer_UpdateDynamicUI.timeout.connect(idl.update_dynamic_ui)
    timer_UpdateDynamicUI.start(500)
    
    sys.exit(app.exec_())