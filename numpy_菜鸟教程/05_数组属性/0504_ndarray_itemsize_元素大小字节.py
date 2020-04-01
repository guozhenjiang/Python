'''
ndarray.itemsize
ndarray.itemsize 以字节的形式返回数组中每一个元素的大小。

例如，一个元素类型为 float64 的数组 itemsiz 属性值为 8
(float64 占用 64 个 bits，每个字节长度为 8，所以 64/8，
占用 8 个字节），
又如，一个元素类型为 complex32 的数组 item 属性为 4（32/8）。
'''

import numpy as np

# 数组的 dtype 为 int8(一个字节)
x = np.array([1, 2, 3, 4, 5], dtype = np.int8)
print(x.itemsize)

# 数组的 dtype 现在为 float64(八个字节)
y = np.array([1, 2, 3, 4, 5], dtype = np.float64)
print(y.itemsize)

'''
1
8
'''