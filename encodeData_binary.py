import numpy as np
import scipy.io as sio
import json
import sys
import csv
import time
import datetime

def vectorize(minVal, maxVal, val):
	vec = [0 for i in range(0, maxVal-minVal+1)]
	vec[val-minVal] = 1
	return vec

if (len(sys.argv) <= 1):
	print "Usage: python", sys.argv[0], "inputfile.csv"
	sys.exit()

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

	# label mapping
	if (not category in label_map):
		label_map[category] = len(label_map.keys())

	# discretize timestamp
	date = datetime.datetime.fromtimestamp(timestamp)
	Labels.append(label_map[category])
	Features.append([date.year, date.month, date.day, date.hour, date.weekday(),\
					 latitude, longitude])

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
	for i in range(0, 5):
		vec = vec + vectorize(int(mins[i]), int(maxs[i]), int(row[i]))
	vec.append(((row[5] - mins[5]) / (maxs[5] - mins[5])))
	vec.append(((row[6] - mins[6]) / (maxs[6] - mins[6])))
	oneHot.append(vec)

# Save processed data mat format
sio.savemat('data/space_time_label_binary.mat', {'Features': oneHot, 'Labels': Labels})

# save nomralization parameters
sio.savemat('data/normalization_params', {'mins': mins, 'maxs': maxs})

# Save label map into JSON
mapfile = open('data/label_map.json', 'w+')
json.dump(label_map, mapfile)
mapfile.close()
