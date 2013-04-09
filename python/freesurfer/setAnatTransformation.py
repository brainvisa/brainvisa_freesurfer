# -*- coding: utf-8 -*-
from soma import aims
from numpy import array

def setAnatTransformation(anatFile):
    a = aims.read(anatFile)
    v = a.header()['voxel_size'][:3]
    s = array( a.header()['volume_dimension'][:3] ) - 1
    n = s*v/2.0
    s2m = a.header()[ 'storage_to_memory' ]
    s2m = aims.AffineTransformation3d( s2m )
    vs2 = ( s2m.transform( v ) - s2m.transform( [ 0,0,0 ] ) ) / 2.
    n += vs2
    if len( a.header()[ 'transformations' ] ) < 2:
      tr = list( a.header()[ 'transformations' ][0] )
      tr[3] = n[0]
      tr[7] = n[1]
      tr[11] = n[2]
      a.header()[ 'transformations' ].append( tr )
      a.header()[ 'referentials' ].append( 'Coordinates aligned to another file or to anatomical truth' )
      pass
    else:
      a.header()[ 'transformations' ][1][3] = n[0]
      a.header()[ 'transformations' ][1][7] = n[1]
      a.header()[ 'transformations' ][1][11] = n[2]
      a.header()[ 'referentials' ][1] = 'Coordinates aligned to another file or to anatomical truth'
    aims.write(a, anatFile)

def usage():
    print "Set first transformation matrix to the center of the image"
    print "usage: python setAnatTransformation.py anat.nii"

if __name__ == "__main__":
    if len(sys.argv)!=2:
        usage()
        sys.exit(1)
    setAnatTransformation(sys.argv[1])

