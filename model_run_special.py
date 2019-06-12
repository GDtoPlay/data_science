#model 의 인자 C, Gamma값을 받아 train하는 프로그램. Special Char Dataset용.
import model
import pickle

#dataset load
with open('data_int_special.txt', 'rb') as f:
    data = pickle.load(f)

data_row_size = len(data[0][0])

C = 1.0
gamma = 1.0

try:
    C = float(input("C 값 입력\n"))
    gamma = float(input("gamma 값 입력\n"))

except ValueError as e:
    print(e)
    print('run defult C, gamma (10000.0, 1.0)')
    C = 10000.0
    gamma = 1.0

#model에 dataset, C, Gamma 인자를 넘겨주고, Special Char model이라는 정보를 넘겨주어 model_save_special폴더에 저장
model.model_train(data, data_row_size, C, gamma, True)
