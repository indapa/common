"""

a collection of useful python functions. 

""" 

import sys
import string
import math
import itertools
import gzip
import os
import collections




def fasta_iter(fasta_name):
    """
    given a fasta file. yield tuples of header, sequence: https://www.biostars.org/p/710/#1412
    """
    fh = open(fasta_name)
    # ditch the boolean (x[0]) and just keep the header or sequence since
    # we know they alternate.
    faiter = (x[1] for x in itertools.groupby(fh, lambda line: line[0] == ">"))
    for header in faiter:
        # drop the ">"
        header = header.next()[1:].strip()
        # join all sequence lines to one.
        seq = "".join(s.strip() for s in faiter.next())
        yield header, seq


def difference (a, b):
    """ return the set difference between A and B 
    """
    return set(a) - set(b)

def intersect(a, b):
    """ return the intersection between list a and b  
    """
    return set(a).intersection(set(b))


def yieldBedIntervals(bedfh,size,overlap=0):
    """ given a filehandle with chromosome sizes and size window and overlap
        yield bed record of that size and overlap """
    regions=[]
    region_size=size
    for line in bedfh:
        if '_' in line: continue
        if "#" in line: continue
        fields = line.strip().split("\t")

        chrom_name = fields[0]
        
        chrom_length = int(fields[1])
        region_start = 0
        
        while region_start < chrom_length-overlap:
            start = region_start
            end = region_start + region_size
            if end > chrom_length:
                end = chrom_length
            region_string = chrom_name + "\t" + str(region_start) + "\t" + str(end)
            yield region_string
            #outfile=".".join([chrom_name+':'+str(region_start)+".."+str(end), 'bed'])
            #outfh=open(outfile, 'w')
            #regions.append(region_string)
            #outfh.write(region_string+"\n")
            region_start = end - overlap

    

def yieldFastqRecord (fh):
    """ a generator that yields a tuple of (fastq_readname, sequence, qualstring)
    adapted from this http://www.biostars.org/p/67246/#67556 
    yields a tuple with (header_name,sequence)
    See http://freshfoo.com/blog/itertools_groupby """

    fqiter=(x[1] for x in itertools.groupby(fh, lambda line: line[0] == '@'))
    #fqiter is made of sub-iterators

    #the first sub-iter is the header
    for header in fqiter:
        readname=header.next().strip()
        #then the next sub-iters are sequence, '+', and qual
        #we concat them into a single string, then split them by '+'
        (sequence,quals)="".join(s.strip() for s in fqiter.next()).split("+",1)
        #finally we yield
        yield readname,sequence,quals

def yieldFastqReadpair(fh1,fh2):
    
    """ This is just calling izip on yieldFastqRecord when given two filehandles  """
    
    fqiter_gen1=yieldFastqRecord(fh1)
    fqiter_gen2=yieldFastqRecord(fh2)
    
    for fqrec1, fqrec2 in itertools.izip(fqiter_gen1, fqiter_gen2):
        yield fqrec1, fqrec2
        
         
     
 
        
def yieldFastaRecord (fh):
    """ adapted from this http://www.biostars.org/p/67246/#67556
        yields a tuple with (header_name,sequence)"""

    faiter = (x[1] for x in itertools.groupby(fh, lambda line: line[0] == ">"))
    for header in faiter:
        header = header.next()[1:].strip()
        yield header, "".join(s.strip() for s in faiter.next())


def determineAltBases( genotypes, refbase):
    """ given a list of  genotypes and the ref base, determing the segregating alt base """

    alleles= [ list(tuple(g)) for g in genotypes ]
    observed_alleles=set( list(itertools.chain.from_iterable(alleles)) )

    alt='.'
    altbases= list( observed_alleles - set(refbase) )

    if len(altbases) == 0:
        alt='.'

    elif len(altbases) > 1:
        alt=",".join(altbases )
    else:
        alt=altbases[0]
    return alt



def numericalGenotypes( refbase,altstring, genostr):
    """ given refbase and comma-delimited string of alternate bases and n-character genotype string,
    return the numerical genotype where 1 is the reference and 2 and above be alternate.
    if the reference was G and alternate was C, GC genotype would be 1/2"""


    altbases=altstring.split(',')
    altbases.sort()

    segregating_alleles=[refbase] + altbases
    numerical_alleles=range(len(segregating_alleles))

    genotype_map=dict(zip(segregating_alleles, numerical_alleles))
    genotyped_alleles=tuple(genostr)
    try:
        nmapped=[ str(genotype_map[x]) for x in genotyped_alleles ]
    except KeyError:
        print 'allele in genotype not in list of ref or alt alleles!'
        return '-1/-1'

    return "/".join(nmapped)


def indexToGenotype( index,alleles='ACGT',ploidy=2 ):
    """ return genotype at a given index position after
    enumerating all possible genotypes given string of alleles and
    assigning to a list. By default the list contains all possible 10 genotypes"""


    genotypes= [ "".join(list(genotype))  for genotype in combinations_with_replacement(alleles, ploidy) ]

    try:
       return genotypes[index]
    except IndexError:
        print "Index out of bounds, not a valid index for list of genotypes"


def genotypeToIndex( geno, ploidy=2,alleles='ACGT'):
    """
    given a genotype return its index in the enumerated list of possible
    genotypesgiven ploidy and alleles 
    """


    genotypes= [ "".join(list(genotype))  for genotype in combinations_with_replacement(alleles, ploidy) ]
    

    try:
        return  genotypes.index(geno)
    except ValueError:
        print "genotype not in list of genotypes."


def writefasta_stdout(sequence, name):
    """ write fasta formated output of a sequence"""
    l = len( sequence )
    c = 0
    sys.stdout.write( ">%s\n" % name )
    while c < l:
        b = min( c + 50, l )
        sys.stdout.write( "%s\n" % str( sequence[c:b] ) )
        c = b


def writefasta(sequence, name, filename):
    """ write fasta formated output of a sequence to file"""
    fh=open(filename, 'w')
    l = len( sequence )
    c = 0
    fh.write( ">%s\n" % name )
    while c < l:
        b = min( c + 50, l )
        fh.write( "%s\n" % str( sequence[c:b] ) )
        c = b

def order(j,k): 
    return (k * (k + 1) / 2) + j



def grouper(n, iterable, fillvalue='x'):
    """ 
    iterate through an utterable n values at a time
    http://stackoverflow.com/a/2990151       
    grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    """

    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def complement(s):
    """ 
    for reverse complementing a sequence
    Return the complementary sequence string.
    """

    basecomplement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    letters = list(s)
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters)

def reversecomplement(s):
     """
     Return the reverse complement of the dna string.
     """
     s = s[::-1]
     s = complement(s)
     return s


def typeofGenotype(allele1, allele2):
    """ 
    I really should be a python version of a typedef here, but dont know how
    hom_ref =0 het =1 hom_nonref=2 no_call=3                             
    """

    #print allele1, allele2


    if allele1== '.' or allele2 == '.': return 3

    if allele1 == '0' and allele2 == '0': return 0

    if allele1 == '0' and allele2 != '0': return 1
    if allele1 != '0' and allele2 == '0': return 1


    #if allele1 == '0' and allele2== '1': return 1
    #if allele1 =='1' and allele2 == '0': return 1

    if allele1 != '0' and allele2 != '0': return 2

def isTransition(allele1, allele2):
    """
    return if allele change is transition (allelle1 -> allele2)
    """
    if allele1 == 'A':
        if allele2 == 'G':
            return True
    elif allele1 == 'G':
        if allele2 == 'A':
            return True
    elif allele1 == 'C':
        if allele2 == 'T':
            return True
    elif allele1 == 'T':
        if allele2 == 'C':
            return True
    else:
        sys.stderr.write("skipping indel for transition/transversion classification\n")
        
    return False


def yield_bedcoordinate(fh):
    """ yield a tuple of (chr, start,end) from bed file """
    for line  in fh:
        if '@' in line: continue
        if '#' in line: continue
        fields=line.strip().split("\t")
        (chr, start, end) = fields[0:3]
        yield(chr, int(start), int(end) )

def PhredScore(errorprob):
    """ given an error probbability, return the phred-scaled value: -10 * log_10(error) """
    if errorprob == 0:
        return 100
    
    return   -10 * math.log10(errorprob)


def ErrorProb(phredscore):
    """ given a phred-scaled score, return the error prob: 10^(-Q/10) """
    return pow(10,(-phredscore/10))

	
def melt_lol (l):
    """ melt a list of lists into a single list: http://stackoverflow.com/a/952952 """
    return [item for sublist in l for item in sublist]

def return_file_basename(file):
    """ Return the base name of pathname path: see http://docs.python.org/2/library/os.path.html
        and http://stackoverflow.com/a/678242"""


    return os.path.basename(os.path.splitext(file)[0])



def twoBitExtract(bedstring, twobit):
    """ given a bedstring and bx.seq.twobit object, extract the sequence from the intervals parsed from the bedstring """
    (chr, start, end, name)=bedstring.split('\t')
    
    start=int(start)
    end=int(end)
 
    assert( end > start ),"end less  than start!"
    sequence=twobit[chr][start:end]
    return sequence.upper()

def containsDuplicates(L):
    """ returns True of list L contains duplicates """
    if [ x for x,y in collections.Counter(L).items() if y > 1]:
        return True
    return False

#def duplicateIndices(L):
#    """ return indices of duplicate records in a list L """
    

def list_duplicates(seq):
    """ return a list of tuples: [ (duplicate_val, [indice]), .... ]  """
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

def isMaxDuplicated(L):
    """ return True False if the max value of a list is duplicated """
    return max(L) in  [x for x,y in collections.Counter(L).items() if y > 1]

def decode_duplicate(ALPHABET, totalsize, L):
    DECODED=[]
    for i in  L[0:totalsize]:
        if type(i) is int: DECODED.append( ALPHABET[ i ] )
        else:
            DECODED.append( ";".join([ ALPHABET[x] for x in i]) )
    return DECODED
            
               
def zerodiv_tuple(t):
    """ given a tuple (x,y), divide, but if its 0/0 return 0 """
    
    if t[0] == 0 and t[1] == 0:
        return 0
    return t[0]/t[1]
      
        
    
