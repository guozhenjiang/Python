from pyglet.gl import *
from math import *

# tex = pyglet.image.load('biosphere.png').get_texture()

step = 10

vlists = []
for lat in range(-90,90,step):
    verts = []
    texc = []
    for lon in range(-180,181,step):
        x = -cos(radians(lat)) * cos(radians(lon))
        y = sin(radians(lat))
        z = cos(radians(lat)) * sin(radians(lon))
        s = (lon+180) / 360.0
        t = (lat+90) / 180.0
        verts += [x,y,z]
        texc += [s,t]
        x = -cos(radians((lat+step))) * cos(radians(lon))
        y = sin(radians((lat+step)))
        z = cos(radians((lat+step))) * sin(radians(lon))
        s = (lon+180) / 360.0
        t = ((lat+step)+90) / 180.0
        verts += [x,y,z]
        texc += [s,t]
    vlist = pyglet.graphics.vertex_list(len(verts)/3, ('v3f', verts), ('t2f', texc))
    vlists.append(vlist)

window = pyglet.window.Window(1024,512)

angle = 0

glEnable(GL_DEPTH_TEST)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2,2,-1,1,-1,1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(angle, 0, 1, 0)
    glColor3f(1,1,1)
    glEnable(GL_TEXTURE_2D)
    # glBindTexture(GL_TEXTURE_2D, tex.id)
    for v in vlists:
        v.draw(GL_TRIANGLE_STRIP)

def update(dt):
    global angle
    angle = angle + 1

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()