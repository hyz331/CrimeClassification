import visualize
import sys
import csv
import gmplot

if (len(sys.argv) < 2):
        print "Usage: python", sys.argv[0], "mode"
        sys.exit()

mode = int(sys.argv[1])

# mode 1 draws the heatmap the old way from training data
if mode==1:
	with open("category_list.txt") as f:
	    category_list = f.read().splitlines()
	for i in category_list:
		print(category_list[i])
		for year in range(2003, 2015+1):
			visualize.main("train.csv", category_list[i], year)

# mode 2 takes a csv file(col0=timestamp, col1=lat, col2=lon), and draws a scatter plot(for now)
elif mode==2:
	fname = sys.argv[2]
	csvfile = open(fname)
	csv = csv.reader(csvfile, delimiter=',')	
	xlist = []
	ylist = []

	for row in csv:
		timestamp = float(row[0])
		lat = float(row[1])
		lon = float(row[2])
		xlist.append(lat)
		ylist.append(lon)

	gmap = gmplot.GoogleMapPlotter.from_geocode("San Francisco")
	gmap.scatter(xlist, ylist, color="0000ff", size=40, marker=False)
	gmap.draw("output_map.html")
	csvfile.close()