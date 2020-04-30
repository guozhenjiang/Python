import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPlainTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('文本颜色')
        self.resize(800, 600)
        self.set_ui()
        
    def set_ui(self):
        self.text = QPlainTextEdit(self)
        self.setCentralWidget(self.text)
        self.text.appendPlainText('Hello')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())