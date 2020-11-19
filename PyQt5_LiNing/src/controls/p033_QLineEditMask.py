import sys                                                              # 获取系统参数

from PyQt5.QtWidgets import QMainWindow, QApplication                   # GUI 程序必须的
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolTip, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QFormLayout

from PyQt5.QtGui import QFont, QPalette, QPixmap, QIntValidator, QDoubleValidator, QRegExpValidator

from PyQt5.QtCore import Qt, QRegExp

'''
    A   ASCII 字母字符是必须输入的(A-Z、a-z)
    a   ASCII 字母字符是允许输入的，但不是必须的(A-Z、a-z)
    N   ASCII 字母字符是必须输入的(A-Z、a-z、0-9)
    n   ASCII 字母字符是允许输入的，但不是必须的(A-Z、a-z、0-9)
    X   任何字符都是必须输入的
    x   任何字符都是允许输入的，但不是必须的
    9   ASCII 数字是必须输入的(0-9)
    0   ASCII 数字字符是允许输入的，但不是必须的(0-9)
    D   ASCII 数字字符是必须输入的(1-9)
    d   ASCII 数字字符是允许输入的，但不是必须的(1-9)
    #   ASCII 数字字符或加减符号是允许输入的，但不是必须的
    H   十六进制格式字符是必须输入的(A-F、a-f、0-9)
    h   十六进制格式字符是允许输入的，但不是必须的(A-F、a-f、0-9)
    B   二进制格式字符是必须输入的(0、1)
    b   二进制格式字符是允许输入的，但不是必须的(0、1)
    >   所有的字母字符都大写
'''

class QLineEditMask(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super(QLineEditMask, self).__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle("用掩码限制 QLineEdit 控件的输入")

        formLayout = QFormLayout()      # 创建表单布局

        ipLineEdit = QLineEdit()
        macLineEdit = QLineEdit()
        dateLineEdit = QLineEdit()
        licenseLineEdit = QLineEdit()

        # 192.168.21.45
        ipLineEdit.setInputMask("000.000.000.000;_")    # 没有输入时 0 显示为 _
        macLineEdit.setInputMask("HH:HH:HH:HH:HH:HH:_")
        dateLineEdit.setInputMask("0000-00-00;_")
        licenseLineEdit.setInputMask(">AAAAA-AAAAA-AAAAA-AAAAA-AAAAA;#")

        formLayout.addRow("数字掩码", ipLineEdit)
        formLayout.addRow("Mac 掩码", macLineEdit)
        formLayout.addRow("日期掩码", dateLineEdit)
        formLayout.addRow("许可证掩码", licenseLineEdit)

        self.setLayout(formLayout)

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QLineEditMask()
    main.show()

    sys.exit(app.exec_())
