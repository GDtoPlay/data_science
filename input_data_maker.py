import sql_filter.py as sql_filter
import base64
import pickle

fw1 = open('data_maker/sql_오탐.txt', 'r')
fw2 = open('data_maker/sql_정탐.txt', 'r')


data_int = [[], []]
max_len = 0

lines_1 = fw1.readlines()
for line in lines_1:
    if line is not  '':
        line_split = line.split()
    
        line_splitcheck = sql_filter.splitcheck(line_split)
        line_parse = sql_filter.parse(line_splitcheck)
    
        line_tree = sql_filter.sql_tree_maker(line_parse)

        line_plain = []
        sql_filter.tree_to_plain(line_tree, line_plain)

        line_data_list = []
        for data in line_plain:
            b = data.encode("UTF-8")
            e = base64.b64encode(b)
            line_data_list.append(int.from_bytes(e,byteorder='big'))

        if max_len < len(line_data_list):
            max_len = len(line_data_list)

        data_int[0].append(line_data_list)
        data_int[1].append(0)


lines_2 = fw2.readlines()
for line in lines_2:
    if line is not  '':
        line_split = line.split()
    
        line_splitcheck = sql_filter.splitcheck(line_split)
        line_parse = sql_filter.parse(line_splitcheck)
    
        line_tree = sql_filter.sql_tree_maker(line_parse)

        line_plain = []
        sql_filter.tree_to_plain(line_tree, line_plain)

        line_data_list = []
        for data in line_plain:
            b = data.encode("UTF-8")
            e = base64.b64encode(b)
            line_data_list.append(int.from_bytes(e,byteorder='big'))

        if max_len < len(line_data_list):
            max_len = len(line_data_list)

        data_int[0].append(line_data_list)
        data_int[1].append(1)


for line_data_list in data_int[0]:
    while len(line_data_list) < max_len:
        line_data_list.append(0)
        
with open('data_int.txt', 'wb') as fr:
    pickle.dump(data_int, fr)

fw1.close()
fw2.close()
fr.close()
