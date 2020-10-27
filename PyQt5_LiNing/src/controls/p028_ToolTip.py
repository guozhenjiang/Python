import sys                                                              # 获取系统参数
from PyQt5.QtWidgets import QMainWindow, QApplication                   # GUI 程序必须的
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QToolTip, QPushButton, QWidget

class ToolTipForm(QMainWindow):                        # 从 QMainWindow 继承
    def __init__(self):                                 # 初始化(构造函数)
        super().__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont("SansSerif", 12))
        self.setToolTip("今天是<b>星期五</b>")
        self.setGeometry(300, 300, 200, 300)
        self.setWindowTitle("设置控件提示消息")

        self.button1 = QPushButton("我的按钮")  # 添加 Button
        self.button1.setToolTip("这是一个按钮，Are you ok >")

        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #app.setWindowIcon(QIcon("./images/clock.ico"))
    main = ToolTipForm()
    main.show()

    sys.exit(app.exec_())
