#!/usr/bin/env python3

import sys
import argparse
import os
import requests
import gmplot
import webbrowser
from bs4 import BeautifulSoup

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
        return r['latitude'], r['longitude']

def start_browser():
        import platform
        system = platform.system()
        if system == "Darwin":
                chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        elif system == "win32":
                # Windows
                chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
        else:
                print("Please open ./mymap.html in your favorite browser!")
                return None
        webbrowser.get(chrome_path).open("./mymap.html")

def plot_pnts(coord_list):
        latitudes  = [coord[0] for coord in coord_list]
        longitudes = [coord[1] for coord in coord_list]
        gmap = gmplot.GoogleMapPlotter(0,0,3)
        gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/" 
        gmap.scatter(latitudes, longitudes, 'k', marker=True)
        #gmap.heatmap(latitudes, longitudes)
        gmap.draw("mymap.html")
        start_browser()

def main():
        parser = argparse.ArgumentParser(description="input file")
        parser.add_argument("-i", dest="filename", required=True, 
                            help="The log file to be mapped", metavar="FILE",
                            type=lambda x:is_valid_file(parser, x))
        args = parser.parse_args()

        while True:
                try:
                        coords = [map_ip(line.split()[-1]) for line in args.filename]
                        for coord in coords:
                                print(coord)
                        plot_pnts(coords)
                        break
                except KeyboardInterrupt:
                        print("Goodbye...")
                        sys.exit(-1)

if __name__ == "__main__":
        main()

