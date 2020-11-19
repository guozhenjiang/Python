import sys                                                              # 获取系统参数

from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit  # GUI 程序必须的
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

class QTextEditDemo(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super(QTextEditDemo, self).__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTextEdit 控件")

        self.resize(300, 320)

        self.textEdit = QTextEdit()
        self.buttonText = QPushButton("显示文本")
        self.buttonHTML = QPushButton("显示 HTML")
        self.buttonToText = QPushButton("获取文本")
        self.buttonToHTML = QPushButton("获取 HTML")

        layout = QVBoxLayout()

        layout.addWidget(self.textEdit)
        layout.addWidget(self.buttonText)
        layout.addWidget(self.buttonHTML)
        layout.addWidget(self.buttonToText)
        layout.addWidget(self.buttonToHTML)

        self.buttonText.clicked.connect(self.onClick_ButtonText)
        self.buttonHTML.clicked.connect(self.onClick_ButtonHTML)

        self.buttonToText.clicked.connect(self.onClick_ButtonToText)
        self.buttonToHTML.clicked.connect(self.onClick_ButtonToHTML)

        self.setLayout(layout)

    def onClick_ButtonText(self):
        self.textEdit.setPlainText("Hello World, 世界你好吗？")

    def onClick_ButtonHTML(self):
        self.textEdit.setHtml('<font color="blue" size=5>Hello World</font>')

    def onClick_ButtonToText(self):
        print(self.textEdit.toPlainText())

    def onClick_ButtonToHTML(self):
        print(self.textEdit.toHtml())

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QTextEditDemo()
    main.show()

    sys.exit(app.exec_())
