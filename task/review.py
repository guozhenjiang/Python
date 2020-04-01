from datetime import datetime

#-----------------------------------------------------------
print("hello world")
#-----------------------------------------------------------

#这是一个注释的用法
# 注释的快捷键 ctrl + /

#-------------------------------------------------------------

#数据类型-----------------
#---Number（数字） 包含 int、float、bool、complex（复数）
#---String（字符串）
#---List（列表）  list[]   列表的元素可以是不同类型。要了解[0:2]列表截取的概念。了解列表的索引 0开始。[1:]和[:]和[:2]
#---Tuple（元组） tuple() 与list类似 里面元素不能修改。索引与list一样
#---Set（集合）由一个或数个形态各异的大小整体组成的，构成集合的事物或对象称作元素或是成员。{}创建，空集合用set().空{}是来创建字典的
#---Dictionary（字典） 无序的对象集合。是一个无序的 键(key) : 值(value) 的集合


name =["李召","董晗","李超","王泽坤","郭振江"] 
print(name)
print(len(name))#打印列表的长度

dict = {}
dict["one"] = "py-第一周"
dict["two"] = "py-第二周"

namedict = {"name1": "zhao","name2": "KUNKUN",}

print(dict["one"]) #输出键为 'one' 的值
print(dict["two"]) #输出键为 'two' 的值
print(namedict) #输出完整的字典
print(namedict.keys()) #输出所有键
print(namedict.values())# 输出所有值

print(len(namedict))#打印字典的长度

a = 1
b = 1.0
print(a)
print(b)
c = input("enter something:   ") #输入获取的类型默认是字符串
#如果不知道我们可以用 type() 来判断数据类型
print(type(c))  

#eval()是将字符串转换成数字类型 输入有小数的自动转换成float
c = eval(c)

print(type(c))

#----------------------------------------------------------------------------------

#-----------------算数运算符----------------------

#   +  -  *  /  %（取余） **（幂运算）  // （取整除）

#---使用过程注意变量的类型！！！-------------

a1 = float(input("enter a number:   "))
b1 = float(input("enter a number:   "))
c1 = a1 * b1
print(c1)
#------------------比较运算符--------------------
#------------------逻辑运算符--------------------
#  and  布尔 与  x and y   x 为 False，x and y 返回 False，否则它返回 y 的计算值
#  or   布尔 或  x  or y   x 为 True，它返回 x 的值，否则它返回 y 的计算值
#  not  布尔 非    not x   x 为 True，返回 False 。如果 x 为 False，它返回 True
# 注意：视频中讲到 如果不是用于 字符串，True False是PY的关键字

a2 = 5
b2 = 6
print(a2 and b2)
print(a2 or b2)
print(not a2)

#------------------条件语句 if-----------------
a3 = 6
b3 = 7
if  (a3 < b3) :
    print("yeah")
else :
    print("no")

if  (a3 > b3) :
    print("yeah")
elif  (a3 < b3):
    print("no")
#------------------注意：行与缩进------------------
#---python是使用  缩进  来表示代码块，不像C语音一样 需要使用大括号 {}
#---缩进的空格数是可变的，但是同一个代码块的语句必须包含相同的缩进空格数，否则会报错

#-----------------while else 循环----------------------
a4 = 0

while a4 < 10 :#有条件循环
    print(a4)
    a4 = a4 + 1
else:
    print("a4 > 10")

a5 = 1

# while a5 == 1 :
#     TEXT = eval(input("ENTER A NUM:   "))
#     print (TEXT)
# print ("程序不会运行到这里！！")

#------------------for 循环-------------------------------
a6 = ["李召","董晗","李超","王泽坤","郭振江"]  
for b6 in a6 :
    print(b6) #遍历所有列表里的元素

#-----------------range() 函数----------------------------
#--如果你需要遍历数字序列，可以使用内置range()函数。它会生成数列
for a7 in range(2,9):
    print(a7)

for b7 in range(6) :
    print(b7)#注意打印是从0开始

#-----------------format 格式化函数----------------
name1 = "LiZhao"
name2 = "DongHan"
output = "Hello  " + name1 + " " + name2   #1
print(output)
output = "Hello, {} {} ".format(name1,name2)  #2
print(output)
output = "Hello, {1} {0} ".format(name1,name2)  #3 不止局限于2个元素
print(output)
output = f"Hello, {name1} {name2}"      #4  仅在py3
print(output)

#---------------------datetime------------------------------------
current_date = datetime.now()
print(current_date)

#---------------------错误处理-----------------
#语法错误、逻辑错误、运行错误
#--------try/except/finally-----------

x = 8
y = 0

print()

try:
    print(x / y)
    print("c")
except ZeroDivisionError as e:
    print("not allowed to divide by 0")
else:
    print("wrong")
finally:
    print("this is our cleanup code")

print()