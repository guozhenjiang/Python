
prime_id = 0;                               # 序号 出现的第几个质数

for i in range(2, 1000):                    # 1 不是质数 从 2 开始
    is_prime = True;
    
    for j in range(1, i):
        if((j != 1) and (j != i)):
            if(0 == i%j):                   # 如果该数能被 1 和 自身 以外的其他数整除
                is_prime = False            # 则该数不是质数
                break                       # 提高效率
                
    if(True == is_prime):                   # 如果当前数是质数
        prime_id += 1
        print(str(prime_id) + ':' + str(i)) # 打印出该数据(同时打印出这是第几个质数)

