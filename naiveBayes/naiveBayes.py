import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import json
import sys
from sklearn import linear_model
from sklearn.neural_network import BernoulliRBM

# Load data
data = sio.loadmat('../data/space_time_label_binary.mat')
testData = sio.loadmat('../data/test_encoded.mat')
normParams = sio.loadmat('../data/normalization_params.mat')
labelMap = json.load(open('../data/label_map.json'))

X = data['Features']
Y = np.transpose(data['Labels'][0])
mins = normParams['mins'][0]
maxs = normParams['maxs'][0]

maxLatOffset = maxs[5] - mins[5]
maxLonOffset = maxs[6] - mins[6]

def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step

def getCoordVal(lat, lon):
	val = 0
	stepLat = maxLatOffset / 50
	stepLon = maxLonOffset / 50
	for latLeft in drange(0.0, maxLatOffset - stepLat + 0.02, stepLat):
		for lonLeft in drange(0.0, maxLonOffset - stepLon + 0.02, stepLon):
			if ( lat >= latLeft and lat < latLeft + stepLat and \
				 lon >= lonLeft and lon < lonLeft + stepLon):
				return val
			else:
				val = val + 1
	raise Exception('lat or lon out of bound')

print getCoordVal(0, 52.1)

# Fit model
#logreg = linear_model.LogisticRegression(C=1e5)
#model = logreg.fit(X, Y)

# Make prediction
#X_test = testData['Features']
#Ids = testData['Ids']
#res = model.predict_proba(X_test)

# Format output
#outfile = open('submission.csv', 'w+')
#revMap = dict()
#for k in labelMap:
#	revMap[labelMap[k]] = k
#keys = revMap.keys()
#keys.sort()
#header = 'id'
#for k in keys:
#	header = header + ',' + revMap[k]
#print >> outfile, header

#for i in range(0, len(res)):
#	print >> outfile, str(Ids[i]) + ','.join(map(lambda p: str(p), res[i]))
