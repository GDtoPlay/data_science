# -*- coding:utf-8 -*-

import json
import base64
from string import ascii_lowercase, ascii_uppercase

with open('sql_json_special1.json') as sql_injection_json_1:

    json_data_1 = json.load(sql_injection_json_1)


with open('sql_json_special2.json') as sql_injection_json_2:

    json_data_2 = json.load(sql_injection_json_2)


            
def sql_str_maker(file, json_data):
    for sql_json in json_data:
        if "DATA" in sql_json:
            sql_data = sql_json["DATA"]
            

            if sql_data is not '':
                file.write(sql_data + '\n')

fw1 = open('sql_special_오탐.txt', 'w', encoding='utf8')
fw2 = open('sql_special_정탐.txt', 'w', encoding='utf8')

sql_str_maker(fw1, json_data_1)
sql_str_maker(fw2, json_data_2)

fw1.close()
fw2.close()


            
