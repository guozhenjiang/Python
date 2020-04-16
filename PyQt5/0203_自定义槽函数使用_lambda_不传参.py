# https://www.learnpyqt.com/courses/start/signals-slots-events/

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
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
        
        # SIGNAL: The connected function will be called whenever the window
        # title is changed. The new title will be passed to the function.
        self.windowTitleChanged.connect(lambda x: self.my_custom_fn())      # 窗口标题发生变化时，槽函数被调用，新的标题作为参数
        
        # This sets the window title which will trigger all the above signals
        # sending the new title to the attached functions or lambdas as the
        # first parameter.
        self.setWindowTitle('My Awesom App')
        
        label = QLabel('THIS IS AWESOM!!!')

        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        
        # Qt 命名空间有很多参数可以自定义
        # 关于 widgets 的可以参考: http://doc.qt.io/qt-5/qt.html
        label.setAlignment(Qt.AlignCenter)
        
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        
        # 设置 central widget 时 内容默认会占据整个窗口
        self.setCentralWidget(label)

    # SLOT: This accepts a string, e.g. the window title, and prints it
    # 槽函数接收一个字符串类型参数，例如窗口标题，然后打印出来
    def onWindowTitleChane(self, s):
        print(s)
    
    # SLOT: This has default parameters and can be called without a value
    # 带有默认参数的槽函数 调用时可以不传参
    def my_custom_fn(self, a='HELLO', b=5):
        print(a, b)

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