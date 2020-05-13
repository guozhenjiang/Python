from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
g = gl.GLGridItem()
w.addItem(g)

pos = np.random.randint(-10, 10, size=(100,10,3))   # 生成三维随机数
pos[:,:,2] = np.abs(pos[:,:,2])                     # 将 Z 是 负值的点移动到 XY 平面镜像位置

ScatterPlotItems = {}
for point in np.arange(10):
    ScatterPlotItems[point] = gl.GLScatterPlotItem(pos=pos[:,point,:])  # 100 个 三维点？
    w.addItem(ScatterPlotItems[point])

color = np.zeros((pos.shape[0],10,4), dtype=np.float32)
color[:,:,0] = 1
color[:,:,1] = 0
color[:,:,2] = 0.5
color[0:5,:,3] = np.tile(np.arange(1,6)/5., (10,1)).T

def update():
    # update volume colors
    global color
    for point in np.arange(10):
        
        '''
            http://www.pyqtgraph.org/documentation/3dgraphics/glscatterplotitem.html
                
            Docs » API Reference » PyQtGraph’s 3D Graphics System » GLScatterPlotItemView page source
            GLScatterPlotItem

            class pyqtgraph.opengl.GLScatterPlotItem(**kwds)[source]
                Draws points at a list of 3D positions.

                __init__(**kwds)[source]
                setData(**kwds)[source]
                    Update the data displayed by this item. All arguments are optional;
                    for example it is allowed to update spot positions while leaving colors unchanged, etc.

                Arguments:	 
                    pos	(N,3) array of floats specifying point locations.
                    color	(N,4) array of floats (0.0-1.0) specifying spot colors OR a tuple of floats specifying a single color for all spots.
                    size	(N,) array of floats specifying spot sizes or a single value to apply to all spots.
                    pxMode	If True, spot sizes are expressed in pixels. Otherwise, they are expressed in item coordinates.
        '''
        ScatterPlotItems[point].setData(color=color[:,point,:], size=((point+1)*5), pxMode=False)
        # print(type(ScatterPlotItems[point]), ScatterPlotItems[point]) # <class 'pyqtgraph.opengl.items.GLScatterPlotItem.GLScatterPlotItem'> <pyqtgraph.opengl.items.GLScatterPlotItem.GLScatterPlotItem object at 0x000002BB97905D38>
    
    color = np.roll(color, 1, axis=0)   # 循环滚动
    pass

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(1000)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()