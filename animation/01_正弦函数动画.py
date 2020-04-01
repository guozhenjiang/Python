# https://morvanzhou.github.io/tutorials/data-manipulation/plt/5-1-animation/

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)
line, = ax.plot(x, np.sin(x))

def my_animate(i):
    line.set_ydata(np.sin(x+i/100))
    # return line

def my_init():
    line.set_ydata(np.sin(x))
    # return line

ani = animation.FuncAnimation(fig=fig, func=my_animate, frames= 100, init_func=my_init, interval=20, blit=False)
plt.show()