import model
import pickle



with open('data_int.txt', 'rb') as f:
    data = pickle.load(f)


data_row_size = len(data[0][0])


model.model_train(data, data_row_size, 10000.0, 1)
