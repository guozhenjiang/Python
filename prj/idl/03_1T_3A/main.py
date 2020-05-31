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
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

import csv
import pandas as pd

from enum import Enum
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

class Map():
    def __init__(self):
        self.dir = './map'
        self.f_path_name = ''
        self.dict = {}

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
            # print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
            # print('Ctrl + Wheel:', event.delta())
            
            self.signal_scrollbar_ctrl_wheel.emit(event.delta() / 120)
            
        # if modifiers == QtCore.Qt.ShiftModifier:
        #     print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
        #     print('Shift + Wheel:', event.delta())
            
class IndoorLocation(QObject):
    def __init__(self):
        self.map = Map()                # 地图信息
        self.port = Port()              # 占用的端口
        self.new_pkg = Pkg_1T3A()       # 串口数据包解析缓存
        self.record = Record()          # 数据记录
        self.drawed_end = 0             # 图形化状态
        self.drawed_len = 0
        self.ui_cnt_recording = 0       # 动态界面变化控制 记录中按钮图标
        
        # 初始化
        self.init_ui()
        self.init_signal_slot()
    
    # Log 功能
    def log(self, log):
        self.ui_main.plainTextEdit_Log.appendPlainText(log)
        print(log)
    
    def init_ui(self):
        f_ui_main = './ui_main_1T_nA.ui'
        self.ui_main = QUiLoader().load(f_ui_main)
        self.log('加载界面文件 %s' %(f_ui_main))
        
        self.log('初始化图标')
        self.ui_main.setWindowIcon(QtGui.QPixmap(r'.\ico\location_256x256.png'))                            # 窗口图标
        self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\record_128x128_red_dot.png'))     # Record
        self.ui_main.pushButton_RecordSave.setIcon(QtGui.QPixmap(r'.\ico\save_256x256.png'))
        self.ui_main.pushButton_RecordPlay.setIcon(QtGui.QPixmap(r'.\ico\play_256x256.png'))
        self.ui_main.pushButton_RecordDelete.setIcon(QtGui.QPixmap(r'.\ico\delete_128x128.png'))
        self.ui_main.pushButton_RecordDir.setIcon(QtGui.QPixmap(r'.\ico\open_dir_256x256.png'))
        self.ui_main.pushButton_RecordRefresh.setIcon(QtGui.QPixmap(r'.\ico\refresh_256x256.png'))
        self.ui_main.pushButton_MapRefresh.setIcon(QtGui.QPixmap(r'.\ico\refresh_256x256.png'))             # Map
        self.ui_main.pushButton_MapImport.setIcon(QtGui.QPixmap(r'.\ico\import_100x100.png'))
        self.ui_main.pushButton_MapDelete.setIcon(QtGui.QPixmap(r'.\ico\delete_128x128.png'))
        self.ui_main.pushButton_MapDir.setIcon(QtGui.QPixmap(r'.\ico\open_dir_256x256.png'))
        
        self.log('加载自定义控件 端口选择')
        self.ui_main.comboBox_name_raw.deleteLater()                                  # 删掉 UI 生成的端口选择下拉框控件
        self.ui_main.comboBox_name = PortComboBox()                                   # 用自己重写的控件替换被删的
        self.ui_main.gridLayout_port_set_select.addWidget(self.ui_main.comboBox_name, 0, 1)     # 添加到原来的布局框中相同位置
        self.slot_PortComboBox_showPopup()
        
        self.log('更新界面 记录')
        self.init_ui_record_view()
        self.slot_record_refresh()          # 更新记录目录下的文件
        self.slot_map_refresh()             # 更新地图目录下的文件
        
        self.log('嵌入图形化控件 Matlabplotlib 2D')
        self.canvas_2d_matplotlib = FigureCanvas(Figure())  # <class 'matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg'>
        self.ui_main.horizontalLayout_2D.addWidget(self.canvas_2d_matplotlib)
        self.axes_2d_static = self.canvas_2d_matplotlib.figure.subplots()   # <class 'matplotlib.axes._subplots.AxesSubplot'>
        self.axes_2d_static.grid(True)
        
        # 添加 matplotlib 工具栏是有效的 只不过添加后部分功能没有
        self.ui_main.toolbar = NavigationToolbar(self.canvas_2d_matplotlib, self.ui_main)
        self.ui_main.verticalLayout_2D_Matplotlib.addWidget(self.ui_main.toolbar)
        
        self.slot_mode_changed()
    
    def init_ui_record_view(self):
        # 删掉 Designer 生成的滑块 重写一个 占据相同的位置
        self.ui_main.horizontalScrollBar_GraphicRaw.deleteLater()
        self.ui_main.horizontalScrollBar_Graphic = CustomQScrollBar(Qt.Horizontal)
        self.ui_main.horizontalScrollBar_Graphic.setPageStep(1)
        self.ui_main.horizontalScrollBar_Graphic.setSingleStep(1)
        
        # record label
        self.ui_main.label_record_min = QLabel('min:0')       # 最小是 0 表示没有收到数据包
        self.ui_main.label_record_idx = QLabel('idx:0')
        self.ui_main.label_record_max = QLabel('max:0')
        
        self.update_record_value_and_label(0, 0, 0)
        
        # record_view label
        self.ui_main.label_view_min = QLabel('min:%d' %(self.record.view_min))
        self.ui_main.label_view_len = QLabel('len:%d(%d)' %(self.record.view_len, self.record.view_len_set))
        self.ui_main.label_view_max = QLabel('max:%d' %(self.record.view_max))
        
        self.ui_main.checkbox_graphic_all = QCheckBox('All')
        self.ui_main.checkbox_graphic_track = QCheckBox('Track')
        
        # 高度固定
        self.ui_main.label_record_min.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui_main.label_record_idx.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui_main.label_record_max.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        self.ui_main.label_view_min.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui_main.label_view_len.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui_main.label_view_max.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        self.ui_main.checkbox_graphic_all.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui_main.checkbox_graphic_track.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        # 齐方式
        self.ui_main.label_record_min.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.ui_main.label_record_idx.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.ui_main.label_record_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        self.ui_main.label_view_min.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.ui_main.label_view_len.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.ui_main.label_view_max.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # record label 水平布局
        layout_record = QtWidgets.QHBoxLayout()
        layout_record_view = QtWidgets.QHBoxLayout()
        
        layout_record.addWidget(self.ui_main.label_record_min)
        layout_record.addWidget(self.ui_main.label_record_idx)
        layout_record.addWidget(self.ui_main.label_record_max)
        
        layout_record_view.addWidget(self.ui_main.checkbox_graphic_all)
        layout_record_view.addWidget(self.ui_main.checkbox_graphic_track)
        layout_record_view.addWidget(self.ui_main.label_view_min)
        layout_record_view.addWidget(self.ui_main.label_view_len)
        layout_record_view.addWidget(self.ui_main.label_view_max)
        
        self.ui_main.verticalLayout_2D_Matplotlib.addItem(layout_record)
        self.ui_main.verticalLayout_2D_Matplotlib.addWidget(self.ui_main.horizontalScrollBar_Graphic)
        self.ui_main.verticalLayout_2D_Matplotlib.addItem(layout_record_view)
        
        # 如果添加的全部是 Wiedget 则无需此操作(上面添加了 layout)
        self.ui_main.tab_2D_Matplotlib.setLayout(self.ui_main.verticalLayout_2D_Matplotlib)
    
    def update_record_len_scrollbar_and_label(self):
        record_len = self.record.len()
        
        if (0 == self.ui_main.horizontalScrollBar_Graphic.minimum()) and (record_len > 0):
            self.ui_main.horizontalScrollBar_Graphic.setMinimum(1)
            self.ui_main.label_record_min.setText('min:%d' %(self.ui_main.horizontalScrollBar_Graphic.minimum()))
            
        self.ui_main.horizontalScrollBar_Graphic.setMaximum(record_len)
        
        if self.ui_main.checkbox_graphic_track.isChecked():
            self.ui_main.horizontalScrollBar_Graphic.setValue(self.ui_main.horizontalScrollBar_Graphic.maximum())
        
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
        
        ui.comboBox_name.currentIndexChanged.connect(                       lambda idx:self.slot_port_name_currentIndexChanged(idx))
        ui.comboBox_name.highlighted.connect(                               lambda idx:self.slot_port_name_highlighted(idx))
        
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
        ui.comboBox_Mode.currentTextChanged.connect(                        lambda:self.slot_mode_changed())
        
        ui.pushButton_RecordStart.clicked.connect(                          lambda:self.slot_record_start_stop())
        ui.pushButton_RecordSave.clicked.connect(                           lambda:self.slot_record_save())
        ui.pushButton_RecordRefresh.clicked.connect(                        lambda:self.slot_record_refresh())
        ui.pushButton_MapRefresh.clicked.connect(                           lambda:self.slot_map_refresh())
        ui.pushButton_RecordPlay.clicked.connect(                           lambda:self.slot_record_play())
        ui.pushButton_RecordDelete.clicked.connect(                         lambda:self.slot_record_delete())
        ui.pushButton_RecordDir.clicked.connect(                            lambda:self.slot_record_open_dir())
        ui.pushButton_MapDir.clicked.connect(                               lambda:self.slot_map_open_dir())
        ui.pushButton_MapImport.clicked.connect(                            lambda:self.slot_map_import())
        
        ui.listWidget_RecordFiles.currentTextChanged.connect(               lambda f_name:self.slot_record_select(f_name))
        ui.listWidget_MapFiles.currentTextChanged.connect(                  lambda f_name:self.slot_map_select(f_name))
        
        # 滚动条信号与槽
        ui.horizontalScrollBar_Graphic.signal_scrollbar_ctrl_wheel.connect( lambda det:self.slot_griphic_scrollbar_ctrl_wheel(det))     # Ctrl + Wheel
        ui.horizontalScrollBar_Graphic.valueChanged.connect(                lambda val:self.slot_griphic_scrollbar_val_changed(val))    # tracking() 值发生变化

        ui.checkbox_graphic_all.stateChanged.connect(                       lambda sta:self.slot_checkbox_record_view_all_changed(sta))
        ui.checkbox_graphic_track.stateChanged.connect(                     lambda sta:self.slot_checkbox_record_view_track_changed(sta))

    # 更新需要动态显示的 UI 每 500ms 调用一次
    def update_dynamic_ui(self):
        if(self.record.is_recording):
            self.ui_cnt_recording += 1
            if(1 == self.ui_cnt_recording % 2):
                self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\stop_256x256_green.png'))
            elif(0 == self.ui_cnt_recording % 2):
                self.ui_main.pushButton_RecordStart.setIcon(QtGui.QPixmap(r'.\ico\stop_256x256_red.png'))
    
    def slot_mode_changed(self):
        self.log('模式切换到 %s' %(self.ui_main.comboBox_Mode.currentText()))
    
    def slot_record_start_stop(self):
        self.record.is_recording = not self.record.is_recording
        
        if self.record.is_recording:
            self.ui_main.pushButton_RecordPlay.setEnabled(False)
        else:
            self.ui_main.pushButton_RecordPlay.setEnabled(True)
        
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
        
    def slot_map_refresh(self):
        # f_name, f_filter = QFileDialog.getOpenFileName(self.ui_main, '选择单个文件', './', '筛选条件(*.jpg *.png *.bmp)')
        # print(f_name)
        
        # f_names, f_filter = QFileDialog.getOpenFileNames(self.ui_main, '选择单个或多个文件', './', '筛选条件(*.jpg *.png *.bmp)')
        # print(f_names)
        
        self.log('刷新: %s' %(self.map.dir))
        self.ui_main.lineEdit_MapDir.setText(self.map.dir)
        
        # fs = os.listdir(f_path)                                                                           # 列出路径下所有的文件和文件夹
        fs = [f for f in os.listdir(self.map.dir) if os.path.isfile(os.path.join(self.map.dir, f))]   # 只列出文件
        self.ui_main.listWidget_MapFiles.clear()
        self.ui_main.listWidget_MapFiles.addItems(fs)
        
        self.ui_main.pushButton_MapImport.setEnabled(False)
        self.ui_main.pushButton_MapDelete.setEnabled(False)
    
    def slot_record_play(self):
        self.log('回放 %s' %(self.record.f_path_name))
        df = pd.read_csv(self.record.f_path_name)   # <class 'pandas.core.frame.DataFrame'>
        dc = df.to_dict()                           # <class 'dict'>
        keys = dc.keys()
        keys_list = list(keys)
        num = len(dc[keys_list[0]])
        
        self.record.items_list = []
        
        for i in range(num):
            self.record.item_dict = {}
            for k in keys:
                self.record.item_dict[k] = dc[k][i]
            # print(self.record.item_dict)
            self.record.items_list.append(copy.copy(self.record.item_dict))
        
        print('导入 CSV 成功')
        
        self.update_record_len_scrollbar_and_label()
        self.update_record_view_scrollbar_and_label()
    
    def slot_record_delete(self):
        self.log('删除: %s' %(self.record.f_path_name))
        os.remove(self.record.f_path_name)
        self.slot_record_refresh()
    
    def slot_record_open_dir(self):
        self.record.dir = QFileDialog.getExistingDirectory(self.ui_main, '选择记录文件路径', self.record.dir)
        self.ui_main.lineEdit_RecordDir.setText(self.record.dir)
        self.slot_record_refresh()
    
    def slot_map_open_dir(self):
        self.map.dir = QFileDialog.getExistingDirectory(self.ui_main, '选择记录文件路径', self.map.dir)
        self.ui_main.lineEdit_RecordDir.setText(self.map.dir)
        self.slot_map_refresh()
    
    def slot_map_import(self):
        # 清除绘图
        self.axes_2d_static.clear()
        
        # 打开地图文件
        with open(self.map.f_path_name, encoding='utf-8') as f_map:
            map_str = f_map.read()
        self.map.dict = eval(map_str)
        self.draw_map(self.map.dict, resize=True)
        
        # 重新绘图
        self.axes_2d_static.figure.canvas.draw()
    
    def draw_map(self, map, resize):
        # x, y, w, h = self.ui_main.horizontalLayout_2D.GetGeometry()

        # r = self.ui_main.horizontalLayout_2D.getGeometry()
        # print(r.x())
        # print(r.y())

        # w = self.axes_2d_static.width()
        # h = self.axes_2d_static.height()
        # print(w, h)

        w = self.ui_main.tabWidget_Display.width()
        h = self.ui_main.tabWidget_Display.height()
        print(w, h)

        # print('2D 图形化控件 x:', self.ui_main.horizontalLayout_2D.x())
        # print('2D 图形化控件 y:', self.ui_main.horizontalLayout_2D.y())
        # print('2D 图形化控件 x:', self.axes_2d_static.x())
        # print('2D 图形化控件 y:', self.axes_2d_static.y())

        if 'type' in map:
            if '2d' == map['type']:
                cfg = map['cfg']                # 默认配置
                w, h, bp = map['size']          # 大小、边距比例
                bx = w * bp
                by = h * bp
                
                # 设置视图范围
                if resize:
                    self.axes_2d_static.set_xlim(0-bx, w+bx)
                    self.axes_2d_static.set_ylim(0-by, h+by)
                
                xs = [0, w, w, 0, 0]
                ys = [0, 0, h, h, 0]
                
                # 绘制边界线
                line = mlines.Line2D(xs, ys, linewidth=1, color='r', alpha=cfg['ref']['a'])
                self.axes_2d_static.add_artist(line)
                
                # 绘制基站位置
                if 'anchors' in map:
                    anchors = map['anchors']
                    for k in anchors:
                        anchor = anchors[k]
                        x, y = anchor['xy']
                        
                        if 'c' in anchor:
                            c = anchor['c']
                        else:
                            c = cfg['anchor']['c']
                            
                        if 'ec' in anchor:
                            ec = anchor['ec']
                        else:
                            ec = cfg['anchor']['ec']
                            
                        circle = plt.Circle(xy=(x, y), radius=15, color=c, ec=ec, alpha=cfg['anchor']['a'], picker=5)
                        circle.set_zorder(cfg['anchor']['zo'])
                        self.axes_2d_static.annotate(k, xy=(x, y), fontsize=8, ha='center', va='center', zorder=10)
                        self.axes_2d_static.add_artist(circle)
                
                # 绘制参考线
                if 'lines' in map:
                    lines = map['lines']
                    for k in lines:
                        line = lines[k]
                        
                        xs = []
                        ys = []
                        for xy in line['xy']:
                            x, y = xy
                            xs.append(x)
                            ys.append(y)
                        
                        if 'w' in line:
                            w = line['w']
                        else:
                            w = 1
                        
                        if 'c' in line:
                            c = line['c']
                        else:
                            c = cfg['ref']['c']
                        
                        # Line2D(xdata, ydata, linewidth=None, linestyle=None, color=None, marker=None, markersize=None, markeredgewidth=None, markeredgecolor=None, markerfacecolor=None, markerfacecoloralt='none', fillstyle=None, antialiased=None, dash_capstyle=None, solid_capstyle=None, dash_joinstyle=None, solid_joinstyle=None, pickradius=5, drawstyle=None, markevery=None, **kwargs)
                        line = mlines.Line2D(xs, ys, linewidth=w, color=c, alpha=cfg['ref']['a'])
                        self.axes_2d_static.add_artist(line)
                
                # 绘制参考矩形
                if 'rectangles' in map:
                    rectangles = map['rectangles']
                    for k in rectangles:
                        rectangle = rectangles[k]
                        
                        x, y, w, h, a = rectangle['xywha']
                        
                        if 'c' in rectangle:
                            c = rectangle['c']
                        else:
                            c = cfg['ref']['c']
                            
                        if 'ec' in rectangle:
                            ec = rectangle['ec']
                        else:
                            ec = cfg['ref']['ec']
                        
                        rectangle = mpatches.Rectangle(xy=(x, y), width=w, height=h, angle=a, fc=c, ec=ec, alpha=cfg['ref']['a'], picker=5)
                        rectangle.set_zorder(cfg['ref']['zo'])
                        # self.axes_2d_static.annotate(k, xy=(x, y), fontsize=8, ha='center', va='center')
                        self.axes_2d_static.add_patch(rectangle)
        else:
            self.log('无法正确加载地图，请检查地图文件格式')
            
    def slot_record_select(self, f_name):
        self.record.f_path_name = self.record.dir + r'/' + f_name
        self.log(self.record.f_path_name)
        if self.record.is_recording:
            self.ui_main.pushButton_RecordPlay.setEnabled(False)
        else:
            self.ui_main.pushButton_RecordPlay.setEnabled(True)
            
        self.ui_main.pushButton_RecordDelete.setEnabled(True)
    
    def slot_map_select(self, f_name):
        self.map.f_path_name = self.map.dir + r'/' + f_name
        self.log(self.map.f_path_name)
        
        self.ui_main.pushButton_MapImport.setEnabled(True)
        self.ui_main.pushButton_MapDelete.setEnabled(True)
    
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
        
    def slot_checkbox_record_view_all_changed(self, sta):
        if 0 == sta:    # 不选中
            self.ui_main.checkbox_graphic_all.setStyleSheet('background-color:rgb(240, 240, 240)')
        elif 2 == sta:  # 选中
            self.ui_main.checkbox_graphic_all.setStyleSheet('background-color:gray')
        
        self.update_record_view_scrollbar_and_label()
    
    def slot_checkbox_record_view_track_changed(self, sta):
        if 0 == sta:    # 不选中
            self.ui_main.checkbox_graphic_track.setStyleSheet('background-color:rgb(240, 240, 240)')
        elif 2 == sta:  # 选中
            self.ui_main.checkbox_graphic_track.setStyleSheet('background-color:gray')
        
        self.ui_main.horizontalScrollBar_Graphic.setValue(self.ui_main.horizontalScrollBar_Graphic.maximum())
        
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
        
    def slot_port_name_currentIndexChanged(self, idx):
        if(len(self.port.valid) > 0):
            self.log(self.port.valid[idx])
            
    def slot_port_name_highlighted(self, idx):
        # print('highlighted id = ', idx)
        if(len(self.port.valid) > 0):
            self.log(self.port.valid[idx])
            
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
        else:
            self.log('端口未打开！')
    
    def slot_dock_show_hide(self, dock_set, is_checked):
        dock_set.setVisible(is_checked)
    
    def update_uart_rx(self):
        if self.port.isopen:
            self.uart_rx_handle()
    
    def update_record_text_info(self, item_dict):
        pkg_stamp = item_dict['stamp']
        
        pkg_info = ' T(%d, %d)' %(item_dict['x'], item_dict['y'])
        pkg_info += ' D(%d, %d, %d)' %(item_dict['d0'], item_dict['d1'], item_dict['d2'])
        pkg_info += ' R(%d, %d, %d)' %(item_dict['r0'], item_dict['r1'], item_dict['r2'])
        
        pkg_raw = item_dict['raw']
        # for v in item_dict['raw']:
        #     pkg_raw += ' %02X' %(v)
        
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
                            self.update_record_text_info(self.record.item_dict)   # copy.copy(...)
                            
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
    
    def update_record_graphic(self):
        if (self.drawed_end != self.record.view_max) or (self.drawed_len != self.record.view_len):
            
            # 清除当前绘图
            self.axes_2d_static.clear()
            
            if self.record.view_len > 0:
                # 取出需要绘制的数据包
                records = self.record.items_list[self.record.view_min-1 : self.record.view_max]   # 需要绘制的所有记录
                record = self.record.items_list[self.record.view_max - 1]                       # 需要绘制的最后一条记录
            
                # 绘制所有记录中 标签位置点
                for i in range(self.record.view_len):
                    a = 1.0 / self.record.view_len * i
                    circle = plt.Circle((records[i]['x'], records[i]['y']), radius=3, color='c', ec='c', alpha=a, picker=5)
                    self.axes_2d_static.add_artist(circle)
                
                # 更新数据包内容文本
                self.update_record_text_info(record)
                
                map = self.map.dict
                # 绘制地图
                self.draw_map(map, resize=True)
                
                if 'type' in map:
                    if '2d' == map['type']:
                        cfg = map['cfg']                # 默认配置
                        if 'anchors' in map:
                            anchors = map['anchors']
                            for k in anchors:
                                anchor = anchors[k]
                                x, y = anchor['xy']
                                
                                # 绘制最后一条记录中 距离圆
                                key_d = 'd%d' %(k)
                                circle = plt.Circle((x, y), radius=record[key_d], color=anchor['c'], ec='c', alpha=cfg['distance']['a'], picker=5)
                                circle.set_zorder(cfg['distance']['zo'])
                                self.axes_2d_static.add_artist(circle)
                                
                                # 绘制最后一条记录中 信号圆
                                key_r = 'r%d' %(k)
                                circle = plt.Circle((x, y), radius=record[key_r], color=cfg['rssi']['c'], ec='c', alpha=cfg['rssi']['a'], picker=5)
                                circle.set_zorder(cfg['rssi']['zo'])
                                self.axes_2d_static.add_artist(circle)
            
            self.axes_2d_static.figure.canvas.draw()    # 重新绘制
            
            self.drawed_end = self.record.view_max
            self.drawed_len = self.record.view_len

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