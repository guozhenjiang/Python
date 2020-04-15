import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 简单Demo
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')  # (这种方法是通过X，Y和Z构建一个矩阵，XYZ各取一个点，这里有四个点）
X = [1, 1, 2, 2]
Y = [3, 4, 4, 3]
Z = [1, 2, 1, 1]

# 绘制曲面 (四个点可以确定一个四面体)
# ax.plot_trisurf(X, Y, Z) 
# 绘制散点图
ax.scatter(X, Y, Z)
plt.show()