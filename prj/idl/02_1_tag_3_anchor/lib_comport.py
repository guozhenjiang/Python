import serial
import serial.tools.list_ports

class ComPort():
    def __init__(self):
        super().__init__()
        # self.scan()
    
    # 端口扫描 返回可用端口名称列表
    def scan(self):
        print('ComPort.scan')
        com_list = list(serial.tools.list_ports.comports())
        com_name = []
        com_num = len(com_list)
        print('\r\n%d 个端口' %(com_num))
        for com in com_list:
            print(com)
            com_name.append(com)
        
        return com_name
    
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

comport = ComPort()

'''
Note:
    
'''