import time

def time_stamp_ms():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    stamp_ms_str = "%s.%03d" % (data_head, data_secs)
    
    return stamp_ms_str

print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
with open('./map/2d_room_hw.txt', encoding='utf-8') as f:
    t = f.read()

print('读取的内容类型: ', type(t))
print('读取的内容:\r\n', t)

# print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
# t = t.replace(' ', '')
# t = t.replace('\t', '')
# print('去掉所有空格、制表位:\r\n', t)

# print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
# t = t.replace('\r', '')
# t = t.replace('\n', '')
# print('去掉所换行:\r\n', t)

'1 + 1'

print('\r\n____________________ %s ____________________' %(time_stamp_ms()))
e = eval(t)
print('对应的 eval 表达式 类型: ', type(e))
print('对应的 eval 表达式 内容:\r\n', e)
print('对应的 eval 表达式 长度: ', len(e))
print('对应的 eval 表达式 关键字: ', e.keys())
print('对应的 eval 表达式 中有:')
for k in e.keys():
    print('\t', len(e[k]), '个', k, '(类型 ', type(e[k]), ')')
    
if 'type' in e:
    print(e['type'])
    print(type(e['type']))