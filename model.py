from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import numpy
import mglearn

def model_train(data_and_target, data_row_size, set_C, set_gamma):

    data = data_and_target[0]
    target = data_and_target[1]    # data_and_target: [data, target]
    
    X_train, X_test, y_train, y_test = train_test_split(data, target, random_state=0)

    svc = SVC(kernel='rbf', C=set_C, gamma=set_gamma).fit(X_train, y_train)


    print("훈련 세트 정확도: {:.2f}".format(svc.score(X_train, y_train)))
    print("테스트 세트 정확도: {:.2f}".format(svc.score(X_test, y_test)))

    joblib.dump(svc, 'model_save/parameter_c_'+str(set_C)+'_gamma_' +str(set_gamma)+ '.pkl')

    return svc



def test():
    X,y = make_blobs(centers=4, random_state=8)
    y = y % 2

    mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
    plt.xlabel("특성 0")
    plt.ylabel("특성 1")

    data = [X, y]

    svc = model_train(data, 2, 10000.0, 0.8)

    mglearn.plots.plot_2d_separator(svc, X, eps=.5)

    plt.legend()
    plt.show()
