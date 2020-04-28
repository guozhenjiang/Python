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

# --------------------------------------------------
csv_data_str = []                       # <class 'list'>

csv_file = open('./vhub/raw.csv', 'r')
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
csv_data_int = np.zeros([csv_row_num, csv_col_num], dtype=int)  # <class 'numpy.ndarray'>

row_cnt = 0
for row in csv_data_str:
    # print(['{:05d}'.format(int(x)) for x in row])             # 格式化输出 CSV 文件行内容
    col_cnt = 0
    for col in row:
        # print('row=%03d col=%03d' %(row_cnt, col_cnt))
        csv_data_int[row_cnt][col_cnt] = int(col)
        col_cnt += 1
    row_cnt += 1

print(csv_data_int)                                             # 输出从 CSV 提取的数据

csv_row_ppg_num = 14
csv_ppg_val = csv_data_int[..., 1:]     # 通过切片获取实际数据部分 去掉了帧序列号

# --------------------------------------------------
port = 'COM3'                           # 端口
baudrate = 1000000                      # 波特率

pkg_len = 34                            # 每包字节数
pkg_ppg_len = 28                        # 每包有多少字节 PPG 数据
pkg_ppg_num = 14                        # 每包有多少个 PPG 数据
win_pkg_num = 40                        # 窗口显示多少个包
win_len = pkg_ppg_num * win_pkg_num     # 窗口大小

cnt_receive = 0                         # 收到的新的字节往 data_pkg 存放的下标
cnt_csv_line = 0

data_pkg = np.zeros(pkg_len, dtype=int, order='C')          # 新包缓存
data_ppg = np.zeros(pkg_ppg_len, dtype=int, order='C')      # 新包中的 PPG 原始数据
ppg_val = np.zeros(pkg_ppg_num, dtype=int, order='C')  # 新包中的 PPG 提取数据
data_win = np.zeros(int(win_len), dtype=int, order='C')     # 窗口显示内容缓存

try:
    print('looking for %s, %d' %(port, baudrate))
    serialport = serial.Serial(port, int(baudrate), timeout=1, parity=serial.PARITY_NONE)
except:
    print("com open failed")
else:
    print("%s open success" %(serialport.name))

print()

app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Python小组演示-滤波")
win.resize(1600, 900)

pg.setConfigOptions(antialias=True)

# p1.addLegend()
# p1.addLegend(legend.loc="topright", legend.names=c("raw","filter"),lty = 1, col=colvec, text.col=colvec, bg="white", bty=1)

p1 = win.addPlot(title="原始数据")#, colspan=1)
p1.setWindowTitle('P1 Win Title')
p1.setRange(QtCore.QRectF(0, -10, win_len, 20)) 
p1.setLabel('bottom', 'Index', units='B')

win.nextRow()

p2 = win.addPlot(title="滤波后数据")#, colspan=1)
p2.setWindowTitle('P2 Win Title')
p2.setRange(QtCore.QRectF(0, -10, win_len, 20)) 
p2.setLabel('bottom', 'Index', units='B')

win.nextRow()

p3 = win.addPlot(title="不同滤波参数对比")#, colspan=1)#colspan=2)
p3.setWindowTitle('P3 Win Title')
p3.setRange(QtCore.QRectF(0, -10, win_len, 20)) 
p3.setLabel('bottom', 'Index', units='B')

# curve_raw = p1.plot(pen=(255,0,0), symbol='raw',       name="R curve_raw")
curve_raw = p1.plot(pen=(255,0,0), symbolBrush=(0,0,200), symbolPen='w', symbol='o', symbolSize=5, name="raw")
curve_filter = p2.plot(pen=(0,255,0), name="filter")

curve_compare_raw = p3.plot(pen=(255,255,255, 120))
curve_compare_filter1 = p3.plot(pen=(0,255,0, 255))
curve_compare_filter2 = p3.plot(pen=(0,100,255, 255))
curve_compare_filter3 = p3.plot(pen=(255,255,0, 255))
curve_compare_filter4 = p3.plot(pen=(255,255,255, 255))

lastTime = time()
fps = None

def update_ui_by_uart():
    global curve_raw, p1, lastTime, fps, data_win, cnt_receive
    
    if(serialport.inWaiting()):
        data_pkg[cnt_receive] = int.from_bytes(serialport.read(), byteorder='big', signed=False)
        # print(data_pkg[cnt_receive])
        
        if(     ((0 == cnt_receive) and (0xFF != data_pkg[cnt_receive]))\
            or  ((1 == cnt_receive) and (0x02 != data_pkg[cnt_receive]))\
            or  ((2 == cnt_receive) and (0x00 != data_pkg[cnt_receive]))\
            or  ((3 == cnt_receive) and (0x00 != data_pkg[cnt_receive]))    ):
            cnt_receive = 0                                         # 发生错位 重新寻找包头
        
        else:                                                       # 正常接收中
            cnt_receive  += 1
            if(cnt_receive >= pkg_len):                             # 收到一个新的完整的包
                # print(['{:02X}'.format(x) for x in data_pkg])     # 格式化输出 整个包
                cnt_receive = 0
                
                data_ppg = data_pkg[(pkg_len-pkg_ppg_len):]
                
                for i in range(int(pkg_ppg_num)):
                    ppg_val[i] = data_ppg[i * 2 + 0]
                    ppg_val[i] <<= 8
                    ppg_val[i] |= data_ppg[i * 2 + 1]
                    
                    # print(['{:05d}'.format(x) for x in ppg_val])   # 格式化输出 PPG 数据
                
                data_win = data_win[pkg_ppg_num:] # 通过切片给新数据腾出位置
                data_win = np.append(data_win, ppg_val)
                
                curve_raw.setData(data_win)                             # 更新原始数据波形
                
                # curve_filter.setData(data_win + 100)
                b, a = signal.butter(10, 0.5, 'lowpass')  
                filterData1 = signal.filtfilt(b, a, data_win)
                
                b, a = signal.butter(10, 0.2, 'lowpass')  
                filterData2 = signal.filtfilt(b, a, data_win)
                
                b, a = signal.butter(10, 0.1, 'lowpass')  
                filterData3 = signal.filtfilt(b, a, data_win)
                
                # print(type(filterData3))    # <class 'numpy.ndarray'>
                
                filterData3_avg = np.average(filterData3)
                filterData3_max = np.amax(filterData3)
                filterData3_min = np.amin(filterData3)
                
                det_p = filterData3_max - filterData3_avg
                det_n = filterData3_avg - filterData3_min
                
                curve_filter.setData(filterData2)                       # 更新滤波后波形
                
                curve_compare_raw.setData(data_win)                     # 更新比较中的 原始波形
                curve_compare_filter1.setData(filterData1)              # 更新比较中的 滤波参数效果 1
                # curve_compare_filter2.setData(filterData2)              # 更新比较中的 滤波参数效果 2
                # curve_compare_filter3.setData(filterData3)              # 更新比较中的 滤波参数效果 3
                
                curve_compare_filter2.setData(filterData2 - 100)
                curve_compare_filter3.setData(filterData3 - 200)
    
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    # p1.setTitle('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot

index_cvs_row = 0

def update_ui_by_csv():
    global curve_raw, p1, lastTime, fps, data_win, cnt_receive, index_cvs_row
                
    data_win = data_win[pkg_ppg_num:] # 通过切片给新数据腾出位置
    data_win = np.append(data_win, csv_ppg_val[index_cvs_row])
    index_cvs_row += 1
    if(index_cvs_row >= csv_row_num):
        index_cvs_row = 0
    
    curve_raw.setData(data_win)                             # 更新原始数据波形
    
    # curve_filter.setData(data_win + 100)
    b, a = signal.butter(10, 0.5, 'lowpass')  
    filterData1 = signal.filtfilt(b, a, data_win)
    
    b, a = signal.butter(10, 0.2, 'lowpass')  
    filterData2 = signal.filtfilt(b, a, data_win)
    
    b, a = signal.butter(10, 0.1, 'lowpass')  
    filterData3 = signal.filtfilt(b, a, data_win)
    
    # print(type(filterData3))    # <class 'numpy.ndarray'>
    
    filterData3_avg = np.average(filterData3)
    filterData3_max = np.amax(filterData3)
    filterData3_min = np.amin(filterData3)
    
    det_p = filterData3_max - filterData3_avg
    det_n = filterData3_avg - filterData3_min
    
    curve_filter.setData(filterData2)                       # 更新滤波后波形
    
    curve_compare_raw.setData(data_win)                     # 更新比较中的 原始波形
    # curve_compare_filter1.setData(filterData1)              # 更新比较中的 滤波参数效果 1
    
    curve_compare_filter2.setData(filterData2)              # 更新比较中的 滤波参数效果 2
    curve_compare_filter3.setData(filterData3)              # 更新比较中的 滤波参数效果 3
    # curve_compare_filter2.setData(filterData2 - 100)
    # curve_compare_filter3.setData(filterData3 - 200)
    
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    # p1.setTitle('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot

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