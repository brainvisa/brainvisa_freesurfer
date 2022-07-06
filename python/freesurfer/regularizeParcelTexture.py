#! /usr/bin/env python
from __future__ import print_function
from __future__ import absolute_import

from numpy import vstack, array
import numpy as np
import pickle
import sys
from soma import aims


def regularizeParcelTexture(isin, mesh, tex, output):
    fisin = open(isin, 'r')
    mesh = aims.read(mesh)
    tex = aims.read(tex)

    isin = pickle.load(open(isin, 'rb'))
    isin0 = array(isin[0])
    isin1 = array(isin[1])

    output_tex = tex.__class__()
    output_tex.header().update(tex.header())
    if 'vertex_number' in output_tex.header():
        del output_tex.header()['vertex_number']
    output_tex[0].resize(len(isin[0]))
    arr_output = output_tex[0].np
    arr_tex = tex[0].np

    t = arr_tex[mesh.polygon().np[isin0]]
    weights = vstack(
        ((1 - isin1[:, 0] - isin1[:, 1]), isin1[:, 0], isin1[:, 1]))
    pweights = weights.argmax(axis=0)
    value = t[np.arange(len(pweights)), pweights]
    arr_output[:] = value

    aims.write(output_tex, output)


def usage():
    print("Regularize parcels texture")
    print("usage : regularizeParcelTexture.py isin white_mesh tex output")


if __name__ == "__main__":
    if len(argv) != 5:
        usage()
        sys.exit(1)
    print("Isin file:", argv[1])
    print("White mesh:", argv[2])
    print("Input texture:", argv[3])
    print("Output texture:", argv[4])
    regularizeParcelTexture(argv[1], argv[2], argv[3], argv[4])
