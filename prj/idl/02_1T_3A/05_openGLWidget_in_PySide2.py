# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.uic import *
#
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
# from OpenGL.GLUT.freeglut import *
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
from PyQt5 import QtWidgets as qWidget
from PyQt5 import QtGui as qGui
from PyQt5 import QtCore as qCore
from PyQt5 import uic
import sys
import os

from OpenGL.GLUT import *
from OpenGL.GL import *
 
 
class mainWindow(qWidget.QMainWindow):
    """Main window class."""
 
    def __init__(self, *args):
        """Init."""
        super(mainWindow, self).__init__(*args)
        ui = os.path.join(os.path.dirname(__file__), 'test.ui')
        uic.loadUi(ui, self)
 
    def setupUI(self):
        print("\033[1;101m SETU6P UI \033[0m")
        # self.windowsHeight = self.openGLWidget.height()
        # self.windowsWidth = self.openGLWidget.width()
 
        self.openGLWidget.initializeGL()
        # self.openGLWidget.resizeGL(self.windowsWidth, self.windowsHeight)
        self.openGLWidget.paintGL = self.paintGL
        self.openGLWidget.initializeGL = self.initializeGL
 
    def paintGL(self):
        # self.loadScene()
        # glut.glutWireSphere(2, 13, 13)
        
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        # glBegin(GL_LINES)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glColor3f (1.0, 0.0, 0.0)
        
        glBegin(GL_QUADS)
        glVertex3i(-100, -1000, 0)
        glVertex3i(100, -100, 0)
        glVertex3i(100, 100, 0)
        glVertex3i(-100, 100, 0)
        glEnd()
        pass
 
    def initializeGL(self):
        print("\033[4;30;102m INITIALIZE GL \033[0m")
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f (1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        glVertex3i(-100, -1000, 0)
        glVertex3i(100, -100, 0)
        glVertex3i(100, 100, 0)
        glVertex3i(-100, 100, 0)
        glEnd()
 
    def loadScene(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        x, y, width, height = gl.glGetDoublev(gl.GL_VIEWPORT)
        glu.gluPerspective(
            45,  # field of view in degrees
            width / float(height or 1),  # aspect ratio
            .25,  # near clipping plane
            200,  # far clipping plane
        )
 
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
 
        glu.gluLookAt(12, 12, 12, 0, 0, 0, 0, 1, 0)
 
glutInit()
app = qWidget.QApplication(sys.argv)
window = mainWindow()
window.setupUI()
window.show()
sys.exit(app.exec_())