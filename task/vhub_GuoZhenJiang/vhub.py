#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Test the speed of rapidly updating multiple plot curves
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

import serial
port = 'COM3'
baudrate = 115200

try:
    print('looking for %s, %d' %(port, baudrate))
    serialport = serial.Serial(port, int(baudrate), timeout=1, parity=serial.PARITY_NONE)
except:
    print("com open failed")
else:
    print("%s open success" %(serialport.name))

print()

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])

#mw = QtGui.QMainWindow()
#mw.resize(800,800)

p = pg.plot()
p.setWindowTitle('pyqtgraph example: MultiPlotSpeedTest')
#p.setRange(QtCore.QRectF(0, -10, 5000, 20)) 
p.setLabel('bottom', 'Index', units='B')

nPlots = 100    # 有多少条曲线
nSamples = 500  # 窗口显示范围大小

#curves = [p.plot(pen=(i,nPlots*1.3)) for i in range(nPlots)]
curves = []
for i in range(nPlots):
    c = pg.PlotCurveItem(pen = (i, nPlots*1.3))
    p.addItem(c)
    c.setPos(0,i*6)
    curves.append(c)

p.setYRange(0, nPlots*6)
p.setXRange(0, nSamples)
p.resize(600, 900)

rgn = pg.LinearRegionItem([nSamples/5., nSamples/3.])
p.addItem(rgn)

data = np.random.normal(size=(nPlots*23, nSamples))
ptr = 0
lastTime = time()
fps = None
count = 0

def update():
    global curve, data, ptr, p, lastTime, fps, nPlots, count
    count += 1
    
    #print "---------", count
    rec = serialport.read(1)
    if(len(rec)):
        tmp = int.from_bytes(rec, byteorder='big', signed=False)
        data[(1)%data.shape[0]] = tmp
        curves[1].setData(data[1])
    # for i in range(nPlots):
    #     curves[i].setData(data[(ptr+i)%data.shape[0]])
        
    #print "   setData done."
    ptr += nPlots
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    p.setTitle('%0.2f fps' % fps)
    
    #app.processEvents()  ## force complete redraw for every plot
timer = QtCore.QTimer()
timer.timeout.connect(update)
# timer.start(0)
timer.start(0)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
