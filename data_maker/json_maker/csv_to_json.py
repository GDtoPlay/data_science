#-*- coding: utf-8 -*-
'''
필독 : 돌리기전에 csv파일 무조건 utf로 저장하기 하고 해야함
'''
import os
import csv
from funcs import *
import urllib.parse
import base64


dirname = "../utf8/"
#파일마다 열순서가 달라서 특정 문자가 몇번째 열에 있는지 구한다

time_index = index_dict("장비발생시간",dirname)
sip_index = index_dict("출발지IP",dirname)
sport_index = index_dict("출발지포트",dirname)
dip_index = index_dict('목적지IP',dirname)
dport_index = index_dict("목적지포트",dirname)
msg_index = index_dict('공격명',dirname)
payload_index = index_dict('페이로드',dirname)
proto_index = index_dict("프로토콜",dirname)
res_index={}
res_index.update(index_dict('정오탐',dirname))
res_index.update(index_dict('결과',dirname))


filenames = search(dirname)			
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass

for file in filenames:
	csvtojson = open('../json/' + file[:-4] + '.json', 'w', encoding="utf-8")
	csvtojson.write("[\n")
	f = open(dirname+file,'r',encoding='utf-8') 
	rdr = csv.reader(f)
	print("processing : " + file)
	check = 0							#엑셀 첫행 체크용 변수 
	for row in rdr:
		file_data={}
		try:
			if check==0:	#엑셀 첫행 건너뛰기
				check+=1
				continue

			if check!=1:	#엑셀 첫행 건너뛰기
				check+=1
				csvtojson.write(",\n")
			csvtojson.write("{")
			csvtojson.write('\n\t"TIME": '+'"'+row[time_index[file]]+'",' )	#"TIME": "2018-12-08 5:01"
			csvtojson.write('\n\t"SIP": '+'"'+row[sip_index[file]]+'",' )
			csvtojson.write('\n\t"SPORT": '+'"'+row[sport_index[file]]+'",' )
			csvtojson.write('\n\t"DIP": '+'"'+row[dip_index[file]]+'",' )
			csvtojson.write('\n\t"DPORT": '+'"'+row[dport_index[file]]+'",' )
			csvtojson.write('\n\t"MSG": '+'"'+row[msg_index[file]]+'",' )
			csvtojson.write('\n\t"RES": '+'"'+row[res_index[file]]+'",' )


			raw_payload = row[payload_index[file]]

			while '\r' in raw_payload or '\n' in raw_payload:
				raw_payload = raw_payload.replace('\r', '')
				raw_payload = raw_payload.replace('\n', '')

			base64_raw_payload = base64.b64encode(raw_payload.encode('utf-8'))
			

			
			csvtojson.write('\n\t"PAYLOAD":' +'[')
			
			payload_json_bunch = pay2json( row[payload_index[file]]  ,file )
			
			csvtojson.write(payload_json_bunch)	

			csvtojson.write(']')
			csvtojson.write("\n}")
			check +=1
			
			
		except IndexError:			#공백 열이 있을 시
			pass

	f.close()
	csvtojson.write("\n]")
	csvtojson.close()
