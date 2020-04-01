# https://www.bilibili.com/video/av75871530?p=3

# coding=utf-8

from matplotlib import  pyplot as plt   # 导入 pyplot

x = range(2, 26, 2)                                     # 数据在 x 轴的位置，是一个可迭代对象
y = [15, 13, 14.5, 17, 20, 25, 26, 26, 24, 22, 18, 15]  # 数据在 y 轴的位置，是一个可迭代对象

plt.plot(x, y)                                          # 绘图
plt.show()                                              # 显示