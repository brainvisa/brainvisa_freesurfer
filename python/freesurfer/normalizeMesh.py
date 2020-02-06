#! /usr/bin/env python
from __future__ import print_function

from numpy import dot, array
from soma import aims
from scipy.io import loadmat
import sys
from numpy.linalg import inv


def normalizeMesh(anat, anat_mat, normanat, meshpath, output):
    anat = aims.read(anat)
    trans_anat = aims.Motion(anat.header()['transformations'][0])
    anat_mat = loadmat(anat_mat)
    af = anat_mat['Affine']
    vg = anat_mat['VG'].mat
    vf = anat_mat['VF'].mat
    C = dot(dot(vg, inv(af)), inv(vf))
    normalisation = aims.Motion(C.ravel())
    norm = aims.read(normanat)
    trans_norm = aims.Motion(norm.header()['transformations'][0])
    mesh = aims.read(meshpath)
    aims.SurfaceManip.meshTransform(mesh, trans_anat)
    aims.SurfaceManip.meshTransform(mesh, normalisation)
    aims.SurfaceManip.meshTransform(mesh, trans_norm)
    mesh.updateNormals()
    aims.write(mesh, output)


def usage():
    print("Normalize mesh")
    print(
        "usage: normalizeMesh.py anat.nii anatmat_sn.mat normanat.nii anat.mesh output.mesh")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        usage()
        sys.exit(1)

    anat = sys.argv[1]
    anat_mat = sys.argv[2]
    normanat = sys.argv[3]
    meshpath = sys.argv[4]
    output = sys.argv[5]
    normalizeMesh(anat, anat_mat, normanat, meshpath, output)
