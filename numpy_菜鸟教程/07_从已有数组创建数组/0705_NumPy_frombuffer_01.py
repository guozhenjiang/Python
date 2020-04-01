'''
--------------------------------------------------
numpy.frombuffer
numpy.frombuffer 用于实现动态数组。
numpy.frombuffer 接受 buffer 输入参数，以流的形式读入转化成 ndarray 对象。

numpy.frombuffer(buffer, dtype = float, count = -1, offset = 0)
    注意：buffer 是字符串的时候，Python3 默认 str 是 Unicode 类型，所以要转成 bytestring 在原 str 前加上 b。

参数说明：

参数	 描述
buffer	可以是任意对象，会以流的形式读入。
dtype	返回数组的数据类型，可选
count	读取的数据数量，默认为-1，读取所有数据。
offset  读取的起始位置，默认为0。

--------------------------------------------------
'''

import  numpy as np

s = b'Hello World'
a = np.frombuffer(s, dtype = 'S1')

print(a)

'''
[b'H' b'e' b'l' b'l' b'o' b' ' b'W' b'o' b'r' b'l' b'd']
'''