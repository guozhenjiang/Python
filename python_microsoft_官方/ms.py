# https://www.bilibili.com/video/av73007133

# --------------------------------------------------
# P25 列表 数组 字典
# --------------------------------------------------

# ----- Lists are collections of items
# names = ['Christopher', 'Susan']
# print(names)

# ----- You can start with an empty list
# scores = []
# scores.append(98)   # Add new item to the end
# scores.append(99)
# print(scores)
# print(scores[1])    # Collections are zero-indexed

# ----- Arrays are also collection of items
# from array import array
# scores = array('d')
# scores.append(97)
# scores.append(98)
# print(scores)
# print(scores[1])

# ----- What's the difference(beetween Arrays and Lists)
# 数组的元素必须类型相同 列表则可以多种类型混合

# ----- Common operations
# names = ['Susan', 'Christopher']
# print (len(names))      # Get the num of items
# names.insert(0, 'Bill') # Insert before index
# print(names)
# names.sort()
# print(names)

# # ----- Retrieving ranges
# names = ['Susan', 'Christopher', 'Bill']
# presenters = names[0:2] # Get the first two items
# # Starting index and num of items to retrieve

# print(names)
# print(presenters)

# ----- Dictionaries
# person = {'first':'Christopher'}
# person['last'] = 'Harrison'
# print(person)
# print(person['first'])

# --------------------------------------------------
# P26 实操 列表、数组、字典
# --------------------------------------------------

# Ctrl + D 多选相同名称的词同时修改

# -----
# christopher = {}
# christopher['first'] = 'Christopher'
# christopher['last'] = 'Harrison'
# susan = {'first':'Susan', 'last':'Ibach'}

# # print(christopher)
# # print(susan)

# people = [christopher, susan]
# people.append({'first':'Bill', 'last':'Gates'})
# presenters = people[0:2]
# print(people)
# print()
# print(presenters)
# print()

# --------------------------------------------------
# P27 循环
# --------------------------------------------------

# ----- Loop though a collection
# for name in ['Christopher', 'Susan']:
#     print(name)

# ----- Looping a number of times
# for index in range(0, 2):
#     print(index)

# ----- Looping whit a condition
# names = ['Christopher', 'Susan']
# index = 0
# while index < len(names):
#     print(names[index])
#     # Change the condition!!
#     index = index + 1

# --------------------------------------------------
# P28 实操 for 和 while 循环
# --------------------------------------------------

# -----
# people = ['Christopher', 'Susan']

# # for name in people:
# #     print(name)

# index = 0
# while index < len(people):
#     print(people[index])
#     index = index + 1
    
# print()

# --------------------------------------------------
# P29 函数
# --------------------------------------------------

# ----- Sometimes we copy and paste our code
# import datetime
# #print timestamps to see how long sections
# #take to run

# first_name = 'Susan'
# print('task completed')
# print(datetime.datetime.now())
# print()

# for x in range(0, 10):
#     print(x)
# print('task completed')
# print(datetime.datetime.now())
# print()

# ----- Use functions instead of repeating code
# import datetime
# # Print the current time
# def print_time():
#     print('task completed')
#     print(datetime.datetime.now())
#     print()

# first_nam = 'Susan'
# print_time()

# for x in range(0, 10):
#     print(x)
# print_time()

# ----- By moving the code to a function, you reduce
# ----- rework and the chance of introducing bugs
# ----- when you change the code you had copied
# #Import the datetime class from datetime library
# from datetime import datetime
# # Print the current time
# def print_time():
#     print('task completed')
#     # Now I don't need the extra datetime prefix
#     print(datetime.now())
#     print()

# print_time()

# ----- What if I want a different message displayed?
# from datetime import datetime
# # print timestamps to see how long section of code
# # take to run

# first_name = 'Susan'
# print('first name assigned')
# print(datetime.now())
# print()

# for x in range(0, 10):
#     print(x)

# print('loop completed')
# print(datetime.now())
# print()

# ----- Pass the task name as a parameter
# from datetime import datetime

# # Print the current time and task name
# def print_time(task_name):
#     print(task_name)
#     print(datetime.now())
#     print()

# first_name = 'Susan'
# print_time('first name assigned')

# for x in range(0, 10):
#     print(x)
# print_time('loop completed')

# ----- Here's another example where the code looks
# ----- different but we are doing the same logic over
# ----- and over
# first_name = input('Enter you first name:\n')
# first_name_initial = first_name[0:1]
# last_name = input('Enter your last name:\n')
# last_name_initial = last_name[0:1]

# print('Your initials are:' + first_name_initial\
#         + last_name_initial)

# ----- I can still use a function, but this time my
# ----- function returns a value
# def get_initial(name):
#     initial = name[0:1]
#     return initial

# first_name = input('Enter your first name:\n')
# first_name_initial = get_initial(first_name)

# last_name = input('Enter your last name:\n')
# last_name_initial = get_initial(last_name)

# print('Your initials are: ' + first_name_initial \
#         + last_name_initial)

# ----- If you need to change something you only
# ----- have to change it in one place
# def get_initial(name):
#     initial = name[0:1].upper()
#     return initial

# first_name = input('Enter your first name:\n')
# first_name_initial = get_initial(first_name)

# last_name = input('Enter your last name:\n')
# last_name_initial = get_initial(last_name)

# print('Your initials are: ' \
#         + first_name_initial \
#         + last_name_initial)

# --------------------------------------------------
# P30 实操函数
# --------------------------------------------------

# ----- 代码和前一节重复

# --------------------------------------------------
# P31 函数参数
# --------------------------------------------------

# --------------------------------------------------
# P32 实操函数参数
# --------------------------------------------------
# ----- 单一参数
# # This function will take a name and return the
# # first letter of the name
# def get_initial(name):
#     initial = name[0:1].upper()
#     return initial

# # Ask for someone's name and return the initials
# first_name = input('Entern your first name:\n')
# first_name_initial = get_initial(first_name)

# print('Your initial is ' + first_name_initial)

# ----- 多个参数 根据不同参数执行不同功能
# # This function will take a name and return the
# # first letter of the name
# def get_initial(name, force_uppercase):
#     if force_uppercase:
#         initial = name[0:1].upper()
#     else:
#         initial = name[0:1]
#     return initial

# # Ask for someone's name and return the initials
# first_name = input('Entern your first name:\n')
# first_name_initial = get_initial(first_name, False)

# print('Your initial is ' + first_name_initial)

# ----- 设置了默认值的参数可以再调用时不填写该参数
# # This function will take a name and return the
# # first letter of the name
# def get_initial(name, force_uppercase=True):
#     if force_uppercase:
#         initial = name[0:1].upper()
#     else:
#         initial = name[0:1]
#     return initial

# # Ask for someone's name and return the initials
# first_name = input('Entern your first name:\n')
# first_name_initial = get_initial(first_name)

# print('Your initial is ' + first_name_initial)

# ----- 显示传参 可以调换参数位置
# # This function will take a name and return the
# # first letter of the name
# def get_initial(name, force_uppercase=True):
#     if force_uppercase:
#         initial = name[0:1].upper()
#     else:
#         initial = name[0:1]
#     return initial

# # Ask for someone's name and return the initials
# first_name = input('Entern your first name:\n')
# first_name_initial = get_initial(force_uppercase=False, name=first_name)

# print('Your initial is ' + first_name_initial)

# --------------------------------------------------
# P33 模块和包
# --------------------------------------------------

# ----- Creating module
# # helpers.py
# def display(message, is_warning=False):
#     if is_warning:
#         print('Warning!!')
#     print(message)

# ----- Importing a module
# # import module as namespace
# import helpers  # helpers 就是一个 namespace
# helpers.display('Not a warning')

# # import all into current namespace
# from helpers import *
# display('Not a warning')

# #inport specific items into current namespace
# from helpers import display
# display('Not a warning')

# ----- Installing packages
# # Install an individual package
# pip install colorama

# # Install from a list of packages
# pip install -r requirements.txt

# # requirements.txt
# colorama

# ----- Python pip 安装与使用
# https://www.runoob.com/w3cnote/python-pip-install-usage.html
# pip --version     # 检测是否已经安装 pip

# 如果未安装 使用如下方法安装（注意必须是管理员模式）
# $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py   # 下载安装脚本
# $ sudo python get-pip.py          # 运行安装脚本

# pip install -U pip                # 升级 pip
# sudo easy_install --upgrade pip   # 升级 pip

# pip install SomePackage           # 最新版本
# pip install SomePackage==1.0.4    # 指定版本
# pip install 'SomePackage>=1.0.4'  # 最小版本

# pip install --upgrade SomePackage # 升级包
# pip uninstall SomePackage         # 卸载包
# pip search SomePackage            # 搜索包
# pip show                          # 显示安装包信息
# pip show -f SomePackage           # 查看指定包信息
# pip list                          # 列出已经安装的包
# pip list -o                       # 查看可升级的包

# --------------------------------------------------
# P34 虚拟环境
# --------------------------------------------------

# ----- Creating a virtual environments
# # Install virtual environment
# pip install virtualenv

# # Windows systems
# python -m venv <folder_name>

# # OSX/Linux(bash)
# virtualenv <folder_name>

# --------------------------------------------------
# P35 实操自定义模块、包、虚拟环境
# --------------------------------------------------

# # -----
# import helpers
# helpers.display('Sample message', True)
# print()

# from helpers import display
# display('Sample message')

# # ----- 查看文件策略
# # Get-ExecutionPolicy -List
# # ----- 修改文件策略
# # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# # ----- 进入虚拟环境
# # .\venv\Scripts\Activate.ps1
# # ----- 退出虚拟环境
# # deactivate
# # ----- pip install -r .\requirements.txt
# # ----- python -m pip install --upgrade pip

# --------------------------------------------------
# P36 调用 API
# --------------------------------------------------

# ----- What is a web service?
# ----- Keys allow me to track which user have
#       permission to use my web service
# ----- There is a standard for sending messages
#       across the web

# -----
# GET:
#     Pass values in query string only
#         Special characters must be "escaped"
#         Limited amount of data

# POST:
#     Pass values in query string and body
#         No need to escape special characters if passed in body
#         Can pass large amounts of data, include images,in body

# ----- The requests library simplifies HTTP calls fromm
#       Python code

# --------------------------------------------------
# P37 实操 API
# --------------------------------------------------

# --------------------------------------------------
# P38 JSON 的三种结构
# --------------------------------------------------

# ----- Many web services return data as JSON

# ----- Using a linting tool to format JSON makes it
# ----- easier to read

# ----- JSON contains key pairs

# ----- To retrieve the value from a "key":"value"
# ----- request the key name

# ----- To request a value from a ...

# ----- You can create "key":"value" JSON objects from
# ----- a dictionary
# # Create a dictionary object
# person_dict = {'first':'Christopher', 'last':'Harrison'}
# # Add additional key pairs as needed to dictionary
# person_dict['City'] = 'Seattle'

# # Convert dictionary to JSON object
# person_json = json.dumps(person_dict)
# print(person_json)

# ----- 创建含有子键值对的 JSON
# person_dict = {'first':'Christopher', 'last':'Harrison'}

# # Creat staff dictionary which assigns a person to a role
# staff_dict = {}
# staff_dict['Program Manager'] = person_dict

# # Convert dictionary to JSON object
# staff_json = json.dumps(staff_dict)

# # Print JSON object
# print(staff_json)

# ----- 将列表添加到 JSON
# person_dict = {'first':'Christopher', 'last':'Harrison'}

# # Create a list ofject of programming languages
# languages_list = ['CSharp', 'Python', 'JavaScript']
# # Add list to dictionary
# person_dict['languages'] = languages_list

# # Convert dictionary to JSON object
# person_json = json.dumps(person_dict)
# print(person_json)

# ----- JSON Linter

# --------------------------------------------------
# P39 实操 JSON
# --------------------------------------------------

# ----- 字典转换成 JSON 键值对
# import json

# # Create a dictionary object
# preson_dict = {'first':'Christopher', 'last':'Harrison'}
# # Add additional key pairs to dictionary as needed
# preson_dict['City'] = 'Seattle'

# # Convert dictionary to JSON object
# person_json = json.dumps(preson_dict)

# # Print JSON object
# print(person_json)

# ----- 字典嵌套形成的子键值对
# import json

# # Create a dictionary object
# preson_dict = {'first':'Christopher', 'last':'Harrison'}
# # Add additional key pairs to dictionary as needed
# preson_dict['City'] = 'Seattle'

# # create a staff dictionary
# # assign a person to a staff position of program manager
# staff_dict = {}
# staff_dict['Program Manager'] = preson_dict
# # Convert dictionary to JSON object
# person_json = json.dumps(staff_dict)

# # Print JSON object
# print(person_json)

# ----- 将 JSON 存入列表中
# import json

# # Create a dictionary object
# preson_dict = {'first':'Christopher', 'last':'Harrison'}
# # Add additional key pairs to dictionary as needed
# preson_dict['City'] = 'Seattle'

# # Create a list object of programing language
# language_list = ['CSharp', 'Python', 'JavaScript']

# # Add list object to dictionary for the languages key
# preson_dict['language'] = language_list

# # Convert dictionary to JSON object
# person_json = json.dumps(preson_dict)

# # Print JSON object
# print(person_json)

# --------------------------------------------------
# P40 环境变量
# --------------------------------------------------

# ----- Reading an environmental variable
# import os
# os_version = os.getenv('OS')
# print(os_version)

# ----- Using dotenv
# # .env file
# DATABASE = Sample_Connection_String

# # app.py
# from dotenv impot load_dotenv
# import os
# load_dotenv()
# database = os.getenv('DATABASE')
# print(database)

# --------------------------------------------------
# P41 实操环境变量
# --------------------------------------------------

# ----- .\venv\Scripts\Activate.ps1
# ----- requirements.txt    python-dotenv
# ----- pip install -r .\requirements.txt
# ----- create .env file
# from dotenv import load_dotenv
# load_dotenv()
# import os
# password = os.getenv('PASSWORD')

# print(password)

# --------------------------------------------------
# P42 装饰器 Decorator
# --------------------------------------------------

# ----- 

# --------------------------------------------------
# P43 实操装饰器
# --------------------------------------------------

# ----- 
def logger(func):
    def wrapper():
        print('Logging execution')
        func()
        print('Done logging')
    return wrapper

@logger # 设置名称为 logger 的装饰器
def sample():
    print('--Inside sample function')

sample()