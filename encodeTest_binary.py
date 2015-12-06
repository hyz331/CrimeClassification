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
word_map = json.load(open('data/word_map.json'))

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

	district = row[3]
	street = row[4].split(' ')
	street = street[-2]

	if (district in word_map):
		disNum = word_map[district]
	else:
		disNum = -1
	if (street in word_map):
		strNum = word_map[street]
	else:
		strNum = -1

	Ids.append(cid)
	Features.append([date.year, date.month, date.day, int(date.hour/4), date.weekday(),\
					 disNum, strNum, latitude, longitude])

# Perform normalization and binary vectorization
mins = normParams['mins'][0]
maxs = normParams['maxs'][0]
oneHot = []
for row in Features:
	vec = []
	for i in range(0, 7):
		vec = vec + vectorize(int(mins[i]), int(maxs[i]), int(row[i]))
	vec.append(((float(row[7]) - float(mins[7])) / (float(maxs[7]) - float(mins[7]))))
	vec.append(((float(row[8]) - float(mins[8])) / (float(maxs[8]) - float(mins[8]))))
	oneHot.append(vec)

sio.savemat('data/test_encoded', {'Ids': Ids, 'Features': oneHot})
