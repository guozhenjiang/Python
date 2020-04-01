'''
https://www.runoob.com/numpy/numpy-matplotlib.html
'''

'''
--------------------------------------------------

--------------------------------------------------
'''

import time
import numpy as np
from matplotlib import pyplot as plt

# 可使用中文
plt.rcParams['font.sans-serif'] = ['SimHei']

x = np.arange(1,11) 
y =  2 * x +  5 
plt.title("Matplotlib demo") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption") 

shape = ['-', '--', '-.']
color = ['b', 'g', 'r']

for sp_id in range(len(shape)):
    for cl_id in range(len(color)):
        op = shape[sp_id] + color[cl_id]
        print('op = ', op)
        #plt.plot(x, y, op) 
        plt.subplot(x, y, op)
        plt.show()
        #plt.close()
        time.sleep(1)