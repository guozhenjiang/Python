# https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py

# sphinx_gallery_thumbnail_number = 3
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()              # an empty figure with no Axes
fig, ax = plt.subplots()        # a figure with a single Axes
fig, axs = plt.subplots(2, 2)   # a figure with a 2x2 grid of Axes

plt.show()

'''
    以上操作绘出来 3 个 独立的 figure
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