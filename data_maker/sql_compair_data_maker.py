#-*- coding:utf-8 -*-

import json
import os
import msg_check
from collections import OrderedDict


dir_name1 ="json_raw_payload"
dir_name2 ="json"

fnames1 = os.listdir(dir_name1)
fnames2 = os.listdir(dir_name2)

sql_inject_key = ['sql', 'injection']
sql_inject_nkey = ['exploit']

# 분류 기준 미적용(대조군)
sql_json_1 = open("sql_json_1.json", "w", encoding="utf-8")
sql_json_1.write("[\n")
flag = 0
for fname in fnames1:
    jsonfile = open(dir_name1+ '/' + fname, 'r', encoding="utf-8")
    json_data = json.load(jsonfile)

    file_data = OrderedDict()
    
    print("processing_1: " + fname)
    check =0
    for data in json_data:
        msg = data['MSG']
        if msg_check.msg_simple_check(msg, 'sql'):
            if flag == 1 and check ==0:
                sql_json_1.write(",\n")
            if check !=0:
                sql_json_1.write(",\n")
            file_data["FILE"] = fname
            file_data["MSG"] = data["MSG"]
            file_data["RES"] = data["RES"]
            file_data["DATA"] = data["PAYLOAD"]
            json.dump(file_data, sql_json_1, indent=4)
            check +=1
            flag =1
    jsonfile.close()
sql_json_1.write("\n]")
sql_json_1.close()


# 분류 기준 적용
sql_json_2 = open("sql_json_2.json", "w", encoding="utf-8")
sql_json_2.write("[\n")
flag = 0
for fname in fnames2:
    jsonfile = open(dir_name2+ '/' + fname, 'r', encoding="utf-8")
    json_data = json.load(jsonfile)

    file_data = OrderedDict()
    
    print("processing_2: " + fname)
    check =0
    for data in json_data:
        msg = data['MSG']
        if msg_check.msg_check(msg, sql_inject_key,sql_inject_nkey):
            if flag == 1 and check ==0:
                sql_json_2.write(",\n")
            if check !=0:
                sql_json_2.write(",\n")
            file_data["FILE"] = fname
            file_data["MSG"] = data["MSG"]
            file_data["RES"] = data["RES"]
            file_data["RAW_PAYLOAD"] = data["RAW_PAYLOAD"]
            tmp = []
            for payload in data["PAYLOAD"]:
                tempdata = []
                for innerdata in payload["DATA"]:
                    tempdata.append(innerdata)
                tmp.append(tempdata)
            file_data["DATA"] = tmp
            json.dump(file_data, sql_json_2, indent=4)
            check +=1
            flag =1
    jsonfile.close()
sql_json_2.write("\n]")
sql_json_2.close()

