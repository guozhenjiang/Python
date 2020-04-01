import pyqtgraph as pg
import numpy as np
import array
import binascii
import serial

comport = 'COM3'
baudrate='115200'
data_lenght = 32

bytes = 32
print('You selected %s, baudrate %d, %d byte.' % (comport, int(baudrate), bytes))

# serialport = serial.Serial(comport, int(baudrate), timeout=1, parity=serial.PARITY_EVEN, rtscts=1)
serialport = serial.Serial(comport, int(baudrate), timeout=1, parity=serial.PARITY_NONE, rtscts=1)

if serialport.isOpen():
    print("open success")
else:
    print("open failed")

app = pg.mkQApp()                           # 建立app
win = pg.GraphicsWindow()                   # 建立窗口

win.setWindowTitle(u'VHUB')
win.resize(800, 500)                        # 小窗口大小

udata = [0] * data_lenght                   # 可动态改变数组的大小,double型数组
data = array.array('d')                     # 可动态改变数组的大小,double型数组
historyLength = 100                         # 横坐标长度

p = win.addPlot()                           # 把图 p 加入到窗口中
p.showGrid(x=True, y=True)                  # 把 X 和 Y 的网格打开
p.setRange(xRange=[0,historyLength], yRange=[-1.2, 1.2], padding=0)
p.setLabel(axis='left', text='Value')       # 靠左
p.setLabel(axis='bottom', text='Label_bottom')
p.setTitle(u'Title')                        # 表格的名字
curve = p.plot()                            # 绘制一个图形

idx = 0
udx = 0

def plotData():
    # global idx                              # 内部作用域想改变外部域变量
    # global udx
    
    #print("udx",udx)
    #print()
    
    udata[udx] = serialport.read(1)
    udx = udx + 1
    
    #print("udata[0]",udata[0])
    #print(udata[31])
    
    #if ((udx == 20)):
    if ((udata[0] == b'\xff')and (udx == data_lenght)):
        udx = 0 
        #print('111111111')
        # tmp = np.sin(np.pi / 50 * idx)
        # print(type(tmp))
        # tmp =binascii.b2a_hex(tmp)
        tmp = int.from_bytes(udata[5],byteorder='big',signed=False)
        
        # tmp=str(tmp)
        # tmp =int(tmp)
        # tmp = binascii.b2a_hex(tmp).decode()
        # print(tmp)
        
        if len(data)<historyLength:
            data.append(tmp)
        else:
            data[:-1] = data[1:]            # 前移
            data[-1] = tmp
        curve.setData(data)
        idx += 1
    elif (udata[0] != b'\xff'):
        udx = 0
        print('tttt')
        
timer = pg.QtCore.QTimer()
timer.timeout.connect(plotData)             # 定时调用plotData函数
timer.start(1)                              # 多少ms调用一次

app.exec_()