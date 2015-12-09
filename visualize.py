import os
import numpy as np
import scipy.io as sio
import sys
import csv
import time
import datetime
import gmplot

category_set = ["FORGERY/COUNTERFEITING",
"LARCENY/THEFT",
"BURGLARY",
"SUSPICIOUS OCC",
"DRUG/NARCOTIC",
"NON-CRIMINAL",
"OTHER OFFENSES",
"MISSING PERSON",
"WARRANTS",
"VEHICLE THEFT",
"ASSAULT",
"WEAPON LAWS",
"ROBBERY",
"SEX OFFENSES FORCIBLE",
"TRESPASS",
"VANDALISM",
"KIDNAPPING",
"RUNAWAY",
"SECONDARY CODES",
"PROSTITUTION",
"FRAUD",
"DISORDERLY CONDUCT",
"DRUNKENNESS",
"STOLEN PROPERTY",
"RECOVERED VEHICLE",
"LIQUOR LAWS",
"DRIVING UNDER THE INFLUENCE",
"ARSON",
"BRIBERY",
"LOITERING",
"GAMBLING",
"EMBEZZLEMENT",
"SUICIDE",
"BAD CHECKS",
"FAMILY OFFENSES",
"EXTORTION",
"SEX OFFENSES NON FORCIBLE",
"TREA",
"PORNOGRAPHY/OBSCENE MAT"]

color_table = dict()
color_table["FORGERY/COUNTERFEITING"] = 'CC0000'
color_table["LARCENY/THEFT"] = 'FF6666'
color_table["BURGLARY"] = 'FFCCCC'
color_table["SUSPICIOUS OCC"] = '663300'
color_table["DRUG/NARCOTIC"] = 'FF6600'
color_table["NON-CRIMINAL"] = 'FF9966'
color_table["OTHER OFFENSES"] = 'FFCC99'
color_table["MISSING PERSON"] = '996633'
color_table["WARRANTS"] = 'FFCC00'
color_table["VEHICLE THEFT"] = 'FFFF33'
color_table["ASSAULT"] = '006600'
color_table["WEAPON LAWS"] = '00CC00'
color_table["ROBBERY"] = '66FF66'
color_table["SEX OFFENSES FORCIBLE"] = '003333'
color_table["TRESPASS"] = '006666'
color_table["VANDALISM"] = '009999'
color_table["KIDNAPPING"] = '00CCCC'
color_table["RUNAWAY"] = '66FFCC'
color_table["SECONDARY CODES"] = '003399'
color_table["PROSTITUTION"] = '0066FF'
color_table["FRAUD"] = '0099FF'
color_table["DISORDERLY CONDUCT"] = '00FFFF'
color_table["DRUNKENNESS"] = '006666'
color_table["STOLEN PROPERTY"] = '0000CC'
color_table["RECOVERED VEHICLE"] = '99CCFF'
color_table["LIQUOR LAWS"] = '9999CC'
color_table["DRIVING UNDER THE INFLUENCE"] = '330066'
color_table["ARSON"] = '660099'
color_table["BRIBERY"] = '9900CC'
color_table["LOITERING"] = '9966FF'
color_table["GAMBLING"] = '9999FF'
color_table["EMBEZZLEMENT"] = '666699'
color_table["SUICIDE"] = '660066'
color_table["BAD CHECKS"] = 'CC0099'
color_table["FAMILY OFFENSES"] = 'FF0099'
color_table["EXTORTION"] = 'FF00FF'
color_table["SEX OFFENSES NON FORCIBLE"] = 'FF66FF'
color_table["TREA"] = 'FF99FF'
color_table["PORNOGRAPHY/OBSCENE MAT"] = '999999'

#if (len(sys.argv) <= 3):
#        print "Usage: python", sys.argv[0], "inputfile.csv", "crime_label", "year"
#        sys.exit()

def main(fname,crime_label,y=-1, draw_heatmap=False):

        #fname = sys.argv[1]
        #y = int(sys.argv[3])
        #crime_label = sys.argv[2]
        csvfile = open(fname)
        file_csv = csv.reader(csvfile, delimiter=',')

        gmap = gmplot.GoogleMapPlotter.from_geocode("San Francisco")

        #xlist = [[] for i in range(0, len(category_set))]
        #ylist = [[] for i in range(0, len(category_set))]
        xlist = []
        ylist = []

        for row in file_csv:
                timestamp = row[0]
                date = datetime.datetime.fromtimestamp(float(timestamp))
                year = date.strftime('%Y')        
                day = row[1]
                district = row[2]
                address = row[3]
                lon = float(row[4])
                lat = float(row[5])
                category = row[6]
                if(category == crime_label):
                        if(y == -1 or y == int(year)):
                                #for i in range(0,1):
                                xlist.append(lat)
                                ylist.append(lon)    
        #for i in range(0, len(category_set)):
        #	gmap.scatter(xlist[i], ylist[i], color=color_table[category_set[i]], size=40, marker=False)       
        print len(xlist)
        if draw_heatmap:               
                gmap.heatmap(xlist, ylist, threshold=20, radius=40)
        else:
                gmap.scatter(xlist, ylist, color=color_table[crime_label], size=40, marker=False)
        crime_convert = crime_label.replace(" ", "_").replace("/", "_")
        if not os.path.exists("maps/" + crime_convert):
                os.makedirs("maps/" + crime_convert)
        filename = "maps/" + crime_convert + "/" + crime_convert + `y` + ".html"
        gmap.draw(filename)

        csvfile.close()
        return 0;

if __name__=='__main__':
        sys.exit(main(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]=='True'))