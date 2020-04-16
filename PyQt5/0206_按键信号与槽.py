# https://www.learnpyqt.com/courses/start/signals-slots-events/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt

# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *

# import sys

# Subclass QMainWindow to customise your application's main window
# 创建 QMainWindow 的子类 MainWindow 来自定义自己应用程序的主窗口
class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # This sets the window title which will trigger all the above signals
        # sending the new title to the attached functions or lambdas as the
        # first parameter.
        self.setWindowTitle('My Awesom App')
        
        button = QPushButton('HELLO!')
        button.pressed.connect(self.pushed_my_button)
        
        # 设置 central widget 时 内容默认会占据整个窗口
        self.setCentralWidget(button)
    
    # SLOT: This has default parameters and can be called without a value
    # 带有默认参数的槽函数 调用时可以不传参
    def pushed_my_button(self):
        print('Pressed it!')

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) is fine.

# 每个应用程序需要（且仅需要）一个 QApplication 实例
# 通过在命令行中传入 sys.argv 向应用程序传入参数
# 如果你确定自己不用传入参数 用 QApplication([]) 也没问题
app = QApplication(sys.argv)

window = MainWindow()
window.show()   # IMPORTANT!!!!! Windows are hidden by default.
                # 这句很重要 窗口默认是隐藏状态

# Start the event loop.
# 启动应用程序的事件循环
app.exec_()

# Your application won't reach here until you exit and the event
# loop has stopped.

# 在退出事件循环之前 应用程序不会运行到这里