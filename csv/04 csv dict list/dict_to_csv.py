import time
import csv

# 精确到毫秒的时间戳
def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

# 单个字典保存成多行 每行是 key, value
def dict_to_csv_01(data_dict, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        for key in data_dict.keys():
            f.write('%s, %s\n' %(key, data_dict[key]))

# 单个字典保存成一行 逐个排列 value
def dict_to_csv_02(data_dict, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, data_dict.keys())
        w.writeheader()
        w.writerow(data_dict)

# 多个字典组成的列表保存成多行 每行逐个排列 value
def dict_to_csv_03(data_dicts, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, data_dicts[0].keys())
        w.writeheader()
        w.writerows(data_dicts)
    
my_data_dict_1 = {'name':'郭振江', 'color':'yellow', 'age':20}

my_data_dict_2 = [{'name':'郭振江', 'color':'yellow', 'age':20},
                  {'name':'董晗', 'color':'red', 'age':18},
                  {'name':'小明', 'color':'green', 'age':3}]

print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
print('单级字典:\r\n', my_data_dict_1)
print('my_data_dict_1 keys:\r\n', my_data_dict_1.keys())
print()
print('字典列表:\r\n', my_data_dict_2)
print('my_data_dict_2 keys:\r\n', my_data_dict_2[0].keys())
print()

dict_to_csv_01(my_data_dict_1, './dict_to_csv_01 01.csv')
dict_to_csv_02(my_data_dict_1, './dict_to_csv_02 01.csv')
dict_to_csv_03(my_data_dict_2, './dict_to_csv_03 01.csv')

