import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import json
import sys
from sklearn import svm
from sklearn.metrics import log_loss
from sklearn import linear_model
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
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
weakClassifier = DecisionTreeClassifier(max_depth = 7)
#classifier = AdaBoostClassifier(base_estimator = DecisionTreeClassifier(), n_estimators = 50)
#scores = cross_validation.cross_val_score(classifier, X, Y, cv=5, scoring='log_loss')
classifier = AdaBoostClassifier(base_estimator = weakClassifier, n_estimators = 60)
classifier.fit(X, Y)
pred = classifier.predict_proba(X)
print log_loss(Y, pred)
print classifier.feature_importances_

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

		for i in range(0, len(pred)):
			print >> outfile, str(Ids[i]) + ',' + ','.join(map(lambda p: str(p), pred[i]))
