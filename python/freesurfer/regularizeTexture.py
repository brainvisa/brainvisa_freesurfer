#! /usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

from numpy import vstack, array
import numpy as np
import pickle
import sys
from soma import aims


def regularizeTexture(isin, mesh, tex, output):
    fisin = open(isin, 'r')
    mesh = aims.read(mesh)
    tex = aims.read(tex)

    isin = pickle.load(open(isin, 'rb'))
    isin0 = array(isin[0])
    isin1 = array(isin[1])

    output_tex = aims.TimeTexture(dtype=tex[0].np.dtype)

    t = tex[0].np[mesh.polygon().np[isin0]]
    weights = vstack(
        ((1 - isin1[:, 0] - isin1[:, 1]), isin1[:, 0], isin1[:, 1])).T
    value = np.sum(t * weights, axis=1)
    output_tex[0].assign(value)

    aims.write(output_tex, output)


def usage():
    print("Regularize texture")
    print(
        "usage : regularizeTexture.py isin original_white_mesh input.tex output.tex")
    print(
        "example : regularizeTexture.py lh.isin lh.white.mesh lh.curv.tex lh.r.curv.tex")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        usage()
        sys.exit(1)
    print(sys.argv)
    print("Isin file:", sys.argv[1])
    print("White mesh:", sys.argv[2])
    print("Input texture:", sys.argv[3])
    print("Output texture:", sys.argv[4])
    regularizeTexture(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
