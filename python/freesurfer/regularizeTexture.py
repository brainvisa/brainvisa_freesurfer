#! /usr/bin/env python2
from numpy import vstack, array, zeros
import pickle
from tio import Texture
import sys
from soma import aims


def regularizeTexture(isin, mesh, tex, output):
    fisin = open(isin, 'r')
    mesh = aims.read(mesh)
    tex = Texture.read(tex)
    
    isin = pickle.load(open(isin))
    isin = vstack((array(isin[0]), array(isin[1]).T)).T

    output = Texture(filename=output, data=zeros(len(isin)))
    
    for n in range(len(isin)):
        t = tex.data[mesh.polygon()[isin[n][0]].arraydata()]
        value = (1-isin[n][1]-isin[n][2])*t[0] + isin[n][1]*t[1] + isin[n][2]*t[2]
        output.data[n] = value    

    output.write()


def usage():
    print "Regularize texture"
    print "usage : regularizeTexture.py isin original_white_mesh input.tex output.tex"
    print "example : regularizeTexture.py lh.isin lh.white.mesh lh.curv.tex lh.r.curv.tex"


if __name__ == "__main__":
    if len(sys.argv)!=5:
        usage()
        sys.exit(1)
    print sys.argv
    print "Isin file:", sys.argv[1]
    print "White mesh:", sys.argv[2]
    print "Input texture:", sys.argv[3]
    print "Output texture:", sys.argv[4]
    regularizeTexture(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])




