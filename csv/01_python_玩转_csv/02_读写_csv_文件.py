import csv

# 读取 csv 文件
file_r = open('02_csv_r.csv', 'r')                      # 打开 csv 文件
print('\r\n打开 %s' %(file_r.name))

reader = csv.reader(file_r)                             # 这儿并不是读取到了文件的全部内容 不能在这句后面关闭文件
print('\r\n%s reader 用来读取文件内容' %(type(reader)))

data = []                                               # 用 list(列表) 存放读取到的内容 字符/字符串
print('\r\n', type(data), ' 类型的 data 用来存放 %s 文件内容' %(file_r.name))

for i in reader:
    print(i)                    # 输出每一行内容
    data.append(i)

file_r.close()                  # 关闭文件
print('\r\n关闭了 %s' %(file_r.name))

print('\r\n整个文件的内容是:')
print(data)                     # 输出整个文件内容


# 写入 csv 文件
file_w = open('02_csv_w.csv', 'w', newline='')          # 创建/覆盖 csv 文件
print('\r\n创建/覆盖 %s' %(file_w.name))

writer = csv.writer(file_w)
print('\r\n%s writer 用来写入文件内容' %(type(writer)))

m = len(data)
print('\r\n %s 一共有 %d 行' %(file_r.name, m))

print('\r\n准备写入到 %s 每一项(行)是:' %(file_w.name))
for i in range(m):
    print(data[i])
    writer.writerow(data[i])

file_w.close()
print('\r\n关闭了 %s' %(file_w.name))

'''

打开 02_csv_r.csv

<class '_csv.reader'> reader 用来读取文件内容

 <class 'list'>  类型的 data 用来存放 02_csv_r.csv 文件内容
['a1', '123']
['a2', '456']
['a3', '789']

关闭了 02_csv_r.csv

整个文件的内容是:
[['a1', '123'], ['a2', '456'], ['a3', '789']]

创建/覆盖 02_csv_w.csv

<class '_csv.writer'> writer 用来写入文件内容

 02_csv_r.csv 一共有 3 行

准备写入到 02_csv_w.csv 每一项(行)是:
['a1', '123']
['a2', '456']
['a3', '789']

关闭了 02_csv_w.csv
'''