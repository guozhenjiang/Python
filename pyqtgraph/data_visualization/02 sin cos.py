# https://www.toutiao.com/i6836297805770785292/?group_id=6836297805770785292

import pyqtgraph as pg
import numpy as np
import array

app = pg.mkQApp()           # 建立 App
win = pg.GraphicsWindow()   # 建立窗口
win.setWindowTitle("pyqtgraph 逐点画波图形")    # 窗口名称
win.resize(800, 500)        # 窗口大小

data = array.array('d')     # 可动态改变数组的大小， double 型数组
historyLength = 100         # 横坐标长度
p = win.addPlot()           # 把图 p 加入到窗口中
p.showGrid(x=True, y=True)  # 把 x 和 y 的网格打开
p.setRange(xRange=[0, historyLength], yRange=[-1.2, 1.2], padding=0)
p.setLabel(axis='left', text='y/V')         # 靠左 y 轴
p.setLabel(axis='bottom', text='x/Point')   # 靠下 x 轴
p.setTitle('y=sin(x)')                      # 表格名字
curve = p.plot()            # 绘制一个图形
idx = 0

# 定义函数
def plotData():
    global idx  # 内部作用域想改变外部域变量

    tmp = np.sin(np.pi / 50 * idx)  # sin 动态函数曲线
    #tmp = np.cos(np.pi / 50 * idx) # cos 动态函数曲线
    
    if len(data) < historyLength:
        data.append(tmp)
    else:
        data[:-1] = data[1:]    # 前移
        data[-1] = tmp
    
    curve.setData(data)
    idx += 1
    
# 启动定时器
timer = pg.QtCore.QTimer()
timer.timeout.connect(plotData) # 定时调用 plotData 函数
timer.start(50)

app.exec_()