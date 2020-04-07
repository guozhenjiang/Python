# from PySide2 import QtOpenGL
# from PySide2 import QGLWidget

# from PySide2.QtWidgets import *
from PySide2.QtOpenGL import *

class MyGLDrawer(QGLWidget):
    
    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        
        self.initializeGL()
        pass

    def initializeGL(self):
        # Set up the rendering context, define display lists etc.:
        # user_program
        self.glClearColor(0.0, 0.0, 0.0, 0.0)
        self.glEnable(GL_DEPTH_TEST)
        # user_program

    def resizeGL(self, w, h):
        # setup viewport, projection etc.:
        glViewport(0, 0, w, h)
        # user_program
        glFrustum() # user_program
        # user_program
        
    def paintGL(self):
        # draw the scene:
        # user_program
        glRotatef() # user_program
        glMaterialfv() # user_program
        glBegin(GL_QUADS)
        glVertex3f() # user_program
        glVertex3f() # user_program
        # user_program
        glEnd()
        # user_program

import sys
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyGLDrawer()
    window.show()
    res = app.exec_()
    window.freeResources()
    sys.exit(res)
