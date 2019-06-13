#Model_run의 인자 C, Gamma값을 Grid Search하는 프로그램
import model
import pickle

#dataset load
with open('data_int.txt', 'rb') as f:
    data = pickle.load(f)

data_row_size = len(data[0][0])

#C, Gamma의 최솟값, 최댓값, 지수를 받아 Grid Search
try:
    C_min = float(input("C 값 최소치 입력\n"))
    C_max = float(input("C 값 최대치 입력\n"))
    C_interval = float(input("C 값 간격(지수) 입력\n"))
	
    gamma_min = float(input("gamma 값 최소치 입력\n"))
    gamma_max = float(input("gamma 값 최대치 입력\n"))
    gamma_interval = float(input("gamma 값 간격(지수) 입력\n"))

#기본값
except ValueError as e:
    print(e)
    print('run default')
    C_min = 1
    C_max = 10
    C_interval = 10
    gamma_min = 1
    gamma_max = 10
    gamma_interval = 10
	
C = C_min
gamma = gamma_min

while(C_max >= C):
	gamma = gamma_min
	while(gamma_max >= gamma):
		print("C :",C,"Gamma :", gamma)
		#model에 dataset, C, Gamma 인자를 넘겨주고, Special Char model이 아니라는 정보를 넘겨주어 model_save폴더에 저장
		model.model_train(data, data_row_size, C, gamma, False)
		gamma *= gamma_interval
	C *= C_interval
	