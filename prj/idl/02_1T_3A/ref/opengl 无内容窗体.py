# https://www.youtube.com/watch?v=FaVrz3SKYJ8

import sys
from PySide2 import QtCore, QtGui, QtOpenGL
from OpenGL.GL import *
from PySide2.QtWidgets import QApplication

class GLDemo(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.xsize = 512
        self.ysize = 512
    
    def initializeGL(self):
        glClearColor()
    
    def paintGL(self):
        glClearColor()
        
    def resizeGL(self):
        glClearColor()

app = QApplication()
ex = GLDemo()
ex.show()
app.exec_()