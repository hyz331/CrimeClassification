# This script takes in a Kaggle training csv, removes unnecessary columns and
# converte dates to timestamps

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

for row in csv:
	timestamp = time.mktime(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S').timetuple())
	category = row[1]
	day = row[3]
	district = row[4]
	address = row[6]
	x = float(row[7])
	y = float(row[8])
	print '%s,%s,%s,%s,%s,%s,%s' % (timestamp, day, district, address, x, y, category)

csvfile.close()
