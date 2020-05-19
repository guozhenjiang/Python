import csv
import time

# 精确到毫秒的时间戳
def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

# 这种方法不合适 得到的始终是字符串
def list_to_csv_01(data_list, file):
    wr = csv.writer(open(file, 'w', newline='', encoding='utf-8'), quoting=csv.QUOTE_ALL)
    for word in data_list:
        wr.writerow([word])

# 适用于一维列表 unidimensional
def list_to_csv_02(data_list, file):
    wr = csv.writer(open(file, 'w', newline='', encoding='utf-8'), quoting=csv.QUOTE_ALL)
    wr.writerow(data_list)

# 适用于二维列表 planar
def list_to_csv_03(data_list, file):
    wr = csv.writer(open(file, 'w', newline='', encoding='utf-8'), quoting=csv.QUOTE_ALL)
    wr.writerows(data_list)

my_data_list_1 = ['one', 'two', 'three']
my_data_list_2 = [['one', 'two', 'three'], [1, 2, 3]]

print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
print('一维列表:\r\n', my_data_list_1)
print('二维列表:\r\n', my_data_list_2)

list_to_csv_01(my_data_list_1, './list_to_csv_01 01.csv')
list_to_csv_01(my_data_list_2, './list_to_csv_01 02.csv')

list_to_csv_02(my_data_list_1, './list_to_csv_02 01.csv')
list_to_csv_02(my_data_list_2, './list_to_csv_02 02.csv')

list_to_csv_03(my_data_list_1, './list_to_csv_03 01.csv')
list_to_csv_03(my_data_list_2, './list_to_csv_03 02.csv')

