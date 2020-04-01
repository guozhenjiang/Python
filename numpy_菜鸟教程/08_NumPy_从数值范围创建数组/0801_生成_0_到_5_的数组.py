'''
--------------------------------------------------
numpy.arange
numpy 包中的使用 arange 函数创建数值范围并返回 ndarray 对象，函数格式如下：

numpy.arange(start, stop, step, dtype)
根据 start 与 stop 指定的范围以及 step 设定的步长，生成一个 ndarray。

参数说明：

参数	 描述
start	起始值，默认为0
stop	终止值（不包含）
step	步长，默认为1
dtype	返回ndarray的数据类型，如果没有提供，则会使用输入数据的类型。

--------------------------------------------------
'''

import numpy as np

x = np.arange(5)

print (x)

'''
[0  1  2  3  4]
'''