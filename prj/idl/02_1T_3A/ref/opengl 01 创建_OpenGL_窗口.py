import sys
from PyQt5 import QtCore, QtGui, QtOpenGL

class MyOpenGLWindow(QtGui.QOpenGLWindow):
    def __init__(self, **kwargs):
        QtGui.QOpenGLWindow.__init__(self)
        self.setTitle("MyQOpenGLWindow")
        self.setWidth(800)
        self.setHeight(800)
        
app = QtGui.QGuiApplication(sys.argv)
myWindow = MyOpenGLWindow()
myWindow.show()

app.exec_()