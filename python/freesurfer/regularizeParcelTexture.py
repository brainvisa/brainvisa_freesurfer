#! /usr/bin/env python2
from numpy import vstack, array, zeros
import pickle
import sys
from soma import aims


def regularizeParcelTexture(isin, mesh, tex, output):
    fisin = open(isin, 'r')
    mesh = aims.read(mesh)
    tex = aims.read(tex)

    isin = pickle.load(open(isin))
    isin = vstack((array(isin[0]), array(isin[1]).T)).T

    output_tex = tex.__class__()
    output_tex.header().update(tex.header())
    output_tex[0].resize(len(isin))
    arr_output = output_tex[0].data().arraydata()
    arr_tex = tex[0].data().arraydata()

    for n in range(len(isin)):
        t = arr_tex[mesh.polygon()[isin[n][0]].arraydata()]
        weights = array([(1-isin[n][1]-isin[n][2]), isin[n][1], isin[n][2]])
        value = t[weights.argmax()]
        arr_output[n] = value

    aims.write(output_tex, output)

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
