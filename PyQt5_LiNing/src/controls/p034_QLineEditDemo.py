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

class QLineEditDemo(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super(QLineEditDemo, self).__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle("QLineEdit 综合案例")

        edit1 = QLineEdit()

        edit1.setValidator(QIntValidator())     # 使用 int 校验器
        edit1.setMaxLength(4)
        edit1.setAlignment(Qt.AlignRight)
        edit1.setFont(QFont("Arial", 20))

        edit2 = QLineEdit()
        edit2.setValidator(QDoubleValidator(0.99, 99.99, 2))

        edit3 = QLineEdit()
        edit3.setInputMask("99_9999_999999;#")

        edit4 = QLineEdit()
        edit4.textChanged.connect(self.textChanged)

        edit5 = QLineEdit()
        edit5.setEchoMode(QLineEdit.Password)
        edit5.editingFinished.connect(self.enterPress)

        edit6 = QLineEdit("Hello PyQt5")
        edit6.setReadOnly(True)

        formLayout = QFormLayout()      # 创建表单布局

        formLayout.addRow("整数校验", edit1)
        formLayout.addRow("浮点数校验", edit2)
        formLayout.addRow("Input Mask", edit3)
        formLayout.addRow("文本变化", edit4)
        formLayout.addRow("密码", edit5)
        formLayout.addRow("只读", edit6)

        self.setLayout(formLayout)

    def textChanged(self, text):
        print("输入的内容" + text)

    def enterPress(self):
        print("已输入值")

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QLineEditDemo()
    main.show()

    sys.exit(app.exec_())
