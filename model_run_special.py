import model
import pickle



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

model.model_train(data, data_row_size, C, gamma)
