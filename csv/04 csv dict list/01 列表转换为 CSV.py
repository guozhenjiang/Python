import csv

def list2csv(list, file):
    wr = csv.writer(open(file, 'w', newline='', encoding='utf-8'), quoting=csv.QUOTE_ALL)
    for word in list:
        wr.writerow([word])

record = ['one', 'two', 'three']

list2csv(record, './01.csv')