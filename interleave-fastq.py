#!/usr/bin/env python
import sys
import os
import string
import re
import itertools
from optparse import OptionParser
from common import yieldFastqRecord
import gzip

def main():
    
    """ Interleave records of fastq files. For example if given file1.fq and file2.fq
        the program will print fastq record from file1 followed by fastq record from file2,
        alternating between to two files till exhausted. Note this assumes that the
        fastq records have the same number of records. The code here is adapted from
        this biostars post: http://www.biostars.org/p/67246/#67556 """
    
    usage = "usage: %prog [options] file1.fastq file2.fastq ... fileN.fastq"
    parser = OptionParser(usage)
    
    parser.add_option("--gunzip", action="store_true", dest="gunzip", default=False,  help="fastq files are uncompressed")
    (options, args)=parser.parse_args()

    
    fastqfiles=args[0:]
    fqfilehandles=[]
    
    if options.gunzip == True:
        fqfilehandles=list(itertools.imap(open, fastqfiles)) #list of filehandles for fastq files
    else:
        fqfilehandles=list(itertools.imap(gzip.open, fastqfiles))
    
    # interleave the fastas with izip and chain the results. this is all lazy
    fastq_records = itertools.chain.from_iterable(itertools.izip(*[yieldFastqRecord(fh) for fh in fqfilehandles]))
    
    for header,seq,qual in fastq_records:
        print "\n".join([header,seq,"+",qual])
if __name__ == "__main__":
    main()
