import csv

# my_list = [	{'姓名':'Khazri',	'编号':'989', 	'生日':'08/02/1991',	'团队':'Bordeaux'},
# 			{'姓名':'Lewis', 	'编号':'989', 	'生日':'08/02/1991',	'团队':'Sunderland'},
# 			{'姓名':'Baker', 	'编号':'9574',	'生日':'25/04/1995',	'团队':'Vitesse'}	]

# # write nested list of dict to csv
# def nestedlist2csv(list, out_file):
#     with open(out_file, 'w', newline='', encoding='utf-8') as f:
#         w = csv.writer(f)
#         fieldnames=list[0].keys()  # solve the problem to automatically write the header
#         w.writerow(fieldnames)
#         for row in list:
#             w.writerow(row.values())

# nestedlist2csv(my_list, './03.csv')

# convert csv file to dict
# @params:
# key/value: the column of original csv file to set as the key and value of dict
def csv2dict(in_file, key, value):
    new_dict = {}
    with open(in_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        fieldnames = next(reader)
        reader = csv.DictReader(f, fieldnames=fieldnames, delimiter=',')
        for row in reader:
            new_dict[row[key]] = row[value]
    return new_dict

dict_04 = csv2dict('./04.csv', '姓名', 3)

print(dict_04)