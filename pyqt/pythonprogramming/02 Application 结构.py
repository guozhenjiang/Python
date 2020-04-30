import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Window by Class Window')
        self.show()

app = QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = Window()
    
#     sys.exit(app.exec_())