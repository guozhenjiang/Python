import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

'''
    QAbstractButton

    QPushButton
    AToolButton
    QRadioButton
    QCheckBox
'''

class QRadioButtonDemo(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super(QRadioButtonDemo, self).__init__()         # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle('QRadioButton')

        layout = QHBoxLayout()

        self.button1 = QRadioButton('单选按钮 1')
        self.button1.setChecked(True)
        self.button1.toggled.connect(self.buttonState)
        layout.addWidget(self.button1)

        self.button2 = QRadioButton('单选按钮 2')
        self.button2.toggled.connect(self.buttonState)
        layout.addWidget(self.button2)

        self.setLayout(layout)

    def buttonState(self):
        radioButton = self.sender()
        if radioButton.isChecked() == True:
            print('<' + radioButton.text() + '> 被选中')
        else:
            print('<' + radioButton.text() + '> 被取消选中状态')

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QRadioButtonDemo()
    main.show()

    sys.exit(app.exec_())
