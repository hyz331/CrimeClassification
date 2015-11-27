import numpy as np
import scipy.io as sio
import json
import sys
import csv
import time
import datetime

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
Features = Features - mins
maxs = Features.max(axis=0)
Features = Features / maxs

# save nomralization parameters
sio.savemat('data/normalizatoin_params', {'minYear': mins[0], 'minMonth': mins[1],\
										  'minDay': mins[2], 'minHour': mins[3],\
										  'minWeekday': mins[4], 'minLat': mins[5],\
										  'minLong': mins[6]})

# Save processed data mat format
sio.savemat('data/space_time_label.mat', {'Features': Features, 'Labels': Labels})

# Save label map into JSON
mapfile = open('data/label_map.json', 'w+')
json.dump(label_map, mapfile)
mapfile.close()
