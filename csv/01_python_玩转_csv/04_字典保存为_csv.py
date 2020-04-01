import csv

data = {'小明':123, '小红':654}
print('\r\n创建了 %s data:' %(type(data)))
print(data)

file_w = open('04_csv_w.csv', 'w', newline='', encoding='utf-8')
print('\r\n创建/覆盖 %s' %(file_w.name))

writer = csv.writer(file_w)
print('\r\n%s writer 用来写入文件内容' %(type(writer)))

print('\r\n准备写入到 %s 每一项(行)是:' %(file_w.name))
for i in data:
    print(data[i])
    writer.writerow([i, data[i]])

file_w.close()
print('\r\n关闭了 %s' %(file_w.name))


'''

创建了 <class 'dict'> data:
{'小明': 123, '小红': 654}

创建/覆盖 04_csv_w.csv

<class '_csv.writer'> writer 用来写入文件内容

准备写入到 04_csv_w.csv 每一项(行)是:
123
654

关闭了 04_csv_w.csv
'''