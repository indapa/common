#!/bin/bash

# Sort VCF file keeping the header. The head command is for performance. 
#adapted from here: http://vcftools.sourceforge.net/docs.html#one-liners
(cat $1  | head -n4| grep ^\#; cat $1  | grep -v ^\# | sort -k1,1d -k2,2n;)  