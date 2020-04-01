# https://www.bilibili.com/video/av84661467?from=search&seid=17104204555378448114
import csv

file_r = open('01_csv_r.csv', 'r')
print('\r\n打开 %s' %(file_r.name))

reader = csv.reader(file_r)
print('\r\n%s reader 用来读取文件内容' %(type(reader)))

a = list(reader)
print('\r\n%s a 保存了 reader 的内容:' %(type(a)))
print(a)

'''

打开 01_csv_r.csv

<class '_csv.reader'> reader 用来读取文件内容

<class 'list'> a 保存了 reader 的内容:
[['序号', '姓名', '性别', '年龄'], ['1', 'A', '男', '16'], ['2', 'B', '女', '17'], ['3', 'C', '男', '18'], ['4', 'D', '女', '19'], ['5', 'E', '男', '20']]
'''