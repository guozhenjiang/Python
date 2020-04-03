import sys
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import SIGNAL, QObject

def func():
    print("func has been called!")

app = QApplication(sys.argv)
button = QPushButton("Call func")
QObject.connect(button, SIGNAL ('clicked()'), func)
button.show()                                                                                             

sys.exit(app.exec_())

'''
    这个例子用 button 现有的 clicked 信号控制 print 特定内容
'''