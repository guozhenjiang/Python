import sys                                              # 获取系统参数
from PyQt5.QtWidgets import QMainWindow, QApplication   # GUI 程序必须的
from PyQt5.QtGui import QIcon                           # 添加图标需要

'''
窗口的 setWindowIcon 方法用于设置窗口的图标，只在 Windows 中可用
QApplication 中的 setWindowIcon 方法用于设置主窗口的图标和应用程序图标，但调用了窗口的 setWindowIcon 方法
QApplication 中的 setWindowIcon 方法就只能用于设置应用程序图标了
'''

class IconForm(QMainWindow):                        # 从 QMainWindow 继承
    def __init__(self):                                 # 初始化(构造函数)
        super(IconForm, self).__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle("设置窗口图标")         # 设置主窗口的标题
        self.setWindowIcon(QIcon("./images/clock.ico"))

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #app.setWindowIcon(QIcon("./images/clock.ico"))
    main = IconForm()
    main.show()

    sys.exit(app.exec_())
