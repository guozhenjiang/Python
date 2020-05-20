import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QWidget()
        self.cw_layout = QHBoxLayout()
        self.central_widget.setLayout(self.cw_layout)
        self.setCentralWidget(self.central_widget)

        self.line = LineEdit()
        self.kb = KeyBoard(self.line)

        self.cw_layout.addWidget(self.line)

        self.create_connections()

    def create_connections(self):
        self.line.signal_evoke_kb.connect(self.show_kb)

    def show_kb(self):
        if self.kb.isHidden():
            self.kb.show()
        else:
            self.kb.hide()


class LineEdit(QLineEdit):

    signal_evoke_kb = pyqtSignal()

    def __init__(self):
        super(LineEdit, self).__init__()

    def mousePressEvent(self, QMouseEvent):
        super(LineEdit, self).mousePressEvent(QMouseEvent)
        self.signal_evoke_kb.emit()

class Key(QPushButton):

    def __init__(self, name, event, receiver):
        super(Key, self).__init__()
        self.name = name
        self.event = event
        self.setText(name)


class KeyBoard(QWidget):

    def __init__(self, receiver):
        super(KeyBoard, self).__init__()
        self.receiver = receiver
        self.layout = QHBoxLayout()
        self.keys = ['q','w','e','r','t','y']
        self.dict_keys ={'q':Qt.Key_Q,'w':Qt.Key_W,'e':Qt.Key_E,'r':Qt.Key_R,'t':Qt.Key_T,'y':Qt.Key_Y,}
        for key in self.keys:
            key_keyboard = Key(key,self.dict_keys[key],receiver)
            key_keyboard.clicked.connect(self.key_pressed)
            self.layout.addWidget(key_keyboard)
        self.setLayout(self.layout)

    def key_pressed(self):
        try:
            event = QKeyEvent(QEvent.KeyPress, self.sender().event, Qt.NoModifier,
                              self.sender().name, False)
            QCoreApplication.postEvent(self.receiver, event)
        except Exception as e:
            print(e)

    def keyPressEvent(self, evt):
        event = QKeyEvent(QEvent.KeyPress, evt.key(), evt.modifiers(),
                          evt.text(), False)
        QCoreApplication.postEvent(self.receiver, event)
        evt.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())