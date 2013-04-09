from numpy import array, dot, hstack, reshape
from soma import aims
import sys

def freesurferMeshToAimsMesh(meshfile, anatfile, outputmeshfile):
    finder = aims.Finder()
    if not finder.check( anatfile ):
      raise IOError( 'File not recognized: %s' % anatfile )
    header = finder.header()
    a_to_s = aims.AffineTransformation3d( header['transformations'][-1] )

    mesh = aims.read(meshfile)
    aims.SurfaceManip.meshTransform( mesh, a_to_s )

    aims.write(mesh, outputmeshfile)


def usage():
    print "Convert Freesurfer mesh file to Aims mesh file"
    print "usage: python freesurferMeshToAimsMesh meshfile.mesh anatfile.nii outputmeshfile.mesh"

if __name__ == "__main__":
    if len(argv)!=4:
        print usage()
        sys.exit(1)
    print "Mesh file:", sys.argv[1]
    print "Anat file:", sys.argv[2]
    print "Output mesh file:", sys.argv[3]
    freesurferMeshToAimsMesh(sys.argv[1], sys.argv[2], sys.argv[3])




