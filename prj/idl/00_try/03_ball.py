# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

## 创建一个GL视图小部件来显示数据
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('Cute Ball')
w.setCameraPosition(distance=50)

## 向视图添加网格
g = gl.GLGridItem()
g.scale(2,2,1)
g.setDepthValue(10)     # 尝试了不同值没发现有什么作用
w.addItem(g)


u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 10 * np.outer(np.cos(u), np.sin(v))
y = 10 * np.outer(np.sin(u), np.sin(v))
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

# print(x)
# print(x[0])

for i in range(100):
    for j in range(100):
        val = x[i]**2 + y[j]**2
        # print(val)
        z[i][j] = val * 0.1
        # z[i][j] = 0.1 * i**2 + 0.1 * j**2


p5 = gl.GLSurfacePlotItem(x, y, z, shader='heightColor', computeNormals=False, smooth=False)
p5.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
p5.translate(0, 0, 0)     # 子图原点位置移动
w.addItem(p5)


# index = 0
# def update():
#     global p4, z, index, p5
#     index -= 1
#     p4.setData(z=z[index%z.shape[0]])
    
#     # p5.setData(z=z[index%z.shape[0]])
    
# timer = QtCore.QTimer()
# timer.timeout.connect(update)
# timer.start(30)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
