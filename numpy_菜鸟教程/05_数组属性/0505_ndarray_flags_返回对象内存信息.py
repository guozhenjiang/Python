'''
ndarray.flags
ndarray.flags 返回 ndarray 对象的内存信息，包含以下属性：

属性                 描述
C_CONTIGUOUS (C)    数据是在一个单一的C风格的连续段中
F_CONTIGUOUS (F)	数据是在一个单一的Fortran风格的连续段中
OWNDATA (O)         数组拥有它所使用的内存或从另一个对象中借用它
WRITEABLE (W)       数据区域可以被写入，将该值设置为 False，则数据为只读
ALIGNED (A)         数据和所有元素都适当地对齐到硬件上
UPDATEIFCOPY (U)    这个数组是其它数组的一个副本，当这个数组被释放时，原数组的内容将被更新
'''

import numpy as np

x = np.array([1, 2, 3, 4, 5])
print(x.flags)

'''
1
8
'''