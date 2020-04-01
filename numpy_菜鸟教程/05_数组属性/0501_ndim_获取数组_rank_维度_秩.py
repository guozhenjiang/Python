'''
ndarray.ndim
ndarray.ndim 用于返回数组的维数，等于秩。
'''

import numpy as np

a = np.arange(24)
print(a.ndim)           # a 现在只有一个维度

# 现在调整其大小
b = a.reshape(2, 4, 3)  # b 现在拥有三个维度
print(b.ndim)

'''
1
3
'''