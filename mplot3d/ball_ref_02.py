from mpl_toolkits.mplot3d import Axes3D, axes3d
import matplotlib.pyplot as plt
import numpy as np

center = [1,2,3]    # 球心坐标
radius = 10         # 球半径

# 球面描述
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

# 绘图
fig = plt.figure()
ax = fig.add_subplot(131, projection='3d')

# 绘制表面
ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')

# 绘制框架
ax = fig.add_subplot(133, projection='3d')
ax.plot_wireframe(x, y, z, rstride=10, cstride=10, color='b')

# 显示
plt.show()