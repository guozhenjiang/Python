#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import csv

port = 'COM3'                                           # 端口
baudrate = 115200                                       # 波特率

pkg_len = 32                                            # 每包字节数
pkg_display_num = 100                                   # 窗口显示多少个包
window_len = pkg_len * pkg_display_num                  # 窗口大小

data_buf = np.zeros(window_len, dtype=int, order='C')   # 窗口中显示的数据的存储区

# --------------------------------------------------
col_num = 34
line_num = 0
for line in open('./vhub/ppg.txt', 'r'):
    line_num += 1

raw_data = np.array([line_num, col_num])
raw_line = []

line_cnt = 0
str = ''
for line in open('./vhub/ppg.txt', 'r'):        # 按行提取
    line_str = line[:-1]                        # 截取行中指定部分 <class 'str'>
    # print(line_str)
    
    print(bytearray.fromhex(line_str))
    
    # raw_data[line_cnt] = bytearray.fromhex(line_str)
    
    # line_str_split = line_str.split(' ')        # 以空格为条件分割为十六进制对应的字符串
    
    # col = 0
    # for line_str_split_item in line_str_split:  # 将每个分割项转换成对应数值
    #     raw_line.append(int(line_str_split_item, base=16))
    
    # raw_data[line_cnt] = raw_line
    
    # raw_str.append(line[:-1])
    # str = line[:-1]
    # print(str)
    
    # print(eval(str))
    # raw_data[line_cnt] = eval(line[:-1])
    line_cnt += 1

# print()
# print(raw_str)

# data_array = np.array(data)
# data_array.reshape(line_cnt, 32)

# print(data_array)

# # --------------------------------------------------
# csv_ppg = open('.\csv_ppg.csv', 'w', newline='')
# writer = csv.writer(csv_ppg)

# try:
#     print('looking for %s, %d' %(port, baudrate))
#     serialport = serial.Serial(port, int(baudrate), timeout=1, parity=serial.PARITY_NONE)
# except:
#     print("com open failed")
# else:
#     print("%s open success" %(serialport.name))

# print()

# app = QtGui.QApplication([])

# p = pg.plot()
# p.setWindowTitle('pyqtgraph example: PlotSpeedTest')
# p.setRange(QtCore.QRectF(0, -10, window_len, 20)) 
# p.setLabel('bottom', 'Index', units='B')
# curve = p.plot()

# data = np.random.normal(size=(50, window_len))     # size = 50 * 5000 = 250000

# lastTime = time()
# fps = None

# def update():
#     global curve, data, p, lastTime, fps, data_buf
    
#     byte_to_read = serialport.inWaiting()
#     if(byte_to_read):                       # 若有串口数据待读取
#         data_buf = data_buf[byte_to_read:]  # 通过切片给新数据腾出位置
        
#         for i in range(byte_to_read):
#             # 追加新数据到数组中
#             data_buf = np.append(data_buf, int.from_bytes(serialport.read(), byteorder='big', signed=False))
        
#         curve.setData(data_buf)
    
#     now = time()
#     dt = now - lastTime
#     lastTime = now
#     if fps is None:
#         fps = 1.0/dt
#     else:
#         s = np.clip(dt*3., 0, 1)
#         fps = fps * (1-s) + (1.0/dt) * s
#     p.setTitle('%0.2f fps' % fps)
#     app.processEvents()  ## force complete redraw for every plot

# timer = QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(0)

# ## Start Qt event loop unless running in interactive mode.
# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         # if(serialport.isOpen()):
#         #     serialport.close()
#         # csv_ppg.close()
#         QtGui.QApplication.instance().exec_()