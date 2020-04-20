import time

print()
# print('time.time():', time.time())
# print('time.localtime():', time.localtime())
# print('time.perf_counter():', time.perf_counter())
# print('time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


ct = time.time()
local_time = time.localtime(ct)
data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
data_secs = (ct - int(ct)) * 1000
time_stamp = "%s.%03d" % (data_head, data_secs)

print(time_stamp)

print()

'''
import time
def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - long(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp
'''