import numpy as np
import scipy.io as sio
import json
import sys
import csv
import time
import datetime

def vectorize(minVal, maxVal, val):
	vec = [0 for i in range(0, maxVal-minVal+1)]
	if (val == - 1):
		return vec
	vec[val-minVal] = 1
	return vec

if (len(sys.argv) <= 1):
	print "Usage: python", sys.argv[0], "inputfile.csv"
	sys.exit()

word_map = json.load(open('data/word_map.json'))
fname = sys.argv[1]
csvfile = open(fname)
csv = csv.reader(csvfile, delimiter=',')

# One hot encoding
Features = []
Labels = []
label_map = dict()
for row in csv:
	# read data from row
	timestamp = float(row[0])
	category = row[6]
	latitude = float(row[4])
	longitude = float(row[5])
	district = row[2]
	street = row[3].split(' ')
	street = street[-2]

	# label mapping
	if (not category in label_map):
		label_map[category] = len(label_map.keys())

	# discretize timestamp
	if (district in word_map):
		disNum = word_map[district]
	else:
		disNum = -1
	if (street in word_map):
		strNum = word_map[street]
	else:
		strNum = -1

	date = datetime.datetime.fromtimestamp(timestamp)
	Labels.append(label_map[category])
	Features.append([date.year, date.month, date.day, int(date.hour/4), date.weekday(),\
					 disNum, strNum, latitude, longitude])

csvfile.close()
Labels = np.array(Labels)
Features = np.array(Features)

# Perform normalization
(numData, numFeature) = Features.shape
mins = Features.min(axis=0)
maxs = Features.max(axis=0)

oneHot = []
for row in Features:
	vec = []
	for i in range(0, 7):
		vec = vec + vectorize(int(mins[i]), int(maxs[i]), int(row[i]))
	vec.append(((row[7] - mins[7]) / (maxs[7] - mins[7])))
	vec.append(((row[8] - mins[8]) / (maxs[8] - mins[8])))
	oneHot.append(vec)

# Save processed data mat format
sio.savemat('data/train_encoded.mat', {'Features': oneHot, 'Labels': Labels})

# save nomralization parameters
sio.savemat('data/normalization_params', {'mins': mins, 'maxs': maxs})

# Save label map into JSON
mapfile = open('data/label_map.json', 'w+')
json.dump(label_map, mapfile)
mapfile.close()
