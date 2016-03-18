#! /usr/bin/env python2
from numpy import vstack, array, zeros
import pickle
from tio import Texture
import sys
from soma import aims


def regularizeParcelTexture(isin, mesh, tex, output):
    fisin = open(isin, 'r')
    mesh = aims.read(mesh)
    tex = Texture.read(tex)
    
    isin = pickle.load(open(isin))
    isin = vstack((array(isin[0]), array(isin[1]).T)).T

    output = Texture(filename=output, data=zeros(len(isin)))
    
    for n in range(len(isin)):
        t = tex.data[mesh.polygon()[isin[n][0]].arraydata()]
        weights = array([(1-isin[n][1]-isin[n][2]), isin[n][1], isin[n][2]])
        value = t[weights.argmax()]
        output.data[n] = value
    
    output.write()

def usage():
    print "Regularize parcels texture"
    print "usage : regularizeParcelTexture.py isin white_mesh tex output"


if __name__ == "__main__":
    if len(argv)!=5:
        usage()
        sys.exit(1)
    print "Isin file:", argv[1]
    print "White mesh:", argv[2]
    print "Input texture:", argv[3]
    print "Output texture:", argv[4]
    regularizeParcelTexture(argv[1], argv[2], argv[3], argv[4])
