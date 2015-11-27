import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from sklearn import linear_model, datasets

data = sio.loadmat('../data/space_time_label_binary.mat')
logreg = linear_model.LogisticRegression(C=1e5)
X = data['Features'][1:1000]
Y = np.transpose(data['Labels'][0][1:1000])

X_test = data['Features'][1000:2000]
Y_test = np.transpose(data['Labels'][0][1000:2000])

model = logreg.fit(X, Y)
print model.score(X_test, Y_test)
