#!/usr/bin/env python
import sys
import pdb
import argparse
import urllib2
"""
This program uses the NCBI eutils package and python to download sequences from Entrez
See https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch and 
http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/
"""

def main():

    usage = "usage: %prog [options] "
    parser = argparse.ArgumentParser(description='fetch sequences from NCBI')
    parser.add_argument("-db", help="protein|nucleotide")
    parser.add_argument("-rettype", help="return type", default="fasta")
    parser.add_argument("-idfile", help="file listing ids of sequences you want to fetch")

    args = parser.parse_args()

    #construct the url to fetch the sequence
    baseurl="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db="
    
    """ 
        open the file of sequence ids
        iterate through constructing the url of the sequence to fetch
        write results to fasta file with name based on id
    """

    with open(args.idfile, 'r') as f:
        for line in f:
            seqid=line.strip()
            print seqid
            url=baseurl+args.db+"&id="+seqid+"&rettype=fasta"
            print url

            #now use urllib2 to write the sequence to file
        
            # file to be written to
            file = seqid +".fasta"

            try:
                response = urllib2.urlopen(url)
            except urllib2.HTTPError:
                sys.stderr.write("unable to fetch url")
                sys.exit(1)
	

            # You can also use the with statement:
            with open(file, 'w') as f: f.write(response.read().strip()+"\n")

if __name__ == "__main__":
    main()
