# 类型字段名可以用于存取实际 age 列
import numpy as np

dt = np.dtype([('age', np.int8)])
a = np.array([(10,), (20,), (30,)], dtype = dt)
print(a['age'])

'''
[10 20 30]
'''