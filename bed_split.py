#!/usr/bin/env python
import sys
import os
import string
import re
from optparse import OptionParser

def returnIntervals(bedfh,size,overlap):
    regions=[]
    region_size=size
    for line in bedfh:
        if '_' in line: continue
        fields = line.strip().split("\t")

        chrom_name = fields[0]
        
        chrom_length = int(fields[2])
        region_start = 0
        
        while region_start < chrom_length-overlap:
            start = region_start
            end = region_start + region_size
            if end > chrom_length:
                end = chrom_length
            region_string = chrom_name + "\t" + str(region_start) + "\t" + str(end)
            regions.append(region_string)

            region_start = end - overlap

    return regions

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("--size", type="int", dest="size", help="window size to split the bed file into, default is 10000", default=10000)
    parser.add_option("--overlap", type="int", dest="overlap", help="window overlap size , default is 5000", default=5000)

    (options, args)=parser.parse_args()


    file=args[0]
    fh=open(file,'r')
    regions=returnIntervals(fh, options.size,options.overlap)

    for r in regions:
        print r




if __name__ == "__main__":
    main()
