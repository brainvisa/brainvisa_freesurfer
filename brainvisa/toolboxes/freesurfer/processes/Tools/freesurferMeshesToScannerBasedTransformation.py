from brainvisa.processes import *
from brainvisa.tools import aimsGlobals
from brainvisa import registration
from soma import aims

name = 'FreeSurfer Meshes to Scanner-based Transformation'

signature = Signature(
  'anat', ReadDiskItem( 'RawFreeSurferAnat', 'Aims readable volume formats' ),
  'freesurfer_meshes_referential',
    ReadDiskItem( 'Referential of Pial', 'Referential' ),
  'scanner_based_referential',
    ReadDiskItem( 'Scanner Based Referential', 'Referential' ),
  'scanner_based_to_meshes_transform',
    WriteDiskItem( 'Freesurfer Scanner To Meshes Transformation',
      'Transformation matrix' ),
)


def initialization( self ):
  self.linkParameters( 'scanner_based_referential', 'anat' )
  self.linkParameters( 'freesurfer_meshes_referential', 'anat' )
  self.linkParameters( 'scanner_based_to_meshes_transform',
    'freesurfer_meshes_referential' )


def execution( self, context ):
  atts = aimsGlobals.aimsVolumeAttributes( self.anat )
  vs = atts.get( 'voxel_size' )
  s2m = atts.get( 'storage_to_memory' )
  if s2m is None:
    s2m = aims.AffineTransformation3d()
  else:
    s2m = aims.AffineTransformation3d( s2m )
  if vs:
    vs2 = ( s2m.transform( vs[:3] ) - s2m.transform( [ 0,0,0 ] ) ) / 2.
    tr = aims.AffineTransformation3d()
    tr.setTranslation( vs2 )
    aims.write( tr, self.scanner_based_to_meshes_transform.fullPath() )
    self.scanner_based_to_meshes_transform.setMinf( 'source_referential',
      self.scanner_based_referential.uuid(), saveMinf=False )
    self.scanner_based_to_meshes_transform.setMinf( 'destination_referential',
      self.freesurfer_meshes_referential.uuid(), saveMinf=True )


