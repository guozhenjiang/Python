import time

print()
print('time.time():', time.time())
print('time.localtime():', time.localtime())
print('time.perf_counter():', time.perf_counter())
print('time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()):', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print()

'''

time.time(): 1587372960.6504586
time.localtime(): time.struct_time(tm_year=2020, tm_mon=4, tm_mday=20, tm_hour=16, tm_min=56, tm_sec=0, tm_wday=0, tm_yday=111, tm_isdst=0)
time.perf_counter(): 0.0211558
time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()): 2020-04-20 16:56:00

'''