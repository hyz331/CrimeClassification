import json
import csv
import scipy.io as sio
import datetime

def vectorize(minVal, maxVal, val):
	vec = [0 for i in range(0, maxVal-minVal+1)]
	vec[val-minVal] = 1
	return vec

# Load mapping and normalization parameters
labelMap = json.load(open('data/label_map.json'))
normParams = sio.loadmat('data/normalization_params.mat')

# Parse csv and perform normalization
inputfile = open('kaggle_raw_csv/test.csv')
csv = csv.reader(inputfile, delimiter=',')

Ids = []
Features = []
for row in csv:
	cid = row[0]
	date = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
	latitude = row[5]
	longitude = row[6]
	feature = [date.year, date.month, date.day, date.hour, date.weekday(), float(latitude), float(longitude)]
	Ids.append(cid)
	Features.append(feature)

# Perform normalization and binary vectorization
mins = normParams['mins'][0]
maxs = normParams['maxs'][0]
oneHot = []
for row in Features:
	vec = []
	for i in range(0, 5):
		vec = vec + vectorize(int(mins[i]), int(maxs[i]), int(row[i]))
	vec.append(((row[5] - mins[5]) / (maxs[5] - mins[5])))
	vec.append(((row[6] - mins[6]) / (maxs[6] - mins[6])))
	oneHot.append(vec)

sio.savemat('data/test_encoded', {'Ids': Ids, 'Features': oneHot})
