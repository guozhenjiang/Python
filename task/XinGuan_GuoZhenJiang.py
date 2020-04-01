import requests     # pip install requests
import json
import numpy as np 
from matplotlib import pyplot as plt 

response = requests.get("https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=陕西&city=咸阳")
print(type(response))                   # <class 'requests.models.Response'>

response.raise_for_status()             # 判断是否返回异常

results = response.json()               # response 返回字典类型的数据
print(type(results))                    # <class 'dict'>

print('response.json:')
json_dumps_vslue = json.dumps(results)  # json.dumps()函数是将字典转化为字符串
print(type(json_dumps_vslue))           # <class 'str'> 

print(json_dumps_vslue)

print()
print("data")
list1 = results["data"]
print(list1[0])
print()

# 创建 x 轴和 y 轴的列表 
x_list = [0]*len(list1)
y_list = [0]*len(list1)

n= 0
while n < len(list1):
    x_list[n] = list1[n]['date']
    y_list[n] = list1[n]['confirm']
    n = n+1

plt.title("XianYang") 
plt.xlabel("date") 
plt.ylabel("confirm persons") 

# plt.plot(x_list,y_list,"ob")                              # 散点图
plt.bar(x_list, y_list, color =  'r', align =  'center')    # 柱状图
plt.show()