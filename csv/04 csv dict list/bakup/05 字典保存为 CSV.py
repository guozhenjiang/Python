# https://stackoverflow.com/questions/3086973/how-do-i-convert-this-list-of-dictionaries-to-a-csv-file

import csv

toCSV = [{'name':'bob','age':25,'weight':200},
         {'name':'jim','age':31,'weight':180}]

keys = toCSV[0].keys()

with open('05.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(toCSV)