from __future__ import print_function
from numpy import array
import numpy
# from tio import Texture
from soma import aims
import sys


def usage():
    print("concatenate textures")
    # print("usage: concatenate_textures.py output.tex file1.tex ...
    # fileN.tex")


def concatenate_textures(output, fileL, fileR):
    print('*** concatenate_textures ***')
    gyriTexR = aims.read(fileR)
    gyriTexL = aims.read(fileL)
    gyriTexB = gyriTexL.__class__()
    vertexNbR = gyriTexR[0].nItem()
    vertexNbL = gyriTexL[0].nItem()
    vertexNbB = vertexNbR + vertexNbL
    gyriTexB[0].resize(vertexNbB)
    arr_b = gyriTexB[0].arraydata()
    arr_b[:vertexNbL] = gyriTexL[0].arraydata()
    lh_max = gyriTexL[0].arraydata().max() + 2
    arr_b[vertexNbL:] = gyriTexR[0].arraydata() + lh_max
    # fix header
    new_lt = {}
    if 'GIFTI_labels_table' in gyriTexL.header():
        print('copy GIFTI_labels_table')
        lt = gyriTexL.header()['GIFTI_labels_table']
        for i in range(lh_max - 1):
            try:
                new_lt[i] = lt[i]
            except:
                pass
    if 'GIFTI_labels_table' in gyriTexR.header():
        lt = gyriTexR.header()['GIFTI_labels_table']
        for i in range(gyriTexR[0].arraydata().max() + 1):
            try:
                new_lt[lh_max + i] = lt[i]
            except:
                pass
    gyriTexB.header().update(gyriTexL.header())
    print('new_lt:', new_lt)
    if len(new_lt) != 0:
        # aims bindings for IntKeyDictionary are incomplete, use the existing
        # object
        lt = gyriTexB.header()['GIFTI_labels_table']
        for i, v in new_lt.items():
            lt[i] = v
        # should just be:
        # gyriTexB.header()['GIFTI_labels_table'] = new_lt
    print('header:')
    print(gyriTexB.header())
    aims.write(gyriTexB, output)

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        usage()
        sys.exit(1)
    output = sys.argv[1]
    fileL = sys.argv[2]
    fileR = sus.argv[3]
    concatenate_textures(output, fileL, fileR)
