#!/usr/bin/env python
import sys
import gzip
import random
from optparse import OptionParser
from common  import return_file_basename

def main():
    """ randomly select N records from paired end fastq files
        code based on this: http://www.biostars.org/p/6544/#6555  """
    usage = "usage: %prog [options] file_1.fq.gz file_2.fq.gz"
    parser = OptionParser(usage)
    
    parser.add_option("--N", type="int", default=100, dest="N", help="number of records to randomly select")
    (options, args)=parser.parse_args()

    if len(args) !=2:
        sys.stderr.write("provide two fastq.gz files!\n")
        sys.exit(1)
    
    fq1=args[0]
    fq2=args[1]
    fq1_basename= return_file_basename(fq1)
    fq2_basename= return_file_basename(fq2)
    suba, subb = gzip.open(fq1_basename + ".subset.gz", "wb"), gzip.open(fq2_basename + ".subset.gz", "wb")
    
    
    
    records1 = sum(1 for _ in gzip.open(fq1)) / 4
    if options.N > records1:
        sys.stderr.write("number requested less than number in fastq file!")
    
    if sum(1 for _ in gzip.open(fq2)) / 4 != records1:
        sys.stderr.write("unequal number of fastq records in PE files!\n")
        sys.exit(1)
    
    fh1=gzip.open(fq1)
    fh2=gzip.open(fq2)
    
    rand_records=sorted([random.randint(0, records1 - 1) for _ in xrange(options.N)])

    rec_no=-1
    for rr in rand_records:
        while rec_no  < rr:
            rec_no+=1
            for i in range(4): fh1.readline()
            for i in range(4): fh2.readline()
        for i  in range(4):
            suba.write(fh1.readline())
            subb.write(fh2.readline())
        rec_no+=1
        
    print >>sys.stderr, "wrote to %s, %s" % (suba.name, subb.name)
            

if __name__ == "__main__":
    main()
