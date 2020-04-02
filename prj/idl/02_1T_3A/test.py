import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton

def window():
   app = QApplication([])
   win = QDialog()
   
   b1 = QPushButton(win)
   b1.setText("Button1")
   b1.move(50,20)
   b1.clicked.connect(b1_clicked)

   win.setGeometry(100,100,200,100)
   win.setWindowTitle("PyQt")
   win.show()
   sys.exit(app.exec_())

def b1_clicked():
   print("Button 1 clicked")

if __name__ == '__main__':
   window()