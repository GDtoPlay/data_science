
import base64
import pickle
import math

fw1 = open('data_maker/sql_special_오탐.txt', 'r', encoding='utf-8')
fw2 = open('data_maker/sql_special_정탐.txt', 'r', encoding='utf-8')


data_int = [[], []]
max_len = 0

lines_1 = fw1.readlines()
for line in lines_1:
    if line is not  '':

        line_data_list = []
        
        b = line.encode("UTF-8")
        e = base64.b64encode(b)
        line_data_list.append(math.log(int.from_bytes(e,byteorder='big')))

        if max_len < len(line_data_list):
            max_len = len(line_data_list)

        data_int[0].append(line_data_list)
        data_int[1].append(0)


lines_2 = fw2.readlines()
for line in lines_2:
    if line is not  '':

        line_data_list = []
        
        b = line.encode("UTF-8")
        e = base64.b64encode(b)
        line_data_list.append(math.log(int.from_bytes(e,byteorder='big')))

        if max_len < len(line_data_list):
            max_len = len(line_data_list)

        data_int[0].append(line_data_list)
        data_int[1].append(1)


for line_data_list in data_int[0]:
    while len(line_data_list) < max_len:
        line_data_list.append(0)
        
with open('data_int_special.txt', 'wb') as fr:
    pickle.dump(data_int, fr)

fw1.close()
fw2.close()
fr.close()
