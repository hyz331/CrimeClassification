import numpy as np
import scipy.io as sio
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
category_map = dict()
for row in csv:
	timestamp = float(row[0])
	category = row[6]
	x = float(row[4])
	y = float(row[5])

	if (not category in category_map):
		category_map[category] = len(category_map.keys())
	Labels.append(category_map[category])
	Features.append([timestamp, x, y])
csvfile.close()
Labels = np.array(Labels)
Features = np.array(Features)

# Save into mat format
sio.savemat('space_time_label.mat', {'Features': Features, 'Labels': Labels})
