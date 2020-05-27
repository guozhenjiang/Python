import time

def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

a = '[(0, 0), (200, 0), (0, 200)]'

# b = list(a)
b = eval(a)

print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
print('b 的类型', type(b))
print('b 的长度', len(b))
print('b 的内容:\r\n', b)
print('b 第一项的类型', type(b[0]))
print('b 第一项的内容:\r\n', b[0])

print('b 每一项的内容:\r\n')
for i in b:
    print(i)
    # for j in i:
    #     print(j)

print()
print(b[1][0])