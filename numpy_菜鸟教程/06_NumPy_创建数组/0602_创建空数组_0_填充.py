'''
--------------------------------------------------
numpy.zeros
创建指定大小的数组，数组元素以 0 来填充：

numpy.zeros(shape, dtype = float, order = 'C')
参数说明：

参数	 描述
shape	数组形状
dtype	数据类型，可选
order   'C' 用于 C 的行数组，或者 'F' 用于 FORTRAN 的列数组

--------------------------------------------------
'''

import numpy as np

# 默认为浮点数
x = np.zeros(5)
print(x)

# 设置类型为整数
y = np.zeros((5,), dtype = np.int)
print(y)

# 自定义类型
z = np.zeros((2, 2), dtype = [('x', 'i4'), ('y', 'i4')])
print(z)

'''
[0. 0. 0. 0. 0.]
[0 0 0 0 0]
[[(0, 0) (0, 0)]
 [(0, 0) (0, 0)]]
'''