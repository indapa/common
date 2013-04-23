#!/usr/bin/env python
import gzip
from optparse import OptionParser
def main():
    
    usage = "usage: %prog [options] file.fastq.gz"
    parser = OptionParser(usage)
    
    
    (options, args)=parser.parse_args()

    if len(args) !=1:
        sys.stderr.write("provide  fastq.gz file!\n")
        sys.exit(1)
    
    fq1=args[0]
    
    
    records1 = sum(1 for _ in gzip.open(fq1)) / 4
    print records1
            

if __name__ == "__main__":
    main()
