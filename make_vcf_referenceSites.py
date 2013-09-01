#!/usr/bin/env python
import argparse
from common import yield_bedcoordinate
import bx.seq.twobit
from VcfRecord import *
from VcfGenotype import *
""" given a bedstring and bx.seq.twobit object, extract the sequence from the intervals parsed from the bedstring """
def twoBitExtract(bedstring, twobit):
    (chr, start, end)=bedstring.split('\t')
    
    start=int(start)
    end=int(end)
 




def main():

    usage = "usage: %prog [options] interval.bed"
    parser = argparse.ArgumentParser(description='make reference vcf records based on non-variant interval bed file and pedfile')
    parser.add_argument('bed', metavar='bed', type=str, help='interval.bed')
    parser.add_argument("-ped", metavar='pedfile', type=str, help="file.ped")
    parser.add_argument("-twobitfile", metavar='tbf', type=str, help="file.2bit")

    args=parser.parse_args()

    samples=[]

    pedfh=open(args.ped)
    bedfh=open(args.bed)
    tbf=bx.seq.twobit.TwoBitFile( open( args.twobitfile ) )

    for line in pedfh:
        samples.append( line.split('\t')[1] )



    print "##fileformat=VCFv4.1"
    print "##INFO=<ID=NS,Number=1,Type=Integer,Description=\"Number of Samples With Data\">"
    print "##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">"
    print "\t".join(["#CHROM",  "POS" ,"ID", "REF", "ALT", "QUAL", "FILTER",  "INFO","FORMAT"]+samples)

    for (chrom,start,end) in yield_bedcoordinate(bedfh):
        for pos in range(start+1,end+1):
            sequence=tbf[chrom][pos-1:pos]
            vrec=VcfRecord(chrom,str(pos), '.', sequence,info="NS=8")
            genotypelist=[ VcfGenotype("GT","0/0") for z in range(len(samples))  ]
            vrec.addGenotypeList(genotypelist)
            print vrec.toStringwithGenotypes()


    

if __name__=="__main__":
    main()
