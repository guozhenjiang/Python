#!/usr/bin/python
# -*-coding: utf-8 -*-

import serial
import pyqtgraph as pg
import threading
import binascii
from datetime import datetime
import struct
import csv
import array
import numpy as np
is_exit = False
data_bytes = 0
data_lenght = 32



class SerialPort:
    udata =  [0]*data_lenght #可动态改变数组的大小,double型数组
    data  =  array.array('d') #可动态改变数组的大小,double型数组 
    def __init__(self, HistoryLength , port , buand):
        self.historyLength = HistoryLength
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def port_open(self):
        if not self.port.isOpen():
            self.port.open()

    def port_close(self):
        self.port.close()

    def send_data(self):
        self.port.write('')

    def read_data(self):
        global is_exit
        global data_bytes
        global data_lenght
        while not is_exit:
            count = self.port.inWaiting()
            
            if ((count != 0)and(count%data_lenght==0 )):
                print('count is ', count)
                self.rx_max_size = count//data_lenght
                #print('self.rx_max_size',self.rx_max_size)
                rec_str = self.port.read(count)
                #print()
                #for i in range(self.rx_max_size):
                whi_index = 0
                while self.rx_max_size > 0:
                    self.rx_max_size = self.rx_max_size -1 
                    print('self.rx_max_size is ' ,self.rx_max_size)
                    #a = np.fromstring(rec_str , dtype = np.uint8)
                    #b = a.tolist()
                    print('whi_index',whi_index)
                    #print(b)
                    tmp = rec_str[5+whi_index*data_lenght]
                    print(tmp)
                    whi_index = whi_index + 1 
                    #print("self.rx_max_size",rec_str[5+self.rx_max_size*data_lenght])
                    #print("rec_str",rec_str[0])
                    data_bytes = data_bytes + rec_str
                    
                    if len(self.data)< self.historyLength:
                        self.data.append(tmp)
                    else:
                        self.data[:-1] = self.data[1:]#前移
                        self.data[-1] = tmp
                    self.curve.setData(self.data)
                    
                    #print('当前数据接收总字节数：'+str(len(data_bytes))+' 本次接收字节数：'+str(len(rec_str)))
                    #print(str(datetime.now()),':',binascii.b2a_hex(rec_str))
            elif (count != 0)and(count%data_lenght!=0 ):
                self.port.flushInput()    # 清除输入缓冲区数据
                print('array array array array array error!',count)
                count = 0
                
                
    def setWindow(self):
        self.app = pg.mkQApp()#建立app
        self.win = pg.GraphicsWindow()#建立窗口
        self.win.setWindowTitle(u'pyqtgraph逐点画波形图')
        self.win.resize(800, 500)#小窗口大小

    def app_exec(self):
        self.app.exec_()
    
    def draw(self):
        p = self.win.addPlot()#把图p加入到窗口中
        p.showGrid(x=True, y=True)#把X和Y的表格打开
        p.setRange(xRange=[0,self.historyLength], yRange=[-1.2, 1.2], padding=0)
        p.setLabel(axis='left', text='y / V')#靠左
        p.setLabel(axis='bottom', text='x / point')
        p.setTitle('y = sin(x)')  #表格的名字
        self.curve = p.plot()#绘制一个图形


serialPort = 'COM11'  # 串口
baudRate = 230400  # 波特率
is_exit=False
data_bytes=bytearray()

if __name__ == '__main__':


    #文件写入操作
    filename=input('请输入文件名：比如test.csv:')
    #打开串口
    mSerial = SerialPort(HistoryLength = 100,port = serialPort, buand = baudRate)
    dt=datetime.now()
    nowtime_str=dt.strftime('%y-%m-%d %I-%M-%S')  #时间
    filename=nowtime_str+'_'+filename
    out=open(filename,'a+')
    csv_writer=csv.writer(out)
    
    mSerial.setWindow()
    mSerial.draw()
    
    #开始数据读取线程
    t1 = threading.Thread(target=mSerial.read_data)
    t1.setDaemon(True)
    t1.start()

    #
    while not is_exit:
        #主线程:对读取的串口数据进行处理
        mSerial.app_exec()
        data_len=len(data_bytes)
        i=0
        while(i<data_len-1):
            if(data_bytes[i]==0xFF and data_bytes[i+1]==0x5A):
                frame_code=data_bytes[i+2]
                frame_len=struct.unpack('<H',data_bytes[i+4:i+6])[0]
                frame_time=struct.unpack('<I',data_bytes[i+6:i+10])[0]
                print('帧类型：',frame_code,'帧长度：',frame_len,'时间戳：',frame_time)
                #print(frame_code,  frame_len,frame_time)
                if frame_code==0x03:   #判断帧类型
                    #struct 解析数据帧
                    accelerated_x,accelerated_y,accelerated_z,angular_x,angular_y,angular_z,tem,speed_x,speed_y,speed_z,\
                    angular_v_x,angular_v_y,angular_v_z=struct.unpack('<fffffffffffff',data_bytes[i+12:i+12+frame_len-6])
                    dt=datetime.now()
                    nowtime_str=dt.strftime('%y-%m-%d %I:%M:%S')  #时间
                    loc_str=[nowtime_str,frame_time,accelerated_x,accelerated_y,accelerated_z,angular_x,angular_y,angular_z,tem,speed_x,speed_y,speed_z,\
                    angular_v_x,angular_v_y,angular_v_z]

                    #写入csv文件
                    try:
                       csv_writer.writerow(loc_str)
                    except Exception as e:
                       raise e       
                i=i+6+frame_len+3
            else:
                i=i+1
        data_bytes[0:i]=b''
        
        
        
        
        
        
        
        
        
        
        
        