# -*- coding: utf-8 -*-
from numpy import array, vstack
import math
from soma import aims, aimsalgo
#from tio import Texture
#import nipy.neurospin.graph as FG
from numpy.linalg import pinv
import pickle
import sys
import numpy

def regularizeMeshAims(brainMesh, isinFile,
                       output_mesh, realsphere='./ico100_7.mesh'):
    brain = aims.read(brainMesh)
    sphere = aims.read(realsphere)
    isin = pickle.load(open(isinFile))
    triangles = aims.TimeTexture( isin[0] )
    aisin = numpy.array( isin[1] )
    coords1 = aims.TimeTexture( aisin[:,0] )
    coords2 = aims.TimeTexture( aisin[:,1] )
    coords3 = aims.TimeTexture( 1. - aisin[:,0] - aisin[:,1] )
    mi = aims.MeshInterpoler( brain, sphere )
    mi.reloadProjectionParams( triangles, coords1, coords2, coords3 )
    sphere2 = mi.resampleMesh( brain )
    aims.write(sphere2, output_mesh)


def regularizeMesh(brainMesh, isinFile,
                   output_mesh, realsphere='./ico100_7.mesh'):
    brain = aims.read(brainMesh)
    origvertex = array(brain.vertex()).squeeze()
    poly = array(brain.polygon())
    sphere = aims.read(realsphere)
    svertex = array(sphere.vertex()).squeeze()
    
    isin = pickle.load(open(isinFile))
    isin = vstack((array(isin[0]), array(isin[1]).T)).T
    
    for v in range(len(svertex)):
        origv = origvertex[poly[isin[v][0]]]
        lam, gam = isin[v][1:3]
        #if (lam != 0) & (gam != 0):
        sphere.vertex()[v] = lam*origv[1] + gam*origv[2] + (1.-lam-gam)*origv[0]
    
    # inverser les polygones
    #for i in sphere.polygon():
    #    i[0], i[2] = i[2], i[0]
    
    sphere.updateNormals()
    aims.write(sphere, output_mesh)


def usage():
    print "Regularize the mesh"
    print "usage : python regularizeMeshFromIsin brain_mesh isin regular_sphere_mesh output_mesh"


if __name__ == "__main__":
    if len(sys.argv)!=5:
        usage()
        sys.exit(1)
    print "Brain mesh:", sys.argv[1]
    print "Isin file:", sys.argv[2]
    print "Real sphere mesh:", sys.argv[3]
    print "Output mesh:", sys.argv[4]
    #regularizeMesh(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[3])
    regularizeMeshAims(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[3])


