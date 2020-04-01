# 引用requests和json两个模块
# 网络请求的库
import requests
# we will need the json library to read the data passed back
# by the web service 
# json是一种轻量级的数据交换格式，该库包含了一些处理这种格式的函数
import json

# numpy与matplotlib需要的模块引用
import numpy as np 
from matplotlib import pyplot as plt 


vision_service_address = "https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=%E9%BB%91%E9%BE%99%E6%B1%9F&city=%E5%93%88%E5%B0%94%E6%BB%A8"

address = vision_service_address

# parameters = {"ret":0,"info":"","data":}

# response = requests.post(address)  # post请求是我们常说的提交表单，
                                     # 表单的数据内容就是post请求的参数，request实现post请求需设置请求参数data，
                                     # 数据格式可以为字典、元组、列表和json格式，不同数据格式有不同的优势。
response = requests.get(address)     # get的请求方式是在url上显示，但post的请求方式却隐藏在请求中。


# 判断是否返回异常  
response.raise_for_status()

# response模块的功能中的json功能返回一组json数据。该数据为字典类型的数据
results = response.json() 
print(type(results))                   # 返回的数据为字典类型

print('results')                       # 空行分隔符，方便观察
json_dumps_vslue = json.dumps(results) # json.dumps()函数是将字典转化为字符串
print(json_dumps_vslue)#
print(type(json_dumps_vslue))          # 观察返回的数据类型为字符串 

print()# 空行分隔，方便观察打印数据
print("data")
list1 = results["data"]
print(list1[0])
print()# 空行分隔，方便观察打印数据

# 创建x轴和y轴的列表 
x_list = [0]*len(list1)
y_list = [0]*len(list1)

n= 0
while n < len(list1):
    x_list[n] = list1[n]['date']
    y_list[n] = list1[n]['confirm']
    n = n+1



plt.title("Harbin ") 
plt.xlabel("date") 
plt.ylabel("confirm persons") 
# plt.plot(x_list,y_list,"ob")  # 散点图
plt.bar(x_list, y_list, color =  'r', align =  'center') # 柱状图
plt.show()


'''
import numpy as np 
from matplotlib import pyplot as plt 
x = np.arange(1,11) 
y =  2  * x +  5 
plt.title("Matplotlib donghan") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption") 
plt.plot(x,y) 
plt.show()
'''



'''
import urllib.request
import urllib.parse
 
url='https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=%E9%BB%91%E9%BE%99%E6%B1%9F&city=%E5%93%88%E5%B0%94%E6%BB%A8'  #调用的网址
# 设置header头跟post请求方式相同
# headers={"User-Agent": "Mozilla...."}
# req = urllib.request.Request(r'https://www.baidu.com/',headers=headers)
print("get请求")
web= urllib.request.urlopen(url)
print("二进制返回结果")
print(web)
print("解析后的结果")
f=web.read()

print(f)
'''