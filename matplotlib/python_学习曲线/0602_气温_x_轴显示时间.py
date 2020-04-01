# https://www.bilibili.com/video/av75871530?p=6

from matplotlib import pyplot as plt
import random

plt.figure(figsize=(20, 8), dpi=80)                     # 设置图片大小

x = range(0, 120)
y = [random.randint(20, 35) for i in range(120)]

# 调整 x 轴刻度
_x = list(x)[::10]
_xtick_labels = ['hello, {}'.format(i) for i in _x]
plt.xticks(_x, _xtick_labels)

plt.plot(x, y)

plt.savefig('./0602.png')

plt.show()