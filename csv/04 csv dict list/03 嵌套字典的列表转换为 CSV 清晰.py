import csv

my_list = [	{'姓名':'Khazri',	'编号':'989', 	'生日':'08/02/1991',	'团队':'Bordeaux'},
			{'姓名':'Lewis', 	'编号':'989', 	'生日':'08/02/1991',	'团队':'Sunderland'},
			{'姓名':'Baker', 	'编号':'9574',	'生日':'25/04/1995',	'团队':'Vitesse'}	]

# write nested list of dict to csv
def nestedlist2csv(list, out_file):
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        fieldnames=list[0].keys()  # solve the problem to automatically write the header
        w.writerow(fieldnames)
        for row in list:
            w.writerow(row.values())

nestedlist2csv(my_list, './03.csv')