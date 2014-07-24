#!/usr/bin/env python
import sys
import os
import argparse

import csv

""" convert a tab delimted text file to csv. Based on this: http://stackoverflow.com/a/10220428 """

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='convert tab-delimited text file to CSV')

    parser.add_argument('file',  type=str,help='tab delimited text file to convert to CSV')

    args = parser.parse_args()

    basename= os.path.splitext(args.file)[0]

    csv_file=basename +".csv"

    in_txt = csv.reader(open(args.file, "rb"), delimiter = '\t')
    out_csv = csv.writer(open(csv_file, 'wb'))

    out_csv.writerows(in_txt)


if __name__ == "__main__":
    main()
