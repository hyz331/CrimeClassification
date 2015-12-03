import numpy as np
import scipy.io as sio
import sys
import time
import datetime

# generate a csv file of (timestamp, lat, lon), default is a grid of SF 
# area 100x100 points

def main(ts=0,minLat=37.708805,maxLat=37.806250,minLon=-122.504894
,maxLon=-122.389194,s=0.001):
	for lat in np.arange(minLat,maxLat,s):
		for lon in np.arange(minLon,maxLon,s):		
			print '%s,%s,%s' % (ts, lat, lon)

if __name__=='__main__':
	if (len(sys.argv) == 1):
		sys.exit(main())
	#if (len(sys.argv) <= 6):
	#	print "Usage: python", sys.argv[0], "timestamp", "min_lat","max_lat","min_lon","max_lon", "step"
	#	sys.exit()
	elif(len(sys.argv) == 7):
		sys.exit(main(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6])))
	else:
		print "Usage: python", sys.argv[0], "timestamp", "min_lat","max_lat","min_lon","max_lon", "step"
		sys.exit()