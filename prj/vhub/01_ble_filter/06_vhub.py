#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
scipy.signal.butter
    https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.butter.html
'''

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import csv
from scipy import signal
import pyqtgraph.widgets.RemoteGraphicsView

# ---------------------------------------- cfg

# ---------------------------------------- CSV
csv_data_str = []                       # <class 'list'>

csv_file = open('./vhub/ppg_03.csv', 'r')
csv_line = csv_file.readline()          # <class 'str'>
while csv_line:
	csv_line = csv_line.strip()			# 去除空格换行等字符
	csv_line = csv_line.split(',')		# 按照逗号分组
	
	arr = list(map(int, csv_line))      # 将stringList转为一维数组
	csv_data_str.append(arr)
	csv_line = csv_file.readline()
csv_file.close

csv_row_num = len(csv_data_str)
csv_col_num = len(csv_data_str[0])
print('row=%d col=%d' %(csv_row_num, csv_col_num))

csv_data_int = np.zeros([csv_row_num, csv_col_num], dtype=int)  # <class 'numpy.ndarray'>

row_cnt = 0
for row in csv_data_str:
    # print(['{:05d}'.format(int(x)) for x in row])     # 格式化输出 CSV 文件行内容
    col_cnt = 0
    for col in row:
        # print('row=%03d col=%03d' %(row_cnt, col_cnt))
        csv_data_int[row_cnt][col_cnt] = int(col)
        col_cnt += 1
    row_cnt += 1

print(csv_data_int)     # 输出从 CSV 提取的数据

csv_row_ppg_num = 14
csv_ppg_val = csv_data_int[..., 1:]     # 通过切片获取实际数据部分 去掉了帧序列号

# ---------------------------------------- UART
uart_port = 'COM3'          # 端口
uart_baud = 1000000         # 波特率

uart_pkg_len = 34           # 每包字节数
uart_ppg_len = 28           # 每包有多少字节 PPG 数据
uart_ppg_num = 14           # 每包有多少个 PPG 数据

uart_byte_in_pkg_index = 0  # 收到的新的字节往 uart_pkg 存放的下标

uart_pkg = np.zeros(uart_pkg_len, dtype=int, order='C')         # 新包缓存
uart_ppg_data = np.zeros(uart_ppg_len, dtype=int, order='C')    # 新包中的 PPG 原始数据
uart_ppg = np.zeros(uart_ppg_num, dtype=int, order='C')         # 新包中的 PPG 提取数据

try:
    print('looking for %s, %d' %(uart_port, uart_baud))
    serialport = serial.Serial(uart_port, int(uart_baud), timeout=1, parity=serial.PARITY_NONE)
except:
    print("com open failed")
else:
    print("%s open success" %(serialport.name))

print()

# ---------------------------------------- 显示窗口
win_pkg_num = 40                                        # 窗口显示多少个包
win_len = uart_ppg_num * win_pkg_num                    # 窗口大小
win_data = np.zeros(int(win_len), dtype=int, order='C') # 窗口显示内容缓存

app = QtGui.QApplication([])

cb_keepout = QtGui.QCheckBox('对比图散开')
cb_keepout.setChecked(False)
win = pg.GraphicsWindow(title = 'Python小组演示-滤波')
win.resize(1000, 600)

layout = pg.LayoutWidget()
layout.addWidget(cb_keepout)
layout.addWidget(win, row=1, col=0, rowspan=1, colspan=1)
layout.show()

# -------------------- plot_raw
pg.setConfigOptions(antialias = True)

p_raw = win.addPlot(title = '原始数据', row=0, col=0, rowspan=1, colspan=1)
# p_raw.setAutoPan(y = True)
p_raw.setWindowTitle('P_RAW Win Title')
p_raw.setRange(QtCore.QRectF(0, -10, win_len, 20)) 
p_raw.setLabel('bottom', 'Index', units='B')
# p_raw.addLegend()

# win.nextRow()
# -------------------- plot_after_filter
p_flt = win.addPlot(title = '滤波后数据', row=1, col=0, rowspan=1, colspan=1)
# p_flt.setAutoPan(y=True)
p_flt.setWindowTitle('P_FLT Win Title')
p_flt.setRange(QtCore.QRectF(0, -10, win_len, 20)) 
p_flt.setLabel('bottom', 'Index', units='B')
# p_flt.addLegend()

# win.nextRow()
# -------------------- plot_compare
p_cmp = win.addPlot(title = '不同滤波参数效果对比', row=4, col=0, rowspan=2, colspan=1)
# p_cmp.setAutoPan(y=True)
p_cmp.setWindowTitle('P_CMP Win Title')
p_cmp.setRange(QtCore.QRectF(0, -10, win_len, 20)) 
p_cmp.setLabel('bottom', 'Index', units='B')
p_cmp.addLegend()

# curve_raw = p_raw.plot(pen=(255,0,0), symbol='raw',       name="R curve_raw")
curve_raw = p_raw.plot(pen=(255,0,0), symbolBrush=(0,0,100), symbolPen='w', symbol='o', symbolSize=5, name="原始数据")
curve_flt = p_flt.plot(pen=(0,255,0), name='滤波参数')
curve_cmp_raw = p_cmp.plot(pen=(255,255,255, 120), name=". 原始波形")
curve_cmp_0_50 = p_cmp.plot(pen=(0,255,0, 255), name=". 参数 0.5")
curve_cmp_0_20 = p_cmp.plot(pen=(0,100,255, 255), name=". 参数 0.2")
curve_cmp_0_10 = p_cmp.plot(pen=(255,255,0, 255), name=". 参数 0.1")

lastTime = time()
fps = None

def update_ui():
    global win_data, curve_cmp_raw, curve_cmp_0_50, curve_cmp_0_20, curve_cmp_0_10, lastTime, fps, cb_keepout
    
    b, a = signal.butter(10, 0.50, 'lowpass')  
    filter_data_0_50 = signal.filtfilt(b, a, win_data)
    
    b, a = signal.butter(10, 0.20, 'lowpass')  
    filter_data_0_20 = signal.filtfilt(b, a, win_data)
    
    b, a = signal.butter(10, 0.10, 'lowpass')  
    filter_data_0_10 = signal.filtfilt(b, a, win_data)
    
    curve_raw.setData(win_data)                         # 更新原始数据波形
    
    curve_flt.setData(filter_data_0_20)                 # 更新滤波后波形
    
    if(cb_keepout.isChecked()):                         # 对比图散开
        curve_cmp_raw.setData(win_data + 500)
        curve_cmp_0_50.setData(filter_data_0_50)
        curve_cmp_0_20.setData(filter_data_0_20 - 300)
        curve_cmp_0_10.setData(filter_data_0_10 - 500)
    else:
        curve_cmp_raw.setData(win_data)                 # 对比图集中
        curve_cmp_0_50.setData(filter_data_0_50)
        curve_cmp_0_20.setData(filter_data_0_20)
        curve_cmp_0_10.setData(filter_data_0_10)
    
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    # p_raw.setTitle('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot

# ---------------------------------------- UART 处理
def update_ui_by_uart():
    global win_data, uart_byte_in_pkg_index
    
    if(serialport.inWaiting()):
        uart_pkg[uart_byte_in_pkg_index] = int.from_bytes(serialport.read(), byteorder='big', signed=False)
        # print(uart_pkg[uart_byte_in_pkg_index])
        
        if(     ((0 == uart_byte_in_pkg_index) and (0xFF != uart_pkg[uart_byte_in_pkg_index]))\
            or  ((1 == uart_byte_in_pkg_index) and (0x02 != uart_pkg[uart_byte_in_pkg_index]))\
            or  ((2 == uart_byte_in_pkg_index) and (0x00 != uart_pkg[uart_byte_in_pkg_index]))\
            or  ((3 == uart_byte_in_pkg_index) and (0x00 != uart_pkg[uart_byte_in_pkg_index]))    ):
            uart_byte_in_pkg_index = 0                                  # 发生错位 重新寻找包头
        
        else:                                                           # 正常接收中
            uart_byte_in_pkg_index  += 1
            if(uart_byte_in_pkg_index >= uart_pkg_len):                 # 收到一个新的完整的包
                # print(['{:02X}'.format(x) for x in uart_pkg])         # 格式化输出 整个包
                uart_byte_in_pkg_index = 0
                
                uart_ppg_data = uart_pkg[(uart_pkg_len-uart_ppg_len):]
                
                for i in range(int(uart_ppg_num)):
                    uart_ppg[i] = uart_ppg_data[i * 2 + 0]
                    uart_ppg[i] <<= 8
                    uart_ppg[i] |= uart_ppg_data[i * 2 + 1]
                    
                    # print(['{:05d}'.format(x) for x in uart_ppg])     # 格式化输出 PPG 数据
                
                win_data = win_data[uart_ppg_num:]                      # 通过切片给新数据腾出位置
                win_data = np.append(win_data, uart_ppg)
                
                update_ui()

# ---------------------------------------- CSV 处理
index_cvs_row = 0
def update_ui_by_csv():
    global win_data, index_cvs_row

    win_data = win_data[uart_ppg_num:] # 通过切片给新数据腾出位置
    win_data = np.append(win_data, csv_ppg_val[index_cvs_row])
    
    # print(index_cvs_row)
    index_cvs_row += 1
    if(index_cvs_row >= csv_row_num):
        index_cvs_row = 0
    
    update_ui()

# timer = QtCore.QTimer()
# timer.timeout.connect(update_ui_by_uart)
# timer.start(0)

timer = QtCore.QTimer()
timer.timeout.connect(update_ui_by_csv)
timer.start(100)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()