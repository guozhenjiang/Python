import sys                                                              # 获取系统参数
from PyQt5.QtWidgets import QMainWindow, QApplication                   # GUI 程序必须的
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolTip, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QFormLayout
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtCore import Qt

'''
    QLineEdit:
        基本功能：输入单行的文本
        高级功能：4 种回显功能：
            1. Normal 正常模式
            2. NoEcho 没有回显
            3. Password
            4. PasswordEchoOnEdit
'''

class QLineEditEchoMode(QWidget):
    def __init__(self):                                 # 初始化(构造函数)
        super().__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle("文本输入框的回显")

        formLayout = QFormLayout()

        normalLineEdit = QLineEdit()
        noEchoLineEdit = QLineEdit()
        passwordLineEdit = QLineEdit()
        passwordEchoOnEditLineEdit = QLineEdit()

        formLayout.addRow("Normal", normalLineEdit)
        formLayout.addRow("NoEcho", noEchoLineEdit)
        formLayout.addRow("Password", passwordLineEdit)
        formLayout.addRow("PasswordEchoOnEdit", passwordEchoOnEditLineEdit)

        # placeholdertext
        normalLineEdit.setPlaceholderText("Normal")
        noEchoLineEdit.setPlaceholderText("NoEcho")
        passwordLineEdit.setPlaceholderText("Password")
        passwordEchoOnEditLineEdit.setPlaceholderText("PasswordEchoOnEdit")

        normalLineEdit.setEchoMode(QLineEdit.Normal)
        noEchoLineEdit.setEchoMode(QLineEdit.NoEcho)
        passwordLineEdit.setEchoMode(QLineEdit.Password)
        passwordEchoOnEditLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.setLayout(formLayout)

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QLineEditEchoMode()
    main.show()

    sys.exit(app.exec_())
