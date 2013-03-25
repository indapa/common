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
    parser.add_option("--forward", type="string", dest="fwd", help="forward fastq gzipped file")
    parser.add_option("--reverse", type="string", dest="reverse", help="reverse fastq gzipped file")

    (options, args)=parser.parse_args()
    
    
    fq1_gen=yieldFastqRecord(options.fwd)
    fq2_gen=yieldFastqRecord(options.reverse)

    for r1, r2 in itertools.izip(fq1_gen, fq2_gen):
        print r1
        print r2



if __name__ == "__main__":
    main()
