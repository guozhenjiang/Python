import csv

header = ['class', 'name', 'sex', 'height', 'year']
print('\r\n%s header：' %(type(header)))
print(header)

row = [    [1, 'xiaoming',     'male',     128,    23],
            [1, 'xiaohong',     'female',   162,    22],
            [2, 'xiaozhang',    'female',   163,    21],
            [2, 'xiaoli',       'male',     158,    21]
        ]
print('\r\n%s row:' %(type(row)))
print(row)

file_w_name = '01_csv_w.csv'

with open(file_w_name, 'w', newline='')as f:
    f_csv = csv.writer(f)
    f_csv.writerow(header)
    f_csv.writerows(row)

print('\r\n创建了 %s 并向其中添加了:' %(file_w_name))
print(header)
print(row)

'''

<class 'list'> header：
['class', 'name', 'sex', 'height', 'year']

<class 'list'> row:
[[1, 'xiaoming', 'male', 128, 23], [1, 'xiaohong', 'female', 162, 22], [2, 'xiaozhang', 'female', 163, 21], [2, 'xiaoli', 'male', 158, 21]]

创建了 01_csv_w.csv 并向其中添加了:
['class', 'name', 'sex', 'height', 'year']
[[1, 'xiaoming', 'male', 128, 23], [1, 'xiaohong', 'female', 162, 22], [2, 'xiaozhang', 'female', 163, 21], [2, 'xiaoli', 'male', 158, 21]]
'''