# Hello World
# print("hello world")

# 输入
# name = input('please enter your name\r\n')
# print()
# print(name)
# print()

# 错误提示
# x = 532 + 12
# y = x / 0     # 这里会报错 同样不能除 0
# print("running?")

# pi = 3.14159
# print(pi)

# 时间（日期）
# from datetime import datetime
# current_data = datetime.now()
# print('Day: ' + str(current_data.day))
# print('Month ' + str(current_data.month))
# print('Year: ' + str(current_data.year))

# # 时间（日期）的自动转换
# from datetime import datetime, timedelta
# birthday = input("When is your birthday(dd/mm/yyyy)")
# birthdat_date = datetime.strptime(birthday, '%d%m%Y')
# print('Birthday: ' + str(birthdat_date))
# one_day = timedelta(days = 1)
# birthday_eve = birthdat_date - one_day
# print('Day before birthday: ' + str(birthday_eve))

# 算算你出生多少天了
# from datetime import datetime, timedelta
# birthday = input("When is your birthday(dd/mm/yyyy)\n")
# birthdat_date = datetime.strptime(birthday, '%d%m%Y')
# current_date = datetime.now()
# days = current_date - birthdat_date
# print("您已存活" + str(days) + "天")

# 异常处理
# x = 42
# y = 0
# print()
# try:
#     print(x / y)
# except ZeroDivisionError as e:
#     print('Not allowed to divide by zero')
# else:
#     print('Something else went wrong')
# finally:
#     print('This is our cleanup code')
# print()

# P19 if 条件语句 > < >= <= == !=

# P20 条件语句实例
# price = input('how much did you pay\n')
# price = float(price)
# if(price >= 1.00):
#     tax = .07
# else:
#     tax = 0
# print('Tax rate is: ' + str(tax))

# country = input('Enter the name of your country\n')
# if country.lower() == 'canada':
#     print('So you must like hockey!')
# else:
#     print('You are not form Canada')


#P21 elif 和 in
# country = input('What country do you live in?\n')
# province = input('What province do you live in\n')
# tax = 0
# if country.lower() == 'canada':
#     if province == 'Alberta':
#         tax = 0.05
#     elif province == 'Nunavut':
#         tax = 0.05
#     elif province == 'Ontario':
#         tax = 0.13
#     else:
#         tax = 0.15

#     if province == 'Alberta'\
#         or province == 'Nunavut':
#         tax = 0.05
#     elif province == 'Ontario':
#         tax = 0.13
#     else:
#         tax = 0.15

#     if province in('Alberta', 'Nunavut', 'Yukon'):
#         tax = 0.05
#     elif province == 'Ontario':
#         tax = 0.13
#     else:
#         tax = 0.15
# else:
#     tax = 0
# print(tax)

#P24 and 和 布尔标记
# A student makes honour roll if their average is  >=85
# and their lowest grade is not blow 75
# gpa = float(input('What was your Grade Point Average?'))
# lowest_grade = float(input('What was your lowest grade?\n'))

# if gpa >= 0.85:
#     if lowest_grade >= 0.70:
#         print('You made the honour roll')

# 测试数据类型
a = 100
print(type(a))

# eval()        # 将字符串类型转换为数值类型