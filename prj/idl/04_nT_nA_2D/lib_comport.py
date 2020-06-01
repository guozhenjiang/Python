import serial
import serial.tools.list_ports
from PySide2.QtCore import QObject
import time

class Port(QObject):
    def __init__(self):
        super().__init__()
        
        self.valid = []                     # 可用端口列表
        self.name = ''                      # 正在使用的端口    COMx
        self.name_last = ''                 # 之前使用的端口    COMx
        self.baud = 115200                  # 波特率            [..., 4800, 9600, 115200, ...]
        self.byte = 8                       # 数据位宽度        [8, 7, 6, 5]
        self.parity = serial.PARITY_NONE    # 校验      [PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE]
        self.stop = serial.STOPBITS_ONE     # 停止位    [STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO]
        self.xonxoff = False                # 是否启用软件流控
        self.rtscts = False                 # 是否启用 Request To Send and Clean To Send
        self.dsrdtr = False                 # 是否启用 Data Set Ready and Data Terminal Ready
        self.isopen = False                 # 是否已经打开
        
        self.read_id = 0                    # 端口打开后第几次读取
        self.read_stamp = time.perf_counter()   # time.perf_counter() 返回浮点数 表示程序持续运行的秒数
        self.read_stamp_last = self.read_stamp
        self.rx_cache = bytes()
    
    def scan(self):
        self.valid.clear()
        
        # serial.tools.list_ports: [port, desc, hwid] https://pyserial.readthedocs.io/en/latest/tools.html
        port_list = list(serial.tools.list_ports.comports())        # 扫描可用端口
        port_list.sort()                                            # 对扫描结果排序
        
        for i in port_list:
            print()
            com_str = ''
            for j in i:
                # print(j)
                com_str += j + ' '
            
            print(com_str)
            self.valid.append(com_str)
    
    def set_parity(self, str_parity):
        dictPaity = {   'None'  : serial.PARITY_NONE,
                        'Odd'   : serial.PARITY_ODD,
                        'Even'  : serial.PARITY_EVEN,
                        'Mark'  : serial.PARITY_MARK,
                        'Space' : serial.PARITY_SPACE}
        
        self.parity = dictPaity[str_parity]
    
    def set_stop(self, str_stop_bit):
        dictStopBit = { '1'     : serial.STOPBITS_ONE,
                        '1.5'   : serial.STOPBITS_ONE_POINT_FIVE,
                        '2'     : serial.STOPBITS_TWO}
        
        self.stop = dictStopBit[str_stop_bit]
    
    def open_close(self):
        # 端口已打开 本次操作时要关闭
        if(self.isopen):
            self.port.close()
            self.isopen = False
            # print('%s 已关闭' %(self.name))
        
        # 端口已关闭 本次操作时要打开
        else:
            # 尝试打开端口
            try:
                self.port = serial.Serial(  port                = self.name,        # 端口号
                                            baudrate            = self.baud,        # 波特率
                                            bytesize            = self.byte,        # 位宽
                                            parity              = self.parity,      # 校验
                                            stopbits            = self.stop,        # 停止位
                                            timeout             = None,             # 超时
                                            xonxoff             = self.xonxoff,     # 软件流控
                                            rtscts              = self.rtscts,      # 硬件流控 RTS/CTS
                                            write_timeout       = None,             # 发送超时
                                            dsrdtr              = self.dsrdtr,      # 硬件流控 DSR/DTR
                                            inter_byte_timeout  = None,             # 字节间超时
                                            exclusive           = None)             # 互斥访问模式
            # 端口打开失败
            except:
                pass
            
            # 端口打开成功
            else:
                self.port.flushInput()
                self.port.flushOutput()
                self.read_id = 0
                self.rx_cache = bytes()
                
                self.isopen = True
                pass

'''
    pyerial note:
    网址
        https://pyserial.readthedocs.io/en/latest/index.html
    安装
        python -m pip install pyserial
        conda install pyserial
        conda install -c conda-forge pyserial
        
        http://pypi.python.org/pypi/pyserial
        https://github.com/pyserial/pyserial/releases
            python setup.py install
    
    波特率
        standard: 50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200
        above: 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000
'''