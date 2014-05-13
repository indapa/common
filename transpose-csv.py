#!/usr/bin/env python
import sys
import os
import argparse
from common import return_file_basename
import csv
from itertools import izip

""" Transpose a CSV file or pivot, I'm not sure which. Anyhow, this program makes rows into columns
    See this post on Stack Overflow http://stackoverflow.com/a/4869245 
    If file is file.csv the output is written to file.transposed.csv """

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='Program description')
    parser.add_argument( dest='csvfile', help="csvfile to pivot (turn rows into columns)\n")
    
    args = parser.parse_args()
    
    csvbasename=return_file_basename(args.csvfile)
    
    outfilecsv= csvbasename+".transposed.csv"
    
    
    
    a = izip(*csv.reader(open(args.csvfile, "rb")))
    csv.writer(open(sys.stdout, "wb")).writerows(a)
    
    
    
    

if __name__ == "__main__":
    main()
