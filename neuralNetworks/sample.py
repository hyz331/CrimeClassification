import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import json
from sklearn import linear_model
from sklearn.neural_network import BernoulliRBM

# Load data
data = sio.loadmat('../data/space_time_label_binary.mat')
testData = sio.loadmat('../data/test_encoded.mat')
labelMap = json.load(open('../data/label_map.json'))
X = data['Features']
Y = np.transpose(data['Labels'][0])

# Fit model
logreg = linear_model.LogisticRegression(C=1e5)
model = logreg.fit(X[1:1000], Y[1:1000])

# Make prediction
X_test = testData['Features']
Ids = testData['Ids']
res = model.predict_proba(X_test)

# Format output
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

for i in range(0, len(res)):
	print >> outfile, str(Ids[i]) + ','.join(map(lambda p: str(p), res[i]))
