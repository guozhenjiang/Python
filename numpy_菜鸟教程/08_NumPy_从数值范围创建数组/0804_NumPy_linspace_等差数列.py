'''
--------------------------------------------------
numpy.linspace
numpy.linspace 函数用于创建一个一维数组，数组是一个等差数列构成的，格式如下：

np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
参数说明：

参数	     描述
start	    序列的起始值
stop	    序列的终止值，如果endpoint为true，该值包含于数列中
num	        要生成的等步长的样本数量，默认为50
endpoint	该值为 true 时，数列中中包含stop值，反之不包含，默认是True。
retstep	    如果为 True 时，生成的数组中会显示间距，反之不显示。
dtype	    ndarray 的数据类型

--------------------------------------------------
'''

import numpy as np

a = np.linspace(1, 10, 10)
print('a = np.linspace(1, 10, 10)')
print(a)

b = np.linspace(1, 10, 10, True)
print('b = np.linspace(1, 10, 10, True)')
print(b)

c = np.linspace(1, 10, 10, False)
print('c = np.linspace(1, 10, 10, False)')
print(c)

'''
a = np.linspace(1, 10, 10)
[ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
b = np.linspace(1, 10, 10, True)
[ 1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
c = np.linspace(1, 10, 10, False)
[1.  1.9 2.8 3.7 4.6 5.5 6.4 7.3 8.2 9.1]
'''

# 所以默认 endpoint = True