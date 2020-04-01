# 将数据类型应用于 ndarray 对象
import numpy as np

dt = np.dtype([('age', np.int8)])
a = np.array([(10,), (20,), (30,)], dtype = dt)
print(a)

'''
[(10,) (20,) (30,)]
'''