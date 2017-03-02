#!/usr/bin/env python3
'''
This program plots fail2ban logs by geolocating IPs from
the logfile and then plotting them on a Google Maps doc
'''

import argparse
import os
import subprocess
import sys
import webbrowser

from bs4 import BeautifulSoup
import gmplot
import requests

def is_valid_file(parser, arg):
    '''
    Helper function that checks if log file is valid
    and returns file object to main()
    '''
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')

def clean_logfile(log):
    '''
    Function uses gnu utils to turn fail2ban.log
    to all IP addresses
    '''
    command = "grep -i unban {} | awk '{{print $8}}' | sort | uniq > .new.log".format(log.name)
    subprocess.Popen(command, shell=True)

def map_ip(ipaddr):
    '''
    url = "https://ipinfo.io/%s/json" % ipaddr
    r = requests.get(url).json()
    print(r['city'],r['country'],r['loc'])
    '''
    url = "http://freegeoip.net/json/%s" % ipaddr
    req = requests.get(url).json()
    print(req['city'], req['country_code'], req['latitude'], req['longitude'])
    return req['latitude'], req['longitude']

def start_browser():
    '''
    Function opens map webpage in the appropriate browser
    '''
    import platform
    system = platform.system()
    if system == "Darwin":
        chrome_path = r'open -a /Applications/Google\ Chrome.app %s'
    elif system == "win32":
        # Windows
        chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
    else:
        print("Please open ./mymap.html in your favorite browser!")
        return None
    webbrowser.get(chrome_path).open("./mymap.html")

def plot_pnts(coord_list):
    '''
    Function takes a list of coordinates and plots them on
    google maps plot.  Can either be a scatter plot or heatmap
    '''
    latitudes = [coord[0] for coord in coord_list]
    longitudes = [coord[1] for coord in coord_list]
    gmap = gmplot.GoogleMapPlotter(0, 0, 3)
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
    gmap.scatter(latitudes, longitudes, 'k', marker=True)
    #gmap.heatmap(latitudes, longitudes)
    gmap.draw("mymap.html")

def main():
    '''
    Main function, takes user supplied fail2ban log file and
    converts it to map image
    '''
    parser = argparse.ArgumentParser(description="input file")
    parser.add_argument("-i", dest="filename", required=True,
                        help="The log file to be mapped", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-x", dest="clean", required=False, default=False, action='store_true',
                        help="This option signals fbmap to clean your log file")
    args = parser.parse_args()

    if args.clean:
        clean_logfile(args.filename) 
        args.filename = is_valid_file(parser, ".new.log")

    while True:
        try:
            coords = [map_ip(line.split()[-1]) for line in args.filename]
            for coord in coords:
                print(coord)
            plot_pnts(coords)
            start_browser()
            break
        except KeyboardInterrupt:
            print("Goodbye...")
            sys.exit(-1)

if __name__ == "__main__":
    main()
