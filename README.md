[![Build Status](https://travis-ci.org/RussianOtter/romap.svg?branch=master)](https://travis-ci.org/RussianOtter/romap)

# Romap - Advanced Network Scanner

usage: romap.py [-h] [-l LOG] [-a] [-p PUBLIC] [-d] [-H HOST] [-P RANGE]

                [-t TIMEOUT] [-D DIRECT] [-m MID] [-M MID] [-n] [-S SEARCH]


optional arguments:

  -h, --help            show this help message and exit
  
  -l LOG, --log LOG     Logs scan to file
  
  -a, --accesspoint     Locate access points
  -p PUBLIC, --public PUBLIC
  
                        Scan Public Addresses
                        
  -d, --detail          Device Detail Information
  
  -H HOST, --Host HOST  Scan Selective Target
  
  -P RANGE, --Range RANGE
  
                        Port Range For -H
                        
  -t TIMEOUT, --timeout TIMEOUT
  
                        Set timeout
                        
  -D DIRECT, --Direct DIRECT
  
                        Directly Scan Device
                        
  -m MID, --mid MID     Second IP Range [17-62]
  
  -M MID, --Mid MID     Third IP Range [17-62]
  
  -n, --nohelp          Hides Autohelp
  
  -S SEARCH, --Search SEARCH
  
                        Search For Port While Scanning
                        
Examples:

romap.py -n -d -s -m 1-13 -t 1 -l log.txt
romap.py -H 192.168.1.254 -P 1000
romap.py -n
