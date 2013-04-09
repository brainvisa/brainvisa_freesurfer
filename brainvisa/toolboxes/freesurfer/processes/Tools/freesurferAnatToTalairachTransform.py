from brainvisa.processes import *
from soma import aims
import numpy
from brainvisa import registration

name = 'FreeSurfer anatomy to Talairach transformation'

signature = Signature(
  'scanner_based_referential',
    ReadDiskItem( 'Scanner Based Referential', 'Referential' ),
  'freesurfer_talairach_auto',
    ReadDiskItem( 'Talairach Auto Freesurfer',
      'MINC transformation matrix' ),
  'transform_to_mni',
    WriteDiskItem( 'Freesurfer Scanner To MNI Transformation',
      'Transformation matrix' ),
)


def initialization( self ):
  self.linkParameters( 'freesurfer_talairach_auto',
    'scanner_based_referential' )
  self.linkParameters( 'transform_to_mni', 'scanner_based_referential' )


def execution( self, context ):
  # import / convert transformation to MNI space
  m = []
  i = 0
  rl = False
  for l in open( self.freesurfer_talairach_auto.fullPath() ).xreadlines():
    if l.startswith( 'Linear_Transform =' ):
      rl = True
    elif rl:
      if l.endswith( ';\n' ):
        l = l[:-2]
      m.append( [ float(x) for x in l.split() ] )
      i += 1
      if i == 3:
        break

  talairach_freesrufer = aims.AffineTransformation3d(
    numpy.array( m  + [[ 0., 0., 0., 1. ]] ) )

  aims.write( talairach_freesrufer, self.transform_to_mni.fullPath() )
  tm = registration.getTransformationManager()
  tm.setNewTransformationInfo( self.transform_to_mni,
    source_referential=self.scanner_based_referential,
    destination_referential= \
      tm.referential( registration.talairachMNIReferentialId ) )

