
# https://blog.csdn.net/MaggieTian77/article/details/79205192


# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QComboBox.html?highlight=combobox#PySide2.QtWidgets.QComboBox
from PySide2.QtWidgets import QComboBox
from PySide2.QtCore import Signal, Slot

class PortComboBox(QComboBox):
    signal_PortComboBox_showPopup = Signal()
    
    # 初始化
    def __init__(self, parent = None):
        super(PortComboBox, self).__init__(parent)
        # print('ComPort_ComboBox_init')

    # 重写 showPopup 函数
    def showPopup(self):
        # print('signal_PortComboBox_showPopup')
        self.signal_PortComboBox_showPopup.emit()
        
        # print('signal continue: showPopup')
        QComboBox.showPopup(self)   # 弹出选项框