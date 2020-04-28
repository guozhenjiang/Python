
'''
1   Number      数字
2   String      字符串  ''
3   List        列表    []
4   Tuple       元组    ()
5   Set         集合    {}  使用 set() 创建
6   Dictionary  字典    ()

Number 包括：
    int  float  bool  complex

不可变数据：
    Number      数字
    String      字符串
    Tuple       元组

可变数据：
    List        列表
    Dicitionary 字典
    Set         集合

注意：
    Python 2 里面有 long
    Python 3 里只有 int

查看对象类型：
    可以使用 type() 查看对象的类型
    也可以用 isinstance() 查看对象类型
    区别是：
        type() 认为子类不是一种父类类型
        isinstance() 认为子类是一种父类类型

'''

a, b, c, d = 20, 5.5, True, 4+3j
print(type(a), type(b), type(c), type(d))
'''
<class 'int'> <class 'float'> <class 'bool'> <class 'complex'>
'''

class A:
    pass

class B(A):
    pass

print(isinstance(A(), A))
print(type(A()) == A)
print(isinstance(B(), A))
print(type(B) == A)
'''
True
True
True
False
'''

