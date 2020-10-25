import sys
import p013_MainWinFormLayout

from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()

    ui = p013_MainWinFormLayout.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    sys.exit(app.exec_())
