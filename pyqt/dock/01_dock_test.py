# https://zhuanlan.zhihu.com/p/38390507

# 这个例子只提供了一部分代码，目前没有跑起来

import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

class Dock(QMainWindow):
    def __init__(self):
        super().__init__()
        hlayout = QHBoxLayout()
        self.dock = QDockWidget("我是一个按钮", self)
        self.bt = QPushButton("点我")
        self.dock.setWidget(self.bt)
        self.tt = QTextEdit()
        self.setCentralWidget(self.tt)
        self.addDockWidget(QMainWindow.RightDockWidgetArea, self.dock)
        self.setLayout(hlayout)
        self.setWindowTitle("学点编程吧：代码如何使用QDockWidget")
        self.bt.clicked.connect(self.game)

    def game(self):
        self.tt.append("你点我啦！")

app = QtWidgets.QApplication(sys.argv)
win = QtWidgets.QMainWindow()
dock = Dock(win)
dock.show()
sys.exit(app.exec_())