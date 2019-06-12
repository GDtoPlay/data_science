#-*- coding:utf-8 -*-

import json
import os
import msg_check
from collections import OrderedDict


dir_name ="json"

fnames = os.listdir(dir_name)

fnames1 = []
fnames2 = []

for frame in fnames:
    if '오탐' in frame: #IPS 장비가 판단한 것중 잘못 탐지한 것들
        fnames1.append(frame)

    elif '정탐' in frame: #IPS 장비가 판단한 것중 제대로 탐지 한 것들
        fnames2.append(frame)
        

sql_inject_key = ['sql', 'injection']
sql_inject_nkey = ['exploit']

# sql injection이 아닌 것들
sql_json_1 = open("sql_json_1.json", "w", encoding="utf-8") # sql injection이 아닌 것들은 sql_json_1.json에 저장된다
sql_json_1.write("[\n")
flag = 0
for fname in fnames1:
    jsonfile = open(dir_name+ '/' + fname, 'r', encoding="utf-8")
    json_data = json.load(jsonfile)

    file_data = OrderedDict()
    
    print("processing_1: " + fname)
    check =0
    for data in json_data:
        msg = data['MSG']
        if msg_check.msg_check(msg, sql_inject_key,sql_inject_nkey): #sql injection으로 탐지 하였는가? 오탐인데 sql injection으로 탐지 하였으면 sql injection이 아님
            if flag == 1 and check ==0:
                sql_json_1.write(",\n")
            if check !=0:
                sql_json_1.write(",\n")
            file_data["FILE"] = fname
            file_data["MSG"] = data["MSG"]
            file_data["RES"] = data["RES"]
            tmp = []
            for payload in data["PAYLOAD"]:
                tempdata = []
                for innerdata in payload["DATA"]:
                    tempdata.append(innerdata)
                tmp.append(tempdata)
            file_data["DATA"] = tmp
            json.dump(file_data, sql_json_1, indent=4)
            check +=1
            flag =1
    jsonfile.close()
    

for fname in fnames2:
    jsonfile = open(dir_name+ '/' + fname, 'r', encoding="utf-8")
    json_data = json.load(jsonfile)

    file_data = OrderedDict()
    
    print("processing_1: " + fname)
    check =0
    for data in json_data:
        msg = data['MSG']
        if not msg_check.msg_check(msg, sql_inject_key,sql_inject_nkey): #sql injection으로 탐지 하지 않았는가? 정탐인데 sql injection으로 탐지 하지 않았다면 sql injection이 아님
            if flag == 1 and check ==0:
                sql_json_1.write(",\n")
            if check !=0:
                sql_json_1.write(",\n")
            file_data["FILE"] = fname
            file_data["MSG"] = data["MSG"]
            file_data["RES"] = data["RES"]
            tmp = []
            for payload in data["PAYLOAD"]:
                tempdata = []
                for innerdata in payload["DATA"]:
                    tempdata.append(innerdata)
                tmp.append(tempdata)
            file_data["DATA"] = tmp
            json.dump(file_data, sql_json_1, indent=4)
            check +=1
            flag =1
    jsonfile.close()
    

sql_json_1.write("\n]")
sql_json_1.close()



# sql injection인 것들
sql_json_2 = open("sql_json_2.json", "w", encoding="utf-8") # sql injection인 것들은 sql_json_2.json에 저장된다
sql_json_2.write("[\n")
flag = 0
for fname in fnames2:
    jsonfile = open(dir_name+ '/' + fname, 'r', encoding="utf-8")
    json_data = json.load(jsonfile)

    file_data = OrderedDict()
    
    print("processing_2: " + fname)
    check =0
    for data in json_data:
        msg = data['MSG']
        if msg_check.msg_check(msg, sql_inject_key,sql_inject_nkey): #sql injection으로 탐지 하였는가? 정탐인데 sql injection으로 탐지 하였으면 sql injection임
            if flag == 1 and check ==0:
                sql_json_2.write(",\n")
            if check !=0:
                sql_json_2.write(",\n")
            file_data["FILE"] = fname
            file_data["MSG"] = data["MSG"]
            file_data["RES"] = data["RES"]
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

