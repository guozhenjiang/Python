import sys                                                              # 获取系统参数

from PyQt5.QtWidgets import QMainWindow, QApplication                   # GUI 程序必须的
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolTip, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QFormLayout

from PyQt5.QtGui import QFont, QPalette, QPixmap, QIntValidator, QDoubleValidator, QRegExpValidator

from PyQt5.QtCore import Qt, QRegExp

'''
    限制只能输入整数、浮点数 或满足一定条件的字符串
'''

class QLineEditValidator(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super(QLineEditValidator, self).__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle("校验器")

        formLayout = QFormLayout()      # 创建表单布局

        intLineEdit = QLineEdit()
        doubleLineEdit = QLineEdit()
        validatorLineEdit = QLineEdit()

        formLayout.addRow("整数类型", intLineEdit)
        formLayout.addRow("浮点类型", doubleLineEdit)
        formLayout.addRow("数字和字母", validatorLineEdit)

        # placeholdertext
        intLineEdit.setPlaceholderText("整数类型")
        doubleLineEdit.setPlaceholderText("浮点类型")
        validatorLineEdit.setPlaceholderText("数字和字母")

        intValidator = QIntValidator(self)          # 整数校验器 [1 ~ 99]
        intValidator.setRange(1, 99)

        doubleValidator = QDoubleValidator(self)    # 整数校验器 [-360 ~ 360] 精度：小数点后 2 位
        doubleValidator.setRange(-360, 360)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        doubleValidator.setDecimals(2)

        reg = QRegExp("[a-zA-Z0-9]+$")              # 数字和字母
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)

        intLineEdit.setValidator(intValidator)
        doubleLineEdit.setValidator(doubleValidator)
        validatorLineEdit.setValidator(validator)

        self.setLayout(formLayout)

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QLineEditValidator()
    main.show()

    sys.exit(app.exec_())
