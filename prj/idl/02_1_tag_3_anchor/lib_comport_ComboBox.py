
# https://blog.csdn.net/MaggieTian77/article/details/79205192

import serial
import serial.tools.list_ports
import logging
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal

class ComPort_ComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def __init__(self, parent = None):
        super(ComPort_ComboBox, self).__init__(parent)

    # 重写showPopup函数
    def showPopup(self):
        print('ComPort_ComboBox.showPopup')
        # 先清空原有的选项
        self.clear()
        self.insertItem(0, '请选择端口')
        index = 1
        
        # 获取接入的所有串口信息，插入combobox的选项中
        portlist = self.get_port_list(self)
        if portlist is not None:
            for i in portlist:
                self.insertItem(index, i)
                index += 1
        QComboBox.showPopup(self)   # 弹出选项框

    @staticmethod
    # 获取接入的所有串口号
    def get_port_list(self):
        print('ComPort_ComboBox.get_port_list')
        try:
            port_list = list(serial.tools.list_ports.comports())
            for port in port_list:
                yield str(port)
        except Exception as e:
            logging.error("获取接入的所有串口设备出错！\n错误信息："+str(e))