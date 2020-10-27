import sys                                                              # 获取系统参数
from PyQt5.QtWidgets import QMainWindow, QApplication                   # GUI 程序必须的
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolTip, QPushButton, QWidget, QLabel
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtCore import Qt
'''
    setAlignment()      # 设置文本的对齐方式
    setIndent()         # 设置文本缩进
    text()              # 获取文本内容
    setBuddy()          # 设置伙伴关系
    setText()           # 设置文本内容
    selectedText()      # 返回所选择的字符
    setWordWrap()       # 设置是否允许换行

    QLabel 常用的信号(事件):
    1. 当鼠标滑过 QLabel 控件时触发 linkHovered
    2. 当鼠标单击 QLabel 控件时触发 linkActivated
'''

class QLabelDemo(QWidget):                        # 从 QMainWindow 继承
    def __init__(self):                                 # 初始化(构造函数)
        super().__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)

        label1.setText("<font color=yellow>这是一个文本标签.</font>")
        label1.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.blue)      # 设置背景色
        label1.setPalette(palette)
        label1.setAlignment(Qt.AlignCenter)

        label2.setText("<a href='#'>欢迎使用 Python GUI 程序</a>")

        label3.setAlignment(Qt.AlignCenter)
        label3.setToolTip("这是一个图片标签")
        label3.setPixmap(QPixmap("./images/python.jpg"))

        label4.setOpenExternalLinks(True)   # True 打开链接 False 响应槽函数
        label4.setText("<a href='https://item.jd.com/12417265.html'>感谢关注 《Python 从菜鸟到高手》")
        label4.setAlignment(Qt.AlignRight)
        label4.setToolTip("这是一个超级链接")

        vbox = QVBoxLayout()

        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)

        label2.linkHovered.connect(self.linkHovered)
        label4.linkActivated.connect(self.linkClicked)

        self.setLayout(vbox)
        self.setWindowTitle("QLabel 控件演示")

    def linkHovered(self):
        print("当鼠标滑过 label 2 标签时，触发事件")

    def linkClicked(self):
        print("当鼠标单击 label 4 标签时，触发事件")

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #app.setWindowIcon(QIcon("./images/clock.ico"))
    main = QLabelDemo()
    main.show()

    sys.exit(app.exec_())
