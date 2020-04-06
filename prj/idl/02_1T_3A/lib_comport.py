import serial
import serial.tools.list_ports
from PySide2.QtCore import QObject

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
    
    def scan(self):
        # 更新 self.valid
        self.valid.clear()
        port_list = list(serial.tools.list_ports.comports())        # 扫描可用端口
        port_list.sort()                                            # 对扫描结果排序
        
        for port_info in port_list:
            com = port_info[0]      # [name, description, hardware_id]
            self.valid.append(com)
    
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
        if(self.isopen):
            self.port.close()
            self.isopen = False
            # print('%s 已关闭' %(self.name))
        else:
            try:
                # print('尝试打开 %s ' %(self.name), self.baud, self.byte, self.parity, self.stop, self.xonxoff, self.rtscts, self.dsrdtr, end=' ')
                
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
                
                self.isopen = True
                # print('成功')
            except:             # 操作失败
                pass
                # print('失败')
            else:               # 操作成功
                
                pass

'''
    Note:
'''