#-*- coding: utf-8 -*-
'''
main.py와 호환성있게짤려고 했는데 우선 logadmin2019만파싱만 짜는걸로...
합치는건나중에.. 뭐가자꾸안됨
'''
import os
import csv
from funcs import *
import urllib.parse
import base64


word =[  # SQL
	['case', 'A', 0], ['by', 'A', 0], ['all', 'A', 0], ['char', 'A', 0], ['character', 'A', 0],
	['chr', 'B', 0], ['column', 'B', 0], ['concat', 'B', 0], ['convert', 'B', 0], ['count', 'B', 0],
	['create', 'C', 0], ['declare', 'C', 0], ['delete', 'C', 0], ['distinct', 'C', 0], ['drop', 'C', 0],
	['from', 'D', 0], ['function', 'D', 0], ['group', 'D', 0], ['having', 'D', 0], ['if', 'D', 0],
	['ifnull', 'E', 0], ['insert', 'E', 0], ['into', 'E', 0], ['like', 'E', 0], ['limit', 'E', 0],
	['or', 'F', 0], ['and', 'F', 0], ['order', 'F', 0], ['select', 'F', 0], ['union', 'F', 0],
	['update', 'G', 0], ['when', 'G', 0], ['where', 'G', 0], ['grant', 'G', 0],
	#######################
	['address', 'H', 0], ['data', 'H', 0], ['database', 'H', 0], ['dba', 'H', 0], ['etc', 'H', 0],
	['file', 'I', 0], ['filename', 'I', 0], ['id', 'I', 0], ['name', 'I', 0], ['passwd', 'I', 0],
	['password', 'J', 0], ['pg', 'J', 0], ['pwd', 'J', 0], ['resource', 'J', 0], ['sys', 'J', 0],
	['system', 'K', 0], ['table', 'K', 0], ['tablename', 'K', 0], ['tables', 'K', 0], ['uid', 'K', 0],
	['user', 'L', 0], ['username', 'L', 0], ['users', 'L', 0], ['utl', 'L', 0], ['value', 'L', 0],
	['values', 'M', 0], ['version', 'M', 0], ['schema', 'M', 0], ['information', 'M', 0],
	['inaddr', 'M', 0],
	['admin', 'M', 0],
	#############################
	['cmd', 'N', 0], ['cmdshell', 'N', 0], ['echo', 'N', 0], ['exe', 'N', 0], ['exec', 'N', 0],
	['shell', 'O', 0], ['master', 'O', 0], ['xp', 'O', 0], ['sp', 'O', 0], ['regdelete', 'O', 0],
	['availablemedia', 'P', 0], ['terminate', 'P', 0], ['regwrite', 'P', 0],
	['regremovemultistring', 'P', 0],
	['regread', 'Q', 0], ['regenumvalues', 'Q', 0], ['regenumkeys', 'Q', 0], ['regenumbalues', 'Q', 0],
	['regdeletevalue', 'R', 0], ['regdeletekey', 'R', 0], ['regaddmultistring', 'R', 0], ['ntsec', 'R', 0],
	['makecab', 'S', 0], ['loginconfig', 'S', 0], ['enumdsn', 'S', 0], ['filelist', 'S', 0],
	['execresultset', 'T', 0], ['dirtree', 'T', 0], ['cmdshell', 'T', 0], ['reg', 'T', 0],
	['servicecontrol', 'U', 0], ['webserver', 'U', 0],
	############################
	['decode', 'V', 0], ['default', 'V', 0], ['delay', 'V', 0], ['document', 'V', 0], ['eval', 'V', 0],
	['getmappingxpath', 'W', 0], ['hex', 'W', 0], ['is', 'W', 0], ['login', 'W', 0], ['match', 'W', 0],
	['not', 'X', 0], ['null', 'X', 0], ['request', 'X', 0], ['sets', 'X', 0], ['to', 'X', 0],
	['var', 'Y', 0], ['varchar', 'Y', 0], ['waitfor', 'Y', 0], ['desc', 'Y', 0], ['connect', 'Y', 0],
	['as', 'Z', 0], ['int', 'Z', 0], ['log', 'Z', 0], ['cast', 'Z', 0], ['rand', 'Z', 0], ['sleep', 'Z', 0],
	['substring', 'a', 0], ['replace', 'a', 0], ['benchmark', 'a', 0], ['md', 'a', 0],
	#######################
	['content', 'b', 0], ['cookie', 'b', 0], ['dbms', 'b', 0], ['db', 'b', 0], ['dir', 'b', 0],
	['get', 'c', 0], ['http', 'c', 0], ['mysql', 'c', 0], ['oracle', 'c', 0], ['post', 'c', 0],
	['query', 'd', 0], ['referer', 'd', 0], ['sql', 'd', 0], ['sqlmap', 'd', 0]
]


dirname = "../LOG/"

#파일마다 열순서가 달라서 특정 문자가 몇번째 열에 있는지 구한다

time_index = index_dict("장비발생시간",dirname)
sip_index = index_dict("출발지IP",dirname)
sport_index = index_dict("출발지포트",dirname)
dip_index = index_dict('목적지IP',dirname)
dport_index = index_dict("목적지포트",dirname)
msg_index = index_dict('공격명',dirname)
payload_index = index_dict('페이로드',dirname)
rawdata_index = index_dict('raw_data',dirname)	#LOGADMIN 2019호환용
request_index = index_dict('request',dirname)	#LOGADMIN 2019호환용
proto_index = index_dict("프로토콜",dirname)
res_index={}
res_index.update(index_dict('정오탐',dirname))
res_index.update(index_dict('결과',dirname))


filenames = search(dirname)			
try:	filenames.remove("desktop.ini") #desktop.ini 잇으면 삭제 없으면 패스
except:	pass


for file in filenames:
	if "csv" not in file:
		continue
	if "오탐" in file:
		res = "0"
	else:
		res = "1"
	csvtojson = open('../special/' + file[:-4] + '.json', 'w', encoding="utf-8")
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
			#csv파일마다 있는열이있고 없는열도 있어서 없는열을 참조하려할때 오류뜸
			#그래서 없는열을 참조 할때는try catch로 csvtojson 실행함

			try:
				csvtojson.write('\n\t"TIME": '+'"'+row[time_index[file]]+'",' )	#"TIME": "2018-12-08 5:01"
			except:
				pass	
			try:
				csvtojson.write('\n\t"SIP": '+'"'+row[sip_index[file]]+'",' )
			except:
				pass
			try:
				csvtojson.write('\n\t"SPORT": '+'"'+row[sport_index[file]]+'",' )
			except:
				pass
			try:
				csvtojson.write('\n\t"DIP": '+'"'+row[dip_index[file]]+'",' )
			except:
				pass
			try:
				csvtojson.write('\n\t"DPORT": '+'"'+row[dport_index[file]]+'",' )
			except:
				pass
			try:
				csvtojson.write('\n\t"MSG": '+'"'+row[msg_index[file]]+'",' )
			except:
				pass
			
			csvtojson.write('\n\t"RES": '+'"'+res+'",' )
						
			raw_payload = row[rawdata_index[file]]

			while '\r' in raw_payload or '\n' in raw_payload:
				raw_payload = raw_payload.replace('\r', '')
				raw_payload = raw_payload.replace('\n', '')

			tmp_payload = ""

			for wrd in word:
				if wrd[0] in raw_payload:
					tmp_payload = tmp_payload + wrd[1]

			csvtojson.write('\n\t"PAYLOAD":' +'"'+tmp_payload+'"')


			
			csvtojson.write("\n}")
			check +=1
			
		except IndexError:			#공백 열이 있을 시
			pass
	f.close()
	csvtojson.write("\n]")
	csvtojson.close()
