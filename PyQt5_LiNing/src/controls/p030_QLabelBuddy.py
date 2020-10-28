import sys                                                              # 获取系统参数
from PyQt5.QtWidgets import QMainWindow, QApplication                   # GUI 程序必须的
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QToolTip, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtCore import Qt

class QLabelBuddy(QDialog):
    def __init__(self):                                 # 初始化(构造函数)
        super().__init__()            # 父类初始化

        self.initUI()

    def initUI(self):
        self.setWindowTitle("QLabel 与伙伴控件")
        nameLabel = QLabel("&Name", self)
        nameLineEdit = QLineEdit(self)

        nameLabel.setBuddy(nameLineEdit)            # 设置伙伴控件

        passwordLabel = QLabel("&Password", self)
        passwordLineEdit = QLineEdit(self)

        passwordLabel.setBuddy(passwordLineEdit)    # 设置伙伴控件

        btnOK = QPushButton("&OK")
        btnCancel = QPushButton("&Cancel")

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(nameLineEdit, 0, 1, 1, 2)

        mainLayout.addWidget(passwordLabel, 1, 0)
        mainLayout.addWidget(passwordLineEdit,1, 1, 1, 2)
        mainLayout.addWidget(btnOK, 2, 1)
        mainLayout.addWidget(btnCancel, 2, 2)

# 防止别的脚本调用，只有当自己单独运行时才会执行！
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = QLabelBuddy()
    main.show()

    sys.exit(app.exec_())
