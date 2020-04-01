# import pyqtgraph as pg
# import numpy as np
# import array
# import binascii
# import serial

# port = 'COM3'
# baudrate = 115200

# data_lenght = 32

# try:
#     print('looking for %s, %d' %(port, baudrate))
#     serialport = serial.Serial(port, int(baudrate), timeout=1, parity=serial.PARITY_NONE)
# except:
#     print("com open failed")
# else:
#     print("%s open success" %(serialport.name))

# print()

# # while(1):
# #     rec = serialport.read(50)
# #     if(len(rec)):
# #         print('%03d byte: %s' %(len(rec), rec))

# app = pg.mkQApp()                           # 建立app
# win = pg.GraphicsWindow()                   # 建立窗口

# win.setWindowTitle(u'VHUB')
# win.resize(800, 500)                        # 小窗口大小

# udata = [0] * data_lenght                   # 可动态改变数组的大小,double型数组
# data = array.array('d')                     # 可动态改变数组的大小,double型数组
# historyLength = 100                         # 横坐标长度

# p = win.addPlot()                           # 把图 p 加入到窗口中
# p.showGrid(x=True, y=True)                  # 把 X 和 Y 的网格打开
# p.setRange(xRange=[0,historyLength], yRange=[-1.2, 1.2], padding=0)
# p.setLabel(axis='left', text='Value')       # 靠左
# p.setLabel(axis='bottom', text='Label_bottom')
# p.setTitle(u'Title')                        # 表格的名字
# curve = p.plot()                            # 绘制一个图形

# def plotData():
#     rec = serialport.read(1)
#     if(len(rec)):
#         curve.setData(0.2)
#         # curve.setData(int.from_bytes(rec))

# # idx = 0
# # udx = 0

# # def plotData():
# #     global idx                              # 内部作用域想改变外部域变量
# #     global udx
    
# #     udata[udx] = serialport.read(1)
# #     udx = udx + 1
    
# #     if ((udata[0] == b'\xff')and (udx == data_lenght)):
# #         udx = 0 
        
# #         tmp = int.from_bytes(udata[5],byteorder='big',signed=False)
        
# #         if len(data)<historyLength:
# #             data.append(tmp)
# #         else:
# #             data[:-1] = data[1:]            # 前移
# #             data[-1] = tmp
# #         curve.setData(data)
# #         idx += 1
        
# #     elif (udata[0] != b'\xff'):
# #         udx = 0
# #         print('tttt')
        
# timer = pg.QtCore.QTimer()
# timer.timeout.connect(plotData)             # 定时调用plotData函数
# timer.start(1)                              # 多少ms调用一次

# app.exec_()