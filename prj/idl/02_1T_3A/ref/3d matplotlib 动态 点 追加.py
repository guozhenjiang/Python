import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from numpy.random import random

# Number of particles
numP = 2
# Dimensions
DIM = 3
timesteps = 2000

x, y, z = random(timesteps), random(timesteps), random(timesteps)

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Setting the axes properties
border = 1
ax.set_xlim3d([-border, border])
ax.set_ylim3d([-border, border])
ax.set_zlim3d([-border, border])
line = ax.plot(x[:1], y[:1], z[:1], 'o')[0]


def animate(i):
    global x, y, z, numP
    idx1 = numP*(i+1)
    # join x and y into single 2 x N array
    xy_data = np.c_[x[:idx1], y[:idx1]].T
    line.set_data(xy_data)
    line.set_3d_properties(z[:idx1])

ani = animation.FuncAnimation(fig, animate, frames=timesteps, interval=1, blit=False, repeat=False)
plt.show()