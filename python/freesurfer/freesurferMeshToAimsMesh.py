from numpy import array, dot, hstack, reshape
from soma import aims
import sys

def freesurferMeshToAimsMesh(meshfile, anatfile, mni_trm, outputmeshfile):
    ''' Transform mesh file from the Freesurfer coordinates system to the
    AIMS one for the image anatfile. The transform goes through MNI space,
    thus needs the scanner-based to MNI transformation (.trm converted version
    of the talairach.auto.xfm in Freesurfer)
    '''

    finder = aims.Finder()
    if not finder.check(anatfile):
        raise IOError('File not recognized: %s' % anatfile)
    header = finder.header()
    sb = list(header['referentials']).index(
        'Scanner-based anatomical coordinates')
    if sb < 0:
        raise ValueError(
            'Scanner-based transformation not found in image header')
    a_to_s = aims.AffineTransformation3d(header['transformations'][sb])
    s_to_mni = aims.read(mni_trm)

    mesh = aims.read(meshfile)
    mni_r = -1
    refs = list(mesh.header()['referentials'])
    for ref in ('Talairach',
                aims.StandardReferentials.mniTemplateReferential(),
                aims.StandardReferentials.mniTemplateReferentialID()):
        mni_r = refs.index('Talairach')
        if mni_r >= 0:
            break
    if mni_r < 0:
        raise ValueError('MNI transform not found in mesh header')

    m_to_mni = aims.AffineTransformation3d(
        mesh.header()['transformations'][mni_r])
    m_to_a = a_to_s.inverse() * s_to_mni.inverse() * m_to_mni
    aims.SurfaceManip.meshTransform( mesh, m_to_a )
    if mesh.header().has_key('material'):
        # remove any counter-clockwise polygons ordering
        del mesh.header()['material']

    aims.write(mesh, outputmeshfile)


def usage():
    print "Convert Freesurfer mesh file to Aims mesh file"
    print "usage: python freesurferMeshToAimsMesh meshfile.mesh anatfile.nii scanner_to_talairach.trm outputmeshfile.mesh"

if __name__ == "__main__":
    if len(argv)!=4:
        print usage()
        sys.exit(1)
    print "Mesh file:", sys.argv[1]
    print "Anat file:", sys.argv[2]
    print "Scanner to MNI transorm file:", sys.argv[3]
    print "Output mesh file:", sys.argv[4]
    freesurferMeshToAimsMesh(sys.argv[1], sys.argv[2], sys.argv[3],
                             sys.argv[4])




