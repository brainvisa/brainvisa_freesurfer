from numpy import array, dot, hstack, reshape
from soma import aims
import sys

def freesurferMeshToAimsMesh(meshfile, anatfile, outputmeshfile):
    anat = aims.read(anatfile)
    z = array(anat.header()['transformations'][0]).reshape(4, 4)
    
    mesh = aims.read(meshfile)

    for i in range(len(mesh.vertex())):
        mesh.vertex()[i] = dot(z,hstack((mesh.vertex()[i], [1])))[:3]

    for p in mesh.polygon():
        p[0],p[2] = p[2],p[0]

    mesh.updateNormals()
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




