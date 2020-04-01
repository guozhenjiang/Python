#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
from scipy import signal
import pyqtgraph.widgets.RemoteGraphicsView

# ----------------------------------------------------------------------------------------------------
# 加载文件
# ----------------------------------------------------------------------------------------------------
class Record:
    def __init__(self, filename):
        super().__init__()
        self.data = []
        self.data_len = 0
        self.open_txt(filename)
        self.txt_to_list()
    
    def open_txt(self, name):
        txt_r = open(name)
        txt = txt_r.read()
        txt = txt.strip()
        txt = txt.split(' ')
        self.txt = txt
        txt_r.close()
    
    def txt_to_list(self):
        data_tmp = []
        len = 0
        
        for v in self.txt:
            len += 1
            val = int(v, 16)
            data_tmp.append(val)
        
        self.data_len = len / 2
        
        for i in range(int(0), int(self.data_len)):
            val_H = data_tmp[2*i + 0]
            val_L = data_tmp[2*i + 1]
            val = (val_H << 8) + val_L
            self.data.append(val)
        
        self.max = max(self.data)
        self.min = min(self.data)

# file_r = open('./data/record_01_无遮挡2m.txt')
# content_raw = file_r.read()
# file_r.close()
# # print('\r\n%s:\r\n' %(file_r.name), content_raw)

# content_strip = content_raw.strip()             # 删除字符串左边和末尾的空格
# content = content_strip.split(' ')

# data_tmp = []
# data_len = 0
# byte_num = 0

# for v in content:
#     byte_num += 1
#     val = int(v, 16)
#     data_tmp.append(val)

# data_len = byte_num / 2                         # 真实数据两字节 先低后高

# data = []                                       # 列表
# data_min = 0
# data_max = 0

# for i in range(int(0), int(data_len)):
#     Val_L = data_tmp[2*i + 0]
#     Val_H = data_tmp[2*i + 1]
#     Val = (Val_H <<8) + Val_L
#     # print('%02X %02X->(%05d)' %(Val_H, Val_L, Val))     # 打印提取数据的详细过程
#     data.append(Val)

# data_max = max(data)
# data_min = min(data)

# ----------------------------------------------------------------------------------------------------
# 波形显示
# ----------------------------------------------------------------------------------------------------
app = QtGui.QApplication([])

win = pg.GraphicsWindow(title = '室内定位点到点数据滤波')
win.title = "hello"
win.resize(1000, 600)

pg.setConfigOptions(antialias = True)

cb_raw_wave = QtGui.QCheckBox('对比图散开')
cb_raw_wave.setChecked(False)

cb_stop = QtGui.QCheckBox('暂停')
cb_stop.setChecked(False)

layout = pg.LayoutWidget()
layout.addWidget(cb_raw_wave, row=0, col=0)
layout.addWidget(cb_stop, row=0, col=1)
layout.addWidget(win, row=1, col=0, rowspan=1, colspan=2)
layout.show()

win_len = 100                                           # 窗口大小
win_data = np.zeros(int(win_len), dtype=int, order='C') # 窗口显示内容缓存
win_data_append = np.zeros(int(1), dtype=int, order='C')
idx_val = 0

# ----------------------------------------------------------------------------------------------------
# 初始数据
# ----------------------------------------------------------------------------------------------------
record = Record('./data/record_01_无遮挡2m.txt')

idx_val = 0
for i in range(win_len):
    win_data[i] = record.data[idx_val]
    idx_val +=1
    if(idx_val >= win_len):
        idx_val = 0

# -------------------- plot_raw
p_raw = win.addPlot(title = '原始数据', row=0, col=0, rowspan=1, colspan=1)
p_raw.setWindowTitle('P_RAW Win Title')
p_raw.setRange(QtCore.QRectF(0, record.min, win_len, record.max))
p_raw.setLabel('bottom', 'Index', units='B')
p_raw.setAutoPan(y=False)
# p_raw.addLegend()

# win.nextRow()
# -------------------- plot_after_filter
p_flt = win.addPlot(title = '滤波后数据', row=1, col=0, rowspan=1, colspan=1)
# p_flt.setAutoPan(y=True)
p_flt.setWindowTitle('P_FLT Win Title')
p_flt.setRange(QtCore.QRectF(0, record.min, win_len, record.max))
p_flt.setLabel('bottom', 'Index', units='B')
# p_flt.addLegend()

# win.nextRow()
# -------------------- plot_compare
p_cmp = win.addPlot(title = '不同滤波参数效果对比', row=2, col=0, rowspan=2, colspan=1)
p_cmp.setAutoPan(y=True)
p_cmp.setWindowTitle('P_CMP Win Title')
p_cmp.setRange(QtCore.QRectF(0, record.min, win_len, record.max))
p_cmp.setLabel('bottom', 'Index', units='B')
p_cmp.addLegend()

# curve_raw = p_raw.plot(pen=(255,0,0), symbol='raw',       name="R curve_raw")
curve_raw = p_raw.plot(pen=(255,0,0), symbolBrush=(0,0,100), symbolPen='w', symbol='o', symbolSize=5, name="原始数据")
curve_flt = p_flt.plot(pen=(0,255,0), name='滤波参数')
curve_cmp_raw = p_cmp.plot(pen=(255,255,255, 120), name=". 原始波形")
curve_cmp_0_50 = p_cmp.plot(pen=(0,255,0, 255), name=". 参数 0.5")
curve_cmp_0_20 = p_cmp.plot(pen=(0,100,255, 255), name=". 参数 0.2")
curve_cmp_0_10 = p_cmp.plot(pen=(255,255,0, 255), name=". 参数 0.1")

win.nextRow()

lastTime = time()
fps = None

# ----------------------------------------------------------------------------------------------------
# 显示更新
# ----------------------------------------------------------------------------------------------------
def update_ui():
    global win_data, curve_cmp_raw, curve_cmp_0_50, curve_cmp_0_20, curve_cmp_0_10, lastTime, fps, cb_raw_wave
    
    b, a = signal.butter(10, 0.50, 'lowpass')  
    filter_data_0_50 = signal.filtfilt(b, a, win_data)
    
    b, a = signal.butter(10, 0.20, 'lowpass')  
    filter_data_0_20 = signal.filtfilt(b, a, win_data)
    
    b, a = signal.butter(10, 0.10, 'lowpass')  
    filter_data_0_10 = signal.filtfilt(b, a, win_data)
    
    b, a = signal.butter(10, 0.09, 'lowpass')
    filter_data = signal.filtfilt(b, a, win_data)
    
    # filter_data = filter_data
    filter_data = filter_data_0_10
    
    curve_raw.setData(win_data)                     # 更新原始数据波形
    
    curve_flt.setData(filter_data)                  # 更新滤波后波形
    
    if(cb_raw_wave.isChecked()):                    # 对比图散开
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

# ---------------------------------------- UI 更新
def update_ui_from_txt():
    global win_data, cb_stop, idx_val, win_data_append

    if(not cb_stop.isChecked()):
        win_data_append[0] = record.data[idx_val]
        # print(win_data_append[0])
        
        win_data = win_data[1:]
        win_data = np.append(win_data, win_data_append)
        
        # print(['{:03d}'.format(int(x)) for x in win_data])
        
        idx_val += 1
        if(idx_val >= record.data_len):
            idx_val = 0
        
        update_ui()

# timer = QtCore.QTimer()
# timer.timeout.connect(update_ui_by_uart)
# timer.start(0)

timer = QtCore.QTimer()
timer.timeout.connect(update_ui_from_txt)
timer.start(50)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()