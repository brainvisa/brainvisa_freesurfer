from __future__ import print_function

from __future__ import absolute_import
from soma import aims
import numpy
import sys

infile = sys.argv[1]
splitname = sys.argv[2]
outfile = sys.argv[3]

vol = aims.read(infile)
dat = numpy.asarray(vol)
dat[dat == 3] = 0
dat[dat == 7] = 3
dat[dat == 8] = 3
dat[dat == 15] = 3
dat[dat == 16] = 3
dat[dat == 46] = 3
dat[dat == 47] = 3
dat[dat != 3] = 0
split = aims.read(splitname)
sdat = numpy.asarray(split)
dat[sdat != 0] = 0
sdat += dat
print(split)
aims.write(split, outfile)
