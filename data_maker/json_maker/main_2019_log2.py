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

dirname = "../LOG/"
#파일마다 열순서가 다르다 그래서 특정 문자가 몇번째 열에잇는지 구하는것
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
	csvtojson = open('../json/' + file[:-4] + '.json', 'w', encoding="utf-8")
	csvtojson.write("[\n")
	f = open(dirname+file,'r',encoding='utf-8') 
	rdr = csv.reader(f)
	print("processing : " + file)
	check = 0							#엑셀 첫행 체크용 변수 
	for row in rdr:
		file_data={}
		try:
			if check==0:	#엑셀 첫행 건너뛰기 용
				check+=1
				continue
			#json.dump 하면 이스케이프문자 그대로 덤프되서 이렇게 일일히 다써줌
			if check!=1:	#엑셀 첫행 건너뛰기 용
				check+=1
				csvtojson.write(",\n")
			csvtojson.write("{")
			#csv파일마다 있는열이있고 없는열도 있어서 없는열을 참조하려할때 오류뜸
			#그래서 없는열을 참조 할때는try catch로 csvtojson 실행함
			#json.dump 하면 이스케이프문자 그대로 덤프되서 이렇게 일일히 다써줌
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
						
			if row[rawdata_index[file]]!="":
				payload_str = tojson_oneline(row[rawdata_index[file]])
				if payload_str!=0:	#tojosn_oneline에서 trycatch로 예외처리한것
					csvtojson.write('\n\t"PAYLOAD": '+'[' )
					csvtojson.write( payload_str )
					csvtojson.write(']')
				else:
					csvtojson.write('\n\t"PAYLOAD": []' )

			
			else:
				csvtojson.write('\n\t"PAYLOAD": []' )


			'''
			속도떄문에 이거 일부러 주석
			try:
				payload_json_bunch = pay2json( row[payload_index[file]] )	#한칸에 GET POS몰려서 적혀있을경우 패킷이 여러개있어서 bunch라고 이름지음
				csvtojson.write('\n\t"PAYLOAD":' +'[')
				csvtojson.write(payload_json_bunch)
				csvtojson.write(']')
			except:
				pass
			'''
			
			csvtojson.write("\n}")
			check +=1
			
		except IndexError:			#12110301_12110500_ok.csv 에 공백열이잇다. 그래서 예외처리
			pass
	f.close()
	csvtojson.write("\n]")
	csvtojson.close()
