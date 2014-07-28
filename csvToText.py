#!/usr/bin/env python
import sys
import os
import argparse

import csv

""" convert a CSV file to text. Based on this: http://stackoverflow.com/a/10220428 """

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='convert CSV file to tab delimited')

    parser.add_argument('file',  type=str,help='CSV file to convert to tab-delimited')

    args = parser.parse_args()

    basename= os.path.splitext(args.file)[0]

    text_file=basename +".txt"

    in_csv = csv.reader(open(args.file, "rb"), delimiter = ',')
    out_text = csv.writer(open(text_file, 'wb'), delimiter= "\t")

    out_text.writerows(in_csv)


if __name__ == "__main__":
    main()
