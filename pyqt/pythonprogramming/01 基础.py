import sys

from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
window = QWidget()
# window.setGeometry(0, 0, 500, 300)
window.setWindowTitle('PyQT Tuts!')
window.show()

sys.exit(app.exec_())