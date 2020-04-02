from testui import *
import sys

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
            QtWidgets.QWidget.__init__(self, parent)
            
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            
            self.ui.pushButton.clicked.connect(lambda:self.pushButton_clicked_())

    def pushButton_clicked_(self):
        print('pushButton_clicked')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    
    myapp.pushButton_clicked_()
    
    sys.exit(app.exec_())
