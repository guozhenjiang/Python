#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import csv

port = 'COM3'                       # 端口
baudrate = 1000000                  # 波特率

len_pkg = 34                        # 每包字节数
len_ppg = 28                        # 每包有多少字节 PPG 数据

num_ppg = len_ppg / 2               # 每包有多少个 PPG 数据

num_pkg = 3                        # 窗口显示多少个包
len_win = num_ppg * num_ppg         # 窗口大小

cnt_receive = 0
cnt_win = 0

data_win = np.zeros(int(len_win), dtype=int, order='C')   # 窗口中显示的数据的存储区
data_pkg = np.zeros(len_pkg, dtype=int, order='C')
data_ppg = np.zeros(len_ppg, dtype=int, order='C')

ppg_val = np.zeros(int(num_ppg), dtype=int, order='C')

try:
    print('looking for %s, %d' %(port, baudrate))
    serialport = serial.Serial(port, int(baudrate), timeout=1, parity=serial.PARITY_NONE)
except:
    print("com open failed")
else:
    print("%s open success" %(serialport.name))

print()

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('pyqtgraph example: PlotSpeedTest')
p.setRange(QtCore.QRectF(0, -10, len_win, 20)) 
p.setLabel('bottom', 'Index', units='B')
curve = p.plot()

# data = np.random.normal(size=(50, len_win))     # size = 50 * 5000 = 250000

lastTime = time()
fps = None

def update_ui():
    global curve, p, lastTime, fps, data_win, cnt_receive
    
    if(serialport.inWaiting()):
        data_pkg[cnt_receive] = int.from_bytes(serialport.read(), byteorder='big', signed=False)
        # print(data_pkg[cnt_receive])
        
        # 发生错位
        if(     ((0 == cnt_receive) and (0xFF != data_pkg[cnt_receive]))\
            or  ((1 == cnt_receive) and (0x02 != data_pkg[cnt_receive]))\
            or  ((2 == cnt_receive) and (0x00 != data_pkg[cnt_receive]))\
            or  ((3 == cnt_receive) and (0x00 != data_pkg[cnt_receive]))    ):
            cnt_receive = 0
        
        # 正常接收中
        else:
            cnt_receive  += 1
            if(cnt_receive >= len_pkg):                         # 收到一个新的完整的包
                # print(['{:02X}'.format(x) for x in data_pkg])   # 格式化输出
                cnt_receive = 0
                
                data_ppg = data_pkg[(len_pkg-len_ppg):]
                
                for i in range(int(num_ppg)):
                    ppg_val[i] = data_ppg[i * 2 + 0]
                    ppg_val[i] <<= 8
                    ppg_val[i] |= data_ppg[i * 2 + 1]
                    
                    # print(['{:05d}'.format(x) for x in ppg_val])   # 格式化输出
                    
                data_win = data_win[1:] # 通过切片给新数据腾出位置
                data_win = np.append(data_win, ppg_val[i])
                
                curve.setData(data_win)
            
    
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    p.setTitle('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot

timer = QtCore.QTimer()
timer.timeout.connect(update_ui)
timer.start(0)

# def update_data():
    

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()