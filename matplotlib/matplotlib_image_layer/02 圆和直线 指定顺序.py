import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

##################################################
#  解决中文字体显示问题
font = {
    'family' : 'SimHei'
};
mpl.rc('font', **font);
##################################################
# 随机设置坐标值
# %matplotlib inline
N = 3
x = np.random.rand(N)
y = np.random.rand(N)
##################################################
fig = plt.figure(figsize=[8,4])
ax = fig.add_subplot(121)
# 绘制circle
for xi,yi in zip(x,y):
    circle = mpatches.Circle((xi,yi), 0.05, ec="blue",fc='blue')
    circle.set_zorder(0)
    ax.add_patch(circle)
# 绘制Line 
line = mlines.Line2D(x,y,lw=3.,ls='-',alpha=1,color='red')
line.set_zorder(1)   
ax.add_line(line)
ax.set_title('先圆后线')

ax = fig.add_subplot(122)
# 绘制circle
for xi,yi in zip(x,y):
    circle = mpatches.Circle((xi,yi), 0.05, ec="blue",fc='blue')
    circle.set_zorder(1)
    ax.add_patch(circle)
# 绘制Line 
line = mlines.Line2D(x,y,lw=3.,ls='-',alpha=1,color='red')
line.set_zorder(0)
ax.add_line(line)
ax.set_title('先线后圆')
t=ax.get_xaxis()

plt.show()