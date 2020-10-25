import sys

from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)    # 创建 QApplication 类的实例

    w = QWidget()                   # 创建一个窗口
    w.resize(400, 200)              # 设置窗口尺寸
    w.move(300, 300)                # 移动窗口
    w.setWindowTitle("第一个基于 PyQt5 的桌面应用")   # 设置窗口标题
    w.show()                        # 显示窗口

    sys.exit(app.exec_())           # 进入程序的主循环、并通过 exit 函数确保主循环安全结束
