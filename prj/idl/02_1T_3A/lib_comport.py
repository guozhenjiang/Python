import serial
import serial.tools.list_ports

# from PyQt5.QtCore import pyqtSignal     # PyQt5 中的用法
from PySide2.QtCore import QObject, Signal, Slot # PySide2 中的用法

class ComPort(QObject):
    signal_PortOpenClose = Signal(bool)
    
    def __init__(self):
        super().__init__()
        
        self.PortValid = []
        self.PortUsing = ''                 # 正在使用的端口    COMx
        self.PortUsed = ''                  # 之前使用的端口    COMx
        self.Baud = 115200                  # 波特率            [..., 4800, 9600, 115200, ...]
        self.DataBit = 8                    # 数据位宽度        [8, 7, 6, 5]
        self.Parity = serial.PARITY_NONE    # 校验    [PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE]
        self.StopBit = serial.STOPBITS_ONE  # 停止位   [STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO]
        self.XonXoff = False                # 是否启用软件流控
        self.RtsCts = False                 # 是否启用 Request To Send and Clean To Send
        self.DsrDtr = False                 # 是否启用 Data Set Ready and Data Terminal Ready
        self.Opend = False                  # 是否已经打开
        
        # self.scan()
        
    # 端口扫描 返回可用端口名称列表
    def just_scan(self):
        # 更新 self.PortValid
        self.PortValid = []
        port_list = list(serial.tools.list_ports.comports())        # 扫描可用端口
        port_list.sort()                                            # 对扫描结果排序
        
        for port_info in port_list:
            com = port_info[0]      # [name, description, hardware_id]
            # print(com)
            self.PortValid.append(com)
        
        print(self.PortValid)
        
    # 端口扫描 返回可用端口名称列表
    def scan(self, ComboBox):
        # 更新 self.PortValid
        self.PortValid = []
        port_list = list(serial.tools.list_ports.comports())        # 扫描可用端口
        port_list.sort()                                            # 对扫描结果排序
        
        for port_info in port_list:
            com = port_info[0]      # [name, description, hardware_id]
            # print(com)
            self.PortValid.append(com)
        
        print(self.PortValid)
        
        # 更新 ComboBox
        self.PortUsed = ComboBox.currentText()
        print('更新之前端口选择下拉菜单的内容是：%s' %(self.PortUsed))
        
        ComboBox.clear()            # 清空当前端口选择下拉菜单内容       
        if(len(self.PortValid) > 0):
            ComboBox.addItems(self.PortValid)
        else:
            ComboBox.addItem('无可用端口')
        
        # used_index = ComboBox.findText(self.PortUsed)
        
        # if(used_index >= 0):
        #     print('上次使用的端口仍然存在')
        # else:
        #     print('上次使用的端口不见了')
    
    def set_com(self, str_com):
        self.PortUsing = str_com
        print('PortUsing = %s' %(self.PortUsing))
    
    def set_baud(self, str_baud):
        self.Baud = int(str_baud, 10)
        print('Baud = %d' %(self.Baud))
    
    def set_data_bit(self, str_data_bit):
        self.DataBit = int(str_data_bit, 10)
        print('DataBit = %d' %(self.DataBit))
    
    def set_parity(self, str_parity):
        dictPaity = {   'None'  : serial.PARITY_NONE,
                        'Odd'   : serial.PARITY_ODD,
                        'Even'  : serial.PARITY_EVEN,
                        'Mark'  : serial.PARITY_MARK,
                        'Space' : serial.PARITY_SPACE}
        
        self.Parity = dictPaity[str_parity]
        print('Parity = ', self.Parity)
    
    def set_stop_bit(self, str_stop_bit):
        dictStopBit = { '1'     : serial.STOPBITS_ONE,
                        '1.5'   : serial.STOPBITS_ONE_POINT_FIVE,
                        '2'     : serial.STOPBITS_TWO}
        
        self.StopBit = dictStopBit[str_stop_bit]
        print('StopBit = ', self.StopBit)
    
    def set_XonXoff(self, en):
        self.XonXoff = en
        print('XonXoff = ', self.XonXoff)
    
    def set_RtsCts(self, en):
        self.RtsCts = en
        print('RtsCts = ', self.RtsCts)
    
    def set_DsrDtr(self, en):
        self.DsrDtr = en
        print('DsrDtr = ', self.DsrDtr)
    
    def open_close(self):
        if(self.Opend):
            self.port.close()
            self.Opend = False
            print('端口 %s 已关闭' %(self.PortUsing))
        else:
            try:
                print('尝试打开端口 %s @ %d bps' %(self.PortUsing, self.Baud))
                
                self.port = serial.Serial(  port                = self.PortUsing,   # 端口号
                                            baudrate            = self.Baud,        # 波特率
                                            bytesize            = self.DataBit,     # 位宽
                                            parity              = self.Parity,      # 校验
                                            stopbits            = self.StopBit,     # 停止位
                                            timeout             = None,             # 超时
                                            xonxoff             = self.XonXoff,     # 软件流控
                                            rtscts              = self.RtsCts,      # 硬件流控 RTS/CTS
                                            write_timeout       = None,             # 发送超时
                                            dsrdtr              = self.DsrDtr,      # 硬件流控 DSR/DTR
                                            inter_byte_timeout  = None,             # 字节间超时
                                            exclusive           = None)             # 互斥访问模式
                
                self.Opend = True
                print('端口 %s 已打开' %(self.PortUsing))
            except:                         # 操作失败
                print('端口打开失败')
            else:                           # 操作成功
                
                pass
        
        print('\r\n发出 signal')
        self.signal_PortOpenClose.emit(self.Opend)
            
    
    # 端口学习(学习记录)
    def study(self):
        print(type(serial.tools.list_ports.comports()), end=':')
        print(serial.tools.list_ports.comports())

        print(type(list(serial.tools.list_ports.comports())), end=':')
        print(list(serial.tools.list_ports.comports()))

        print(type(len(list(serial.tools.list_ports.comports()))), end=':')
        print(len(list(serial.tools.list_ports.comports())))
        
        for com in list(serial.tools.list_ports.comports()):
            # print(type(com), end='    ')
            print(com)

# comport = ComPort()

'''
Note:
    
'''