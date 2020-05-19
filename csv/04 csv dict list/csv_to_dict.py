import time
import csv
import pandas as pd

# 精确到毫秒的时间戳
def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

# 
def csv_to_dict_01(file):
    df = pd.read_csv(file)      # DataFrame
    print(type(df))
    print(df)                   # <class 'pandas.core.frame.DataFrame'>
    
    dc = df.to_dict()
    print(type(dc))             # <class 'dict'>
    print(dc)
    
    keys = dc.keys()
    print(keys)
    data_dict_len = len(dc)
    
    print(data_dict_len)
    
    for i in range(data_dict_len):
        print()
        for k in keys:
            print(dc[k][i],'(', type(dc[k][i]), ')', end=' ')

print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
print()

csv_to_dict_01('./csv_to_dict 01.csv')
