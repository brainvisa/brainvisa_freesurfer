#! /usr/bin/env python2
from soma import aims
from numpy import array, mean
import sys

def usage():
    print "Create average mesh from resampled brain mesh."
    print "usage: average_mesh.py output.mesh subject1.mesh ... subjectN.mesh"

def average_mesh(output, inputs):
    mesh = []
    
    for i in inputs:
        v = aims.read(i)
        mesh.append(array(v.vertex()))
        del v
    
    mesh = array(mesh)
    nmesh = aims.read(inputs[0])
    
    for i in range(len(nmesh.vertex())):
        nmesh.vertex()[i]=mean(mesh[:,i],0)
    
    nmesh.updateNormals()
    aims.write(nmesh, output)

if __name__ == "__main__":
    if len(sys.argv)<=3:
        usage()
        sys.exit(1)
    
    mesh = []
    output = sys.argv[1]
    inputs = sys.argv[2:]
    average_mesh(output, inputs)
