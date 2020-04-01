# https://www.bilibili.com/video/av75871530?p=4

# coding=utf-8

from matplotlib import  pyplot as plt   # 导入 pyplot

x = range(2, 26, 2)                                     # 数据在 x 轴的位置，是一个可迭代对象
y = [15, 13, 14.5, 17, 20, 25, 26, 26, 24, 22, 18, 15]  # 数据在 y 轴的位置，是一个可迭代对象

plt.figure(figsize=(20, 8), dpi=80)                     # 设置图片大小

plt.plot(x, y)                                          # 绘图

# plt.xticks(x)                                           # 设置 x 轴刻度

# _xtick_labels = [i/2 for i in range(4, 49)]             # 使出现小数点
# plt.xticks(_xtick_labels)
# plt.xticks(_xtick_labels[::3])                          # 从列表中每隔 3 个取一个
plt.xticks(range(25, 50))                               # x 轴上仅 25~50 有刻度

plt.savefig('./0406.png')                               # 保存到当前目录下

plt.show()                                              # 显示