import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import json
import sys
from sklearn import svm
from sklearn.metrics import log_loss
from sklearn import linear_model
from sklearn import cross_validation 

# Load data
data = sio.loadmat('../data/space_time_label_binary.mat')
testData = sio.loadmat('../data/test_encoded.mat')
normParams = sio.loadmat('../data/normalization_params.mat')
labelMap = json.load(open('../data/label_map.json'))

X = data['Features']
Y = np.transpose(data['Labels'][0])

# Fit model
print 'Training...'
#classifier = svm.SVC(C = 10, probability=True)
classifier = linear_model.LogisticRegression()
scores = cross_validation.cross_val_score(classifier, X, Y, cv=5, scoring='log_loss')
print scores
