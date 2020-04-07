import pyglet
from pyglet.gl import *

win = pyglet.window.Window()

@win.event
def on_draw():
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw outlines only
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
    # Draw some stuff
    glBegin(GL_POLYGON)
    glVertex2i(100, 100)
    glVertex2i(200, 100)
    glVertex2i(200, 200)
    glVertex2i(100, 200)
    
    glVertex2i(10, 300)
    glVertex2i(50, 50)
    # glVertex2i(400, 400)
    # glVertex2i(400, 300)
    glEnd()

pyglet.app.run()