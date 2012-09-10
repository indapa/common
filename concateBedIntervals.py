#!/usr/bin/env python
import sys
import bx.seq.twobit
import collections
import itertools
from optparse import OptionParser
from common import *
def returnFileIter( fh ):
    for line in fh:
        yield line

def get_seq (chrom, start, end, bxtwobit):
    start=int(start)
    end=int(end)
    sequence=bxtwobit[chrom][start:end]
    sequence=sequence.upper()
    
    return sequence

def main():
    usage = "usage: %prog [options] file.bed\n given a bed file and tbf, concatenate bed intervals into a single fasta file\n"
    parser = OptionParser(usage)
    parser.add_option("--tbf", type="string", dest="tbf", default="/share/home/indapa/genomes/hg19/hg19.2bit", help="path to twobit file")
    parser.add_option("--fastaheader", type="string", dest="faheader", default="seq", help="fasta header string (default seq)")
    parser.add_option("--fasta", type="string", dest="faout", default="seq.fa", help="name of fasta file (default seq.fa) ")
    (options, args)=parser.parse_args()
    

    bedfile=args[0]



    try:
        sys.stderr.write("opening twobitfile...\n")
        twobit=bx.seq.twobit.TwoBitFile( open( options.tbf ) )
    except:
        sys.stderr.write("unable to open twobit file!\n")
        sys.exit(1)
        
    bedfh=open(bedfile, 'r')

    targetsequence=''

    for line in bedfh:
        (chr, start, end,name)=line.strip().split('\t')
        sequence= get_seq(chr, start, end, twobit)
        
        targetsequence+=sequence
        print len(sequence)
    print len(targetsequence)

    writefasta(targetsequence, option.faheader, faout)

if __name__ == "__main__":
    main()


