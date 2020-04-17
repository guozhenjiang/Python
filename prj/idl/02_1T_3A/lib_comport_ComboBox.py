
# https://blog.csdn.net/MaggieTian77/article/details/79205192
# https://doc.qt.io/qtforpython/PySide2/QtWidgets/QComboBox.html?highlight=combobox#PySide2.QtWidgets.QComboBox

from PySide2.QtWidgets import QComboBox
from PySide2.QtCore import Signal

class PortComboBox(QComboBox):
    signal_PortComboBox_showPopup = Signal()
    
    def __init__(self, parent = None):
        super(PortComboBox, self).__init__(parent)
    
    def showPopup(self):            # 重写 showPopup
        # print('signal emit: signal_PortComboBox_showPopup')
        self.signal_PortComboBox_showPopup.emit()
        
        # print('showPopup now')
        QComboBox.showPopup(self)   # 弹出选项框
        