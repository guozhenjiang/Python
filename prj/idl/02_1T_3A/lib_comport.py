import serial
import serial.tools.list_ports

class ComPort():
    def __init__(self):
        super().__init__()
        
        self.PortValid = []
        self.PortUsing = ''         # 正在使用的端口
        self.PortUsed = ''          # 之前使用的端口
        self.Baud = 115200          # 波特率
        self.DataBit = 8            # 数据位宽度
        self.Parity = 'None'        # 校验
        self.StopBit = 1            # 停止位
        self.FlowControl = 'None'   # 流控
        self.Opend = False          # 是否已经打开
        
        # self.scan()
        
    # 端口扫描 返回可用端口名称列表
    def scan(self):
        self.PortValid = []
        port_list = list(serial.tools.list_ports.comports())        # 扫描可用端口
        port_list.sort()                                            # 对扫描结果排序
        
        for port_info in port_list:
            com = port_info[0]      # [name, description, hardware_id]
            # print(com)
            self.PortValid.append(com)
        
        print(self.PortValid)
        
        return self.PortValid
    
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