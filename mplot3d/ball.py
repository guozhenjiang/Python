from mpl_toolkits.mplot3d import Axes3D, axes3d
import matplotlib.pyplot as plt
import numpy as np
import time

class Location:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

Anchor_1 = Location('A1', 0, 0, 0)
Anchor_2 = Location('A2', 0, 0, 5)
Anchor_3 = Location('A3', 0, 5, 0)
Anchor_4 = Location('A4', 0, 5, 5)
Anchor_5 = Location('A5', 5, 0, 0)
Anchor_6 = Location('A6', 5, 0, 5)
Anchor_7 = Location('A7', 5, 5, 0)
Anchor_8 = Location('A8', 5, 5, 5)

def DrawBall(subplot, anchor, distance, color):
    # 球面描述
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = distance * np.outer(np.cos(u), np.sin(v)) + anchor.x
    y = distance * np.outer(np.sin(u), np.sin(v)) + anchor.y
    z = distance * np.outer(np.ones(np.size(u)), np.cos(v)) + anchor.z
    
    subplot.plot_surface(x, y, z,  rstride=4, cstride=4, color=color)

# 绘图
fig = plt.figure()
subplot_1 = fig.add_subplot(131, projection='3d')

center = [1,2,3]    # 球心坐标
radius = 10         # 球半径

# 球面描述
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

# 绘制表面
subplot_1.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')
subplot_1.legend()

# time.sleep(5)

# 绘制框架
subplot_2 = fig.add_subplot(132, projection='3d')
subplot_2.legend()
subplot_2.plot_wireframe(x, y, z, rstride=10, cstride=10, color='r')

subplot_3 = fig.add_subplot(133, projection='3d')
subplot_3.legend()

# r g b y c m k w
# DrawBall(subplot_3, Anchor_1, 2, 'r')
# DrawBall(subplot_3, Anchor_2, 2, 'g')
# DrawBall(subplot_3, Anchor_3, 2, 'b')
# DrawBall(subplot_3, Anchor_4, 2, 'y')

# DrawBall(subplot_3, Anchor_5, 2, 'c')
# DrawBall(subplot_3, Anchor_6, 2, 'm')
# DrawBall(subplot_3, Anchor_7, 2, 'k')
# DrawBall(subplot_3, Anchor_8, 2, 'w')

# 显示
# plt.show()
# time.sleep(1)

# subplot_3.cal()
# plt.show()
# time.sleep(1)

DrawBall(subplot_3, Anchor_1, 2, 'r')
DrawBall(subplot_3, Anchor_2, 2, 'g')
DrawBall(subplot_3, Anchor_3, 2, 'b')
DrawBall(subplot_3, Anchor_4, 2, 'y')
plt.show()