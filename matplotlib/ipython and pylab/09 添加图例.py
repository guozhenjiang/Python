# 导入 matplotlib 的所有内容（nympy 可以用 np 这个名字来使用）
from pylab import *

# 创建一个 8 * 6 点（point）的图，并设置分辨率为 80
# figure(figsize=(8,6), dpi=80)
figure(figsize=(10,6), dpi=80)

# 创建一个新的 1 * 1 的子图，接下来的图样绘制在其中的第 1 块（也是唯一的一块）
subplot(1,1,1)

X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
C,S = np.cos(X), np.sin(X)

# # 绘制余弦曲线，使用蓝色的、连续的、宽度为 1 （像素）的线条
# # plot(X, C, color="blue", linewidth=1.0, linestyle="-")
# plot(X, C, color="blue", linewidth=2.5, linestyle="-")

# # 绘制正弦曲线，使用绿色的、连续的、宽度为 1 （像素）的线条
# # plot(X, S, color="green", linewidth=1.0, linestyle="-")
# plot(X, S, color="red",  linewidth=2.5, linestyle="-")

# # 设置横轴的上下限
# # xlim(-4.0,4.0)
# xlim(X.min()*1.1, X.max()*1.1)


# # 设置纵轴的上下限
# # ylim(-1.0,1.0)
# ylim(C.min()*1.1, C.max()*1.1)

xmin ,xmax = X.min(), X.max()
ymin, ymax = C.min(), C.max()

dx = (xmax - xmin) * 0.2
dy = (ymax - ymin) * 0.2

xlim(xmin - dx, xmax + dx)
ylim(ymin - dy, ymax + dy)

# # 设置横轴记号
# xticks(np.linspace(-4,4,9,endpoint=True))
# # 设置纵轴记号
# yticks(np.linspace(-1,1,5,endpoint=True))

# xticks( [-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
# yticks([-1, 0, +1])

xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
       [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

yticks([-1, 0, +1],
       [r'$-1$', r'$0$', r'$+1$'])

ax = gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
plot(X, S, color="red",  linewidth=2.5, linestyle="-", label="sine")

legend(loc='upper left')

# 以分辨率 72 来保存图片
# savefig("exercice_2.png",dpi=72)

# 在屏幕上显示
show()