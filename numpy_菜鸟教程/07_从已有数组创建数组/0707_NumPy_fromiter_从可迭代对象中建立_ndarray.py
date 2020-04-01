'''
--------------------------------------------------
numpy.fromiter
numpy.fromiter 方法从可迭代对象中建立 ndarray 对象，返回一维数组。

numpy.fromiter(iterable, dtype, count=-1)
参数	     描述
iterable    可迭代对象
dtype       返回数组的数据类型
count       读取的数据数量，默认为-1，读取所有数据

--------------------------------------------------
'''

#numpy.fromiter 方法从可迭代对象中建立 ndarray 对象，返回一维数组。

import numpy as np

# 使用 range 函数创建列表对象
list = range(5)
it = iter(list)

# 使用迭代器创建 ndarray
x = np.fromiter(it, dtype = float)

print(x)

'''
[0. 1. 2. 3. 4.]
'''