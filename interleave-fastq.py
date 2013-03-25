#!/usr/bin/env python
import sys
import os
import string
import re
from optparse import OptionParser
import gzip
from common import *

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("--forward", type="string", dest="forward", help="forward fastq gzipped file")
    parser.add_option("--reverse", type="string", dest="reverse", help="reverse fastq gzipped file")

    (options, args)=parser.parse_args()
    fh1=gzip.open(options.forward,'rb')
    fh2=gzip.open(options.reverse,'rb')
    
    fq1_gen=yieldFastqRecord(fh1)
    fq2_gen=yieldFastqRecord(fh2)

    for r1, r2 in itertools.izip(fq1_gen, fq2_gen):
        print r1
        print r2



if __name__ == "__main__":
    main()
