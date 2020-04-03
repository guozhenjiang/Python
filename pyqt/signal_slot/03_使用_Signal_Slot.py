import sys
from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QPushButton

# define a function that will be used as a slot
def sayHello():
 print('Hello world!')

app = QApplication(sys.argv)

button = QPushButton('Say hello!')

# connect the clicked signal to the sayHello slot
button.clicked.connect(sayHello)
button.show()

sys.exit(app.exec_())