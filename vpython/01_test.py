# # from visual import *
# from vpython import *

# sphere()

# from vpython import sphere,vector
# L = 5
# R = 0.3
# for i in range(-L,L+1):
#     for j in range(-L,L+1):
#         for k in range(-L,L+1):
#             sphere(pos=vector(i,j,k),radius=R)



from pyqtgraph.Qt import QtGui, QtCore
# import numpy as np
import pyqtgraph as pg
# from pyqtgraph.ptime import time
# from scipy import signal
# import pyqtgraph.widgets.RemoteGraphicsView

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title = '室内定位点到点数据滤波')
win.title = "hello"
win.resize(1000, 600)

pg.setConfigOptions(antialias = True)

from vpython import *
ball = sphere(pos=vector(1,2,1), radius=0.5)