'''
--------------------------------------------------
numpy.ones
创建指定形状的数组，数组元素以 1 来填充：

numpy.ones(shape, dtype = None, order = 'C')
参数说明：

参数	 描述
shape	数组形状
dtype	数据类型，可选
order	'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组

--------------------------------------------------
'''

import numpy as np

# 默认为浮点数
x = np.ones(5)
print(x)

# 自定义类型
x = np.ones((2, 2), dtype = int)
print(x)

'''
[1. 1. 1. 1. 1.]
[[1 1]
 [1 1]]
'''