import sys
import p022MainWinMenuToolbar

from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()

    ui = p022MainWinMenuToolbar.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    sys.exit(app.exec_())
