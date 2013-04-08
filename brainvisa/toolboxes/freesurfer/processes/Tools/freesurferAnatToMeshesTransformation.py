from brainvisa.processes import *
from brainvisa.tools import aimsGlobals
from brainvisa import registration
from soma import aims

name = 'Anat To FreeSurfer Meshes Transformation'

signature = Signature(
  'anat', ReadDiskItem( 'RawFreeSurferAnat', 'Aims readable volume formats' ),
  'freesurfer_meshes_referential',
    ReadDiskItem( 'Referential of Pial', 'Referential' ),
  'anat_referential',
    ReadDiskItem( 'Referential of Raw T1 MRI', 'Referential' ),
  'anat_to_meshes_transform',
    WriteDiskItem( 'Freesurfer Anat To Meshes Transformation',
      'Transformation matrix' ),
)


def initialization( self ):
  self.linkParameters( 'anat_referential', 'anat' )
  self.linkParameters( 'freesurfer_meshes_referential', 'anat' )
  self.linkParameters( 'anat_to_meshes_transform',
    'freesurfer_meshes_referential' )


def execution( self, context ):
  atts = aimsGlobals.aimsVolumeAttributes( self.anat )
  tr = aims.AffineTransformation3d( atts[ 'transformations' ][0] )
  aims.write( tr, self.anat_to_meshes_transform.fullPath() )
  self.anat_to_meshes_transform.setMinf( 'source_referential',
    self.anat_referential.uuid(), saveMinf=False )
  self.anat_to_meshes_transform.setMinf( 'destination_referential',
    self.freesurfer_meshes_referential.uuid(), saveMinf=True )


