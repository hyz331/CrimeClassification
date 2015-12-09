import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import json
import sys
import csv
import time
import datetime

from sklearn import svm
from sklearn.metrics import log_loss
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation

# Load data
data = sio.loadmat('../data/train_encoded.mat')
testData = sio.loadmat('../data/test_encoded.mat')
normParams = sio.loadmat('../data/normalization_params.mat')
labelMap = json.load(open('../data/label_map.json'))
csvfile = open('../kaggle_raw_csv/test.csv')
rawTest = csv.reader(csvfile, delimiter=',')

X = data['Features']
Y = np.transpose(data['Labels'][0])

# Fit model
print 'Training...'
#classifier = svm.SVC(probability=True,C=0.0001)
classifier = linear_model.LogisticRegression()
#classifier = MultinomialNB()
#weakClassifier = DecisionTreeClassifier(max_depth = 15)
#classifier = AdaBoostClassifier(base_estimator = weakClassifier, n_estimators = 300)

#classifier.fit(X[0:1000], Y[0:1000])
#train_pred = classifier.predict_proba(X[0:1000])
#print log_loss(Y[0:1000], train_pred)

classifier.fit(X, Y)
train_pred = classifier.predict_proba(X)
print log_loss(Y, train_pred)

# Predict and get score
print 'Predicting...'
X_test = testData['Features']
Ids = testData['Ids']
test_pred = classifier.predict_proba(X_test)
test_pred = np.around(test_pred, decimals=5)

# Format output
print 'Outputing...'
outfile = open('../test_pred_weight.csv', 'w+')
i = 0
for row in rawTest:
	timestamp = time.mktime(datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').timetuple())
	lat = row[6]
	lon = row[5]
	print >> outfile, str(timestamp) + ',' + lat + ',' + lon + ',' + ','.join(map(lambda p: str(p), test_pred[i]))
	i = i + 1