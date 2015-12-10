import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import json
import sys
from sklearn import svm
from sklearn.metrics import log_loss
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.ensemble import GradientBoostingClassifier 

# Load data
data = sio.loadmat('../data/train_encoded.mat')
testData = sio.loadmat('../data/test_encoded.mat')
normParams = sio.loadmat('../data/normalization_params.mat')
labelMap = json.load(open('../data/label_map.json'))

X = data['Features']
Y = np.transpose(data['Labels'][0])

# Fit model
print 'Training...'
classifier = GradientBoostingClassifier(n_estimators = 35, verbose = 2)
classifier.fit(X, Y)

# Predict and get score
'Predicting...'
X_test = testData['Features']
Ids = testData['Ids']
pred = classifier.predict_proba(X_test)

# Format output
print 'Outputing...'
outfile = open('submission.csv', 'w+')
revMap = dict()
for k in labelMap:
	revMap[labelMap[k]] = k
keys = revMap.keys()
keys.sort()
header = 'id'
for k in keys:
	header = header + ',' + revMap[k]
print >> outfile, header

pred = np.around(pred, decimals=9)
for i in range(0, len(pred)):
	print >> outfile, str(Ids[i]) + ',' + ','.join(map(lambda p: str(p), pred[i]))
