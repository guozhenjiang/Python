# https://www.bilibili.com/video/av75871530?p=5

from matplotlib import pyplot as plt
import random

x = range(0, 120)
y = [random.randint(20, 35) for i in range(120)]

plt.figure(figsize=(20, 8), dpi=80)                     # 设置图片大小

plt.plot(x, y)
plt.show()