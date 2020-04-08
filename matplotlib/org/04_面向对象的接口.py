# https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py

# sphinx_gallery_thumbnail_number = 3
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2, 100)

# Note that even in the OO-style, we use `.pyplot.figure` to create the figure.
fig, ax = plt.subplots()                # Create a figure and an axes.
ax.plot(x, x, label='linear')           # Plot some data on the axes.
ax.plot(x, x**2, label='quadratic')     # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')         # ... and some more.
ax.set_xlabel('x label')                # Add an x-label to the axes.
ax.set_ylabel('y label')                # Add a y-label to the axes.
ax.set_title("Simple Plot")             # Add a title to the axes.
ax.legend()                             # Add a legend.

plt.show()

'''
    Axes: 轴
        控制数据限制
            axes.Axes.set_xlim()
            axes.Axes.set_ylim()
        
        设置而 Axes 标题
            set_title()
            set_xlabel()
            set_ylabel()
    Axis: 轴
        Locator
        Formatter
    
    Artist:
        
'''