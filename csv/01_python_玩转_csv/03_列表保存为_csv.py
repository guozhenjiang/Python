import csv

data = [['b1', 111], ['b2', 222], ['b3', 333]]
print('\r\n创建了 %s data 内容:' %(type(data)))
print(data)

file_w = open('03_csv_w.csv', 'w', newline='')
print('\r\n打开 %s' %(file_w.name))

writer = csv.writer(file_w)
print('\r\n%s writer 用来写入文件内容' %(type(writer)))

print('\r\n向 %s 写入:' %(file_w.name))
for i in range(len(data)):
    writer.writerow(data[i])
    print(data[i])

file_w.close()
print('\r\n关闭了 %s' %(file_w.name))


'''

创建了 <class 'list'> data 内容:
[['b1', 111], ['b2', 222], ['b3', 333]]

打开 03_csv_w.csv

<class '_csv.writer'> writer 用来写入文件内容

向 03_csv_w.csv 写入:
['b1', 111]
['b2', 222]
['b3', 333]

关闭了 03_csv_w.csv
'''