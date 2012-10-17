# -*- coding: utf-8 -*-
from soma import aims
from numpy import array

def setAnatTransformation(anatFile):
    a = aims.read(anatFile)
    v = array(a.header()['voxel_size'])
    s = array(a.header()['volume_dimension']) - 1
    n = s*v/2.0
    a.header()['transformations'][0][3] = n[0]
    a.header()['transformations'][0][7] = n[1]
    a.header()['transformations'][0][11] = n[2]
    aims.write(a, anatFile)
    
def usage():
    print "Set first transformation matrix to the center of the image"
    print "usage: python setAnatTransformation.py anat.nii"

if __name__ == "__main__":
    if len(sys.argv)!=2:
        usage()
        sys.exit(1)
    setAnatTransformation(sys.argv[1])

