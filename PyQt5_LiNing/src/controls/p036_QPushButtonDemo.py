import sys                                                              # 获取系统参数

from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit  # GUI 程序必须的
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolTip, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QFormLayout

from PyQt5.QtGui import QFont, QPalette, QPixmap, QIntValidator, QDoubleValidator, QRegExpValidator, QIcon

from PyQt5.QtCore import Qt, QRegExp

'''
    QAbstractButton

    QPushButton
    AToolButton
    QRadioButton
    QCheckBox
'''

class QPushButtonDemo(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super(QPushButtonDemo, self).__init__()         # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QPushButton Demo')

        layout = QVBoxLayout()

        self.button1 = QPushButton('第一个按钮')
        self.button1.setText('First Button')
        self.button1.setCheckable(True)
        self.button1.toggle()
        self.button1.clicked.connect(self.buttonState)
        self.button1.clicked.connect(lambda:self.whichButton(self.button1))

        layout.addWidget(self.button1)

        # 在文本前面显示图像

        self.button2 = QPushButton('图像按钮')
        self.button2.setIcon(QIcon(QPixmap('./images/python.png')))
        self.button2.clicked.connect(lambda:self.whichButton(self.button2))
        layout.addWidget(self.button2)

        self.setLayout(layout)

        # 使按钮不可用

        self.button3 = QPushButton('不可用按钮')
        self.button3.setEnabled(False)
        layout.addWidget(self.button3)

        # 设置默认按钮

        self.button4 = QPushButton('&MyButton')
        self.button4.setDefault(True)
        self.button4.clicked.connect(lambda:self.whichButton(self.button4))
        layout.addWidget(self.button4)

    def buttonState(self):
        if self.button1.isChecked():
            print('按钮 1 已经被选中')
        else:
            print('按钮 1 未被选中')

    def whichButton(self, btn):
        print('被单击的按钮是<' + btn.text() + '>')

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QPushButtonDemo()
    main.show()

    sys.exit(app.exec_())
