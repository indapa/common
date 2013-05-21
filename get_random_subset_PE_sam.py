#!/usr/bin/env python
import sys
import gzip
import random
from optparse import OptionParser
from common  import return_file_basename
import pysam

def main():
    
    """ get a specified number of paired-end reads from a samfile """
    usage = "usage: %prog [options] readname_sorted.sam"
    parser=OptionParser(usage)
    parser.add_option("--N", type="int", default=100, dest="N", help="number of records to randomly select")
    parser.add_option("--h", action="store_true", dest="header",  default=False, help="set if header included in samfile")
    (options,args)=parser.parse_args()
    
    samfilename=args[0]
    basename=return_file_basename(samfilename)
    
    subfh=open(basename+".subset.sam", "w")
    
    samfh=open(samfilename, 'r')
    if options.header==True:
        inheader=True
        while (inheader):
            headerline=samfh.readline()
            if headerline.startswith('@'):
                subfh.write(headerline)
            else: 
                break
    
    records1 = sum(1 for _ in open(samfilename)) / 2
    rand_records=sorted([random.randint(0, records1 - 1) for _ in xrange(options.N)])
    
    print rand_records
    
    rec_no=-1
    
    for rr in rand_records:
        while rec_no < rr:
            rec_no+=1
            for i in range(2): samfh.readline()
        for i in range(2):
            subfh.write(samfh.readline())
        rec_no+=1
        
    print >>sys.stderr, "wrote to %s" % (subfh.name)
                
    
    
   
if __name__ == "__main__":
    main()
