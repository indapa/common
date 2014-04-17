# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import sys

for line in sys.stdin:
    print "".join([x if ord(x) < 128 else '?' for x in line.strip()])



# <codecell>


