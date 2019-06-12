import sql_filter
import base64
import pickle
import math

fw1 = open('data_maker/sql_오탐.txt', 'r', encoding='utf-8')
fw2 = open('data_maker/sql_정탐.txt', 'r', encoding='utf-8')


data_int = [[], []]  #data_int[0]: 각 데이터를 ast 로 만든 이후 리스트 하나로 뽑아낸 결과물, data_int[1]: sql injection 여부  0: sql injection 아님, 1: sql injection
max_len = 0

lines_1 = fw1.readlines()
for line in lines_1:          #sql injection이 아닌 것들에 대해서
    if line is not  '':
        line_split = (line.lower()).split()  #평문 -> lowercase + split() -> splitcheck -> parse -> sql_tree_maker -> tree_to_plain
    
        line_splitcheck = sql_filter.splitcheck(line_split) 
        line_parse = sql_filter.parse(line_splitcheck)
    
        line_tree = sql_filter.sql_tree_maker(line_parse)

        line_plain = []
        sql_filter.tree_to_plain(line_tree, line_plain)

        line_data_list = []
        for data in line_plain:
            b = data.encode("UTF-8")
            e = base64.b64encode(b)
            line_data_list.append(math.log(int.from_bytes(e,byteorder='big')))   # 재배치된 리스트의 각 워드를 base64로 해싱하고 그 값에 자연로그를 취한다

        if max_len < len(line_data_list):
            max_len = len(line_data_list)

        data_int[0].append(line_data_list)
        data_int[1].append(0)


lines_2 = fw2.readlines()
for line in lines_2:         #sql injection인 것들에 대해서
    if line is not  '':
        line_split = (line.lower()).split()  #평문 -> lowercase + split() -> splitcheck -> parse -> sql_tree_maker -> tree_to_plain
    
        line_splitcheck = sql_filter.splitcheck(line_split)
        line_parse = sql_filter.parse(line_splitcheck)
    
        line_tree = sql_filter.sql_tree_maker(line_parse)

        line_plain = []
        sql_filter.tree_to_plain(line_tree, line_plain)

        line_data_list = []
        for data in line_plain:
            b = data.encode("UTF-8")
            e = base64.b64encode(b)
            line_data_list.append(math.log(int.from_bytes(e,byteorder='big')))  # 재배치된 리스트의 각 워드를 base64로 해싱하고 그 값에 자연로그를 취한다

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
