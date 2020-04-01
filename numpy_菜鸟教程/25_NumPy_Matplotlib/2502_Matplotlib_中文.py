'''
https://www.runoob.com/numpy/numpy-matplotlib.html
'''

'''
--------------------------------------------------
图形中文显示
Matplotlib 默认情况不支持中文，我们可以使用以下简单的方法来解决：

首先下载字体（注意系统）：https://www.fontpalace.com/font-details/SimHei/

SimHei.ttf 文件放在当前执行的代码文件中：
--------------------------------------------------
'''

# import numpy as np 
# from matplotlib import pyplot as plt 
# import matplotlib
 
# # fname 为 你下载的字体库路径，注意 SimHei.ttf 字体的路径
# # E:\gzj_kf\Python\NumPy_菜鸟教程\25_NumPy_Matplotlib
# zhfont1 = matplotlib.font_manager.FontProperties(C:\Windows\Fonts="SimHei.ttf") 
 
# x = np.arange(1,11) 
# y =  2  * x +  5 
# plt.title("中文标题", fontproperties=zhfont1) 
 
# # fontproperties 设置中文显示，fontsize 设置字体大小
# plt.xlabel("x 轴", fontproperties=zhfont1)
# plt.ylabel("y 轴", fontproperties=zhfont1)
# plt.plot(x, y) 
# plt.show()

import numpy as np 
from matplotlib import pyplot as plt 
import matplotlib

x = np.arange(1,11) 
y =  2 * x * x +  5 

# 可使用中文
plt.rcParams['font.sans-serif'] = ['SimHei']

plt.title("中文标题") 

plt.xlabel("x 轴")
plt.ylabel("y 轴")
plt.plot(x, y) 
plt.show()