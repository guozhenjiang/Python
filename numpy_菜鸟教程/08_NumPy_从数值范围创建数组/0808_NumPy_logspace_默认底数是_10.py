'''
--------------------------------------------------
numpy.logspace
numpy.logspace 函数用于创建一个于等比数列。格式如下：

np.logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)
base 参数意思是取对数的时候 log 的下标。

参数         描述
start       序列的起始值为：base ** start
stop        序列的终止值为：base ** stop。如果endpoint为true，该值包含于数列中
num         要生成的等步长的样本数量，默认为50
endpoint    该值为 true 时，数列中中包含stop值，反之不包含，默认是True。
base        对数 log 的底数。
dtype       ndarray 的数据类型

--------------------------------------------------
'''

import numpy as np

# 默认底数是 10
a = np.logspace(1.0, 2.0, num=10)
print('np.logspace(1.0, 2.0, num=10)')
print(a)

'''
np.logspace(1.0, 2.0, num=10)
[ 10.          12.91549665  16.68100537  21.5443469   27.82559402
  35.93813664  46.41588834  59.94842503  77.42636827 100.        ]
'''