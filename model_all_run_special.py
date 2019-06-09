import model
import pickle



with open('data_int_special.txt', 'rb') as f:
    data = pickle.load(f)


data_row_size = len(data[0][0])

#C = 1.0
#gamma = 1.0

try:
    C_min = float(input("C 값 최소치 입력\n"))
    C_max = float(input("C 값 최대치 입력\n"))
    C_interval = float(input("C 값 간격(지수) 입력\n"))
	
    gamma_min = float(input("gamma 값 최소치 입력\n"))
    gamma_max = float(input("gamma 값 최대치 입력\n"))
    gamma_interval = float(input("gamma 값 간격(지수) 입력\n"))

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
		model.model_train(data, data_row_size, C, gamma)
		gamma *= gamma_interval
	C *= C_interval
