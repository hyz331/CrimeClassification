import numpy as np
import scipy.io as sio
import json
import sys
import csv
import time
import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.ensemble import ExtraTreesClassifier

def vectorize_bow(word_map, w1):
	vec = [0 for i in range(0, len(word_map.keys()))]
	vec[word_map[w1]] = 1
	return vec

if (len(sys.argv) <= 1):
	print "Usage: python", sys.argv[0], "inputfile.csv"
	sys.exit()

print "Processing data..."
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
	Labels.append(label_map[category])
csvfile.close()

# One hot encoding
Features = []
csvfile = open(fname)
for row in csv.reader(csvfile, delimiter=','):
	# read data from row
	district = row[2]
	Features.append(vectorize_bow(word_map, district))

Labels = np.array(Labels)
Features = np.array(Features)
csvfile.close()

print "Selecting..."
X = Features 
Y = Labels
classifier = ExtraTreesClassifier()
classifier.fit(X, Y)
rank = classifier.feature_importances_

revMap = dict()
for k in word_map.keys():
	revMap[word_map[k]] = k

for i in range(0, len(rank)):
	print revMap[i], rank[i]
