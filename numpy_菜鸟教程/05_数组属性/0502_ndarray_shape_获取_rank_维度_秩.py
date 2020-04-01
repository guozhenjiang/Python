'''
ndarray.shape
ndarray.shape 表示数组的维度，返回一个元组，
这个元组的长度就是维度的数目，即 ndim 属性(秩)。
比如，一个二维数组，其维度表示"行数"和"列数"。

ndarray.shape 也可以用于调整数组大小。
'''

import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6]])
print(a.shape)

'''
(2, 3)
'''