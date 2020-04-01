import csv

# 读取 csv 文件
file_r = open('01_csv_r.csv', 'r')    # 打开 csv 文件
print('\r\n打开 %s' %(file_r.name))

reader = csv.reader(file_r)           # 这儿并不是读取到了文件的全部内容 不能在这句后面关闭文件
print('\r\n%s reader 用来读取文件内容' %(type(reader)))

data = []                               # 用 list(列表) 存放读取到的内容 字符/字符串
print('\r\n', type(data), ' 类型的 data 用来存放 %s 文件内容' %(file_r.name))

print('\r\n文件的每一项(行)是:')
for i in reader:
    print(i)                            # 输出每一行内容
    data.append(i)

file_r.close()                        # 关闭文件
print('\r\n关闭了 %s' %(file_r.name))

print('\r\n整个文件的内容是:')
print(data)                             # 输出整个文件内容


'''

打开 01_csv_r.csv

<class '_csv.reader'> reader 用来读取文件内容

 <class 'list'>  类型的 data 用来存放 01_csv_r.csv 文件内容

文件的每一项(行)是:
['a1', '123']
['a2', '456']
['a3', '789']

关闭了 01_csv_r.csv

整个文件的内容是:
[['a1', '123'], ['a2', '456'], ['a3', '789']]
'''