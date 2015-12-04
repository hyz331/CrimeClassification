import numpy as np
import scipy.io as sio
import json
import sys
import csv
import time
import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

def vectorize_bow(word_map, w1, w2):
	vec = [0 for i in range(0, len(word_map.keys()))]
	vec[word_map[w1]] = 1
	vec[word_map[w2]] = 1
	return vec

def vectorize(minVal, maxVal, val):
	vec = [0 for i in range(0, maxVal-minVal+1)]
	vec[val-minVal] = 1
	return vec

if (len(sys.argv) <= 1):
	print "Usage: python", sys.argv[0], "inputfile.csv"
	sys.exit()

fname = sys.argv[1]
csvfile = open(fname)

Labels = []
label_map = dict()
word_map = dict()
# Generate mapping and label vector
for row in csv.reader(csvfile, delimiter=','):
	category = row[6]
	district = row[2]
	street = row[3].split(' ')
	street = street[-2]
	# label mapping
	if (not category in label_map):
		label_map[category] = len(label_map.keys())
	# word mapping
	if (not district in word_map):
		word_map[district] = len(word_map.keys())
	if (not street in word_map):
		word_map[street] = len(word_map.keys())
	Labels.append(label_map[category])
csvfile.close()

csvfile = open(fname)
Features = []
# One hot encoding
count = 0
for row in csv.reader(csvfile, delimiter=','):
	# read data from row
	timestamp = float(row[0])
	latitude = float(row[4])
	longitude = float(row[5])
	district = row[2]
	street = row[3].split(' ')
	street = street[-2]

	# discretize timestamp
	date = datetime.datetime.fromtimestamp(timestamp)

	# add feature
	Features.append([date.year, date.month, date.day, date.hour, date.weekday()] +
					[latitude, longitude] + vectorize_bow(word_map, district, street))

	count = count + 1
	if (count > 10000): break

Labels = np.array(Labels)
Features = np.array(Features)

# Perform normalization
(numData, numFeature) = Features.shape
mins = Features.min(axis=0)
maxs = Features.max(axis=0)

oneHot = []
count = 0
for row in Features:
	vec = []
	for i in range(0, 5):
		vec = vec + vectorize(int(mins[i]), int(maxs[i]), int(row[i]))
	vec.append(((row[5] - mins[5]) / (maxs[5] - mins[5])))
	vec.append(((row[6] - mins[6]) / (maxs[6] - mins[6])))
	oneHot.append(vec)
	for i in range(7, len(row)):
		vec.append(row[i])
	count = count + 1
	if (count > 10000): break

print "Adaboost..."
X = oneHot
Y = Labels[0:10001]
weakClassifier = DecisionTreeClassifier(max_depth = 5)
classifier = AdaBoostClassifier(base_estimator = weakClassifier, n_estimators = 100)
classifier.fit(X, Y)
rank = classifier.feature_importances_
for i in rank:
	print i,
