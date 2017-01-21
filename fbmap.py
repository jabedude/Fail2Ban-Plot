#!/usr/bin/env python3

import sys
import argparse
import os
import requests
import gmplot

def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return open(arg, 'r')

def map_ip(ipaddr):
        '''
        url = "https://ipinfo.io/%s/json" % ipaddr
        r = requests.get(url).json()
        print(r['city'],r['country'],r['loc'])
        '''
        url = "http://freegeoip.net/json/%s" % ipaddr
        r = requests.get(url).json()
        print(r['city'],r['country_code'],r['latitude'],r['longitude'])

def plot_pnt():
        gmap = gmplot.GoogleMapPlotter(0,0,3)
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/" 
        gmap.scatter([32.0617], [118.7778], 'k', marker=True)
        gmap.draw("mymap.html")

def main():
        parser = argparse.ArgumentParser(description="input file")
        parser.add_argument("-i", dest="filename", required=True, help="The log file to be mapped", metavar="FILE", type=lambda x:is_valid_file(parser, x))
        args = parser.parse_args()

        #print(type(args.filename))

        #for line in args.filename:
        #        map_ip(line.split()[-1])
        plot_pnt()

if __name__ == "__main__":
        main()

