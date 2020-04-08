# https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py

# sphinx_gallery_thumbnail_number = 3
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')          # Plot some data on the (implicit) axes.
plt.plot(x, x**2, label='quadratic')    # etc.
plt.plot(x, x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()

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