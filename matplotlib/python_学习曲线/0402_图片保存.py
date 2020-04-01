# https://www.bilibili.com/video/av75871530?p=4

# coding=utf-8

from matplotlib import  pyplot as plt   # 导入 pyplot

x = range(2, 26, 2)                                     # 数据在 x 轴的位置，是一个可迭代对象
y = [15, 13, 14.5, 17, 20, 25, 26, 26, 24, 22, 18, 15]  # 数据在 y 轴的位置，是一个可迭代对象

plt.figure(figsize=(20, 8), dpi=80)                     # 设置图片大小

plt.plot(x, y)                                          # 绘图

plt.savefig('./0402.png')                               # 保存到当前目录下
plt.savefig('./0402.svg')                               # 保存到当前目录下

plt.show()                                              # 显示