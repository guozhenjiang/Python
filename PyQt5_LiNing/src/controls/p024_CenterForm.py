import sys                                              # 获取系统参数
from PyQt5.QtWidgets import QMainWindow, QApplication   # GUI 程序必须的
from PyQt5.QtGui import QIcon                           # 添加图标需要
from PyQt5.QtWidgets import QDesktopWidget

class CenterForm(QMainWindow):                          # 从 QMainWindow 继承
    def __init__(self):                                 # 初始化(构造函数)
        super(CenterForm, self).__init__()            # 父类初始化

        self.setWindowTitle("让窗口居中")                # 设置主窗口的标题
        self.resize(400, 300)                           # 设置窗口尺寸
        #self.center()

        self.status = self.statusBar()
        self.status.showMessage("只存在 5 秒 的消息", 5000)

    def center(self):
        screen = QDesktopWidget().screenGeometry()      # 获取屏幕坐标
        size = self.geometry()                          # 获取窗口坐标

        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2

        self.move(newLeft, newTop)

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon("./images/clock.ico"))
    main = CenterForm()
    main.center()
    main.show()

    sys.exit(app.exec_())
