'''
https://www.runoob.com/numpy/numpy-array-creation.html

--------------------------------------------------
NumPy 创建数组
ndarray 数组除了可以使用底层 ndarray 构造器来创建外，也可以通过以下几种方式来创建。

--------------------------------------------------
numpy.empty
numpy.empty 方法用来创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组：

numpy.empty(shape, dtype = float, order = 'C')
参数说明：

参数	 描述
shape   数组形状
dtype	数据类型，可选
order	有"C"和"F"两个选项,分别代表，行优先和列优先，在计算机内存中的存储元素的顺序。

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